import os
import base64
from io import BytesIO
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
# from docx import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from qdrant_client.http import models as rest
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
from typing import List
from src.core.model import model, qdrant_client
from src.core.balance_sheet import query_model_with_image_b64
from src.models.rag_store import CatalogSelection

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

vectorstore = Qdrant(
    client=qdrant_client,
    collection_name="rag_docs",
    embeddings=embedder,
)

# catalog_retriever = vectorstore.as_retriever(
#     search_kwargs={
#         "k": 1,
#         "filter": {"doc_type": "catalog"},
#     }
# )

# --------- Text extractors ----------
def extract_text_from_pdf_text_based(file_bytes):
    reader = PdfReader(BytesIO(file_bytes))
    all_text = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        all_text.append(txt)
    return "\n".join(all_text)


def extract_text_from_pdf_image_based(file_bytes):
    # Convert PDF to image
    tmp = "tmp_ocr.pdf"
    with open(tmp, "wb") as f:
        f.write(file_bytes)
    imgs = convert_from_path(tmp, dpi=120)

    all_chunks = []
    for i, img in enumerate(imgs):
        print(f"OCR text from page {i}")
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        b64_img = base64.b64encode(buffer.getvalue()).decode()

        text = model.invoke([
            {"role": "system", "content": "You are OCR engine. Return plain text only."},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}},
                {"type": "text", "text": "Extract all text."}
            ]}
        ]).content

        all_chunks.append(text)

    os.remove(tmp)
    return "\n".join(all_chunks)


# def extract_text_from_docx(file_bytes):
#     buffer = BytesIO(file_bytes)
#     doc = Document(buffer)
#     return "\n".join([p.text for p in doc.paragraphs])


# --------- Store to vector DB ----------
def add_doc_to_rag_store(text, metadata: dict | None = None):
    BATCH_SIZE = 200

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,   # optional, helps debugging
    )

    chunks = text_splitter.split_text(text)
    if not chunks:
        return

    # vectors = embedder.embed_documents(chunks)
    doc_id = str(uuid4())

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]
        vectors = embedder.embed_documents(batch)

        qdrant_client.upsert(
            collection_name="rag_docs",
            points=[
                {
                    "id": str(uuid4()),
                    "vector": vectors[i],
                    "payload": {
                        "text": batch[i],
                        "doc_id": doc_id,
                        "chunk_index": start + i,
                        **(metadata or {})
                    }
                }
                for i in range(len(batch))
            ]
        )
    print(f"Adding chunks to RAG: {str(metadata)}")

def add_catalog_entry(payload: dict):
    """
    Store one catalog entry per document in the same Qdrant collection.
    Takes a payload dict (same style as add_doc_to_rag_store).
    Expected keys: doc_name, title, description (others are kept as-is).
    """
    parts = []
    for k, v in payload.items():
        if v is None:
            continue
        parts.append(f"{k}: {v}")

    text = "\n".join(parts)
    vector = embedder.embed_query(text)

    catalog_payload = dict(payload)
    catalog_payload.update({
        "text": text,
        "doc_type": "catalog",
    })

    qdrant_client.upsert(
        collection_name="rag_docs_catalog",
        points=[
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": catalog_payload,
            }
        ],
    )

    print(f"Adding to catalog RAG: {str(catalog_payload)}")


# --------- Query ----------

def select_relevant_docs_from_catalog(question: str) -> List[str]:
    """
    1) Use catalog_retriever to get candidate catalog docs (doc_type='catalog').
    2) Ask LLM (via query_model_with_image_b64) which doc_name(s) are relevant.
       - Returns list of doc_name strings.
       - Empty list => no RAG.
    """
    q_vec = embedder.embed_query(question)

    catalog_docs = qdrant_client.search(
        collection_name="rag_docs",
        query_vector=q_vec,
        limit=4,
        with_payload=True,
        query_filter=rest.Filter(
            must=[
                rest.FieldCondition(
                    key="doc_type",
                    match=rest.MatchValue(value="catalog"),
                )
            ]
        ),
    )
    if not catalog_docs:
        return []

    print(f">>>>>>>> Catalog hit: {catalog_docs}")
    # Build a compact textual view of candidates for the LLM
    lines = []
    for idx, d in enumerate(catalog_docs, start=1):
        meta = d.payload or {}
        doc_name = meta.get("doc_name", "")
        title = meta.get("title", "")
        desc = meta.get("description", "")

        lines.append(
            f"{idx}. doc_name={doc_name}\n"
            f"   title={title}\n"
            f"   description={desc}"
        )

    catalog_text = "\n\n".join(lines)

    system_message = (
        "You are a routing assistant.\n"
        "You receive a user question and a list of candidate documents from a catalog.\n"
        "Each candidate has: doc_name, title, description.\n\n"
        "Your job:\n"
        "- Decide which documents are relevant for answering the question.\n"
        "- You MUST return your decision using the provided Pydantic model "
        "'CatalogSelection', putting the selected doc_name strings into "
        "'relevant_doc_names'.\n"
        "- If no document is relevant, return an empty 'relevant_doc_names' list.\n"
        "- IMPORTANT: Use 'doc_name' values exactly as shown (don't invent or change them)."
    )

    prompt = (
        f"Question:\n{question}\n\n"
        f"Candidate catalog documents:\n{catalog_text}\n\n"
        "Select which doc_name values are relevant for answering this question."
    )

    selection: CatalogSelection = query_model_with_image_b64(
        image_b64_list=[],
        prompt=prompt,
        structure=CatalogSelection,
        system_message=system_message,
        stream=False,
    )

    print(f">>>>>>>>> doc selected: {selection}")

    # Safety: ensure it's a list of unique, non-empty strings
    names = []
    seen = set()
    for name in selection.relevant_doc_names:
        name = (name or "").strip()
        if name and name not in seen:
            seen.add(name)
            names.append(name)

    return names

def _retrieve_chunks_for_docs(
    question: str,
    allowed_doc_names: List[str],
    max_chunks: int = 4,
):
    """
    Retrieve enriched content chunks for RAG query,
    including more metadata (title, doc_name, doc_id, page_number, chunk_index)
    so LLM has better context.
    """
    q_vec = embedder.embed_query(question)

    raw_hits = qdrant_client.search(
        collection_name="rag_docs",
        query_vector=q_vec,
        limit=max_chunks * 5,
        with_payload=True,
    )

    context_chunks = []
    source_docs = []

    allowed_set = set(allowed_doc_names) if allowed_doc_names else set()

    for h in raw_hits:
        payload = h.payload or {}

        # skip catalog entries
        if payload.get("doc_type") == "catalog":
            continue

        doc_name = payload.get("doc_name", "Unknown document")
        title = payload.get("title") or payload.get("doc_title") or ""
        # doc_id = payload.get("doc_id", "")
        # page_number = payload.get("page_number")
        # chunk_index = payload.get("chunk_index")

        # filter by doc name
        if allowed_set and doc_name not in allowed_set:
            continue

        text = payload.get("text", "")
        if not text:
            continue

        # ------------------------------------------------------------------
        # 🟦 Build enriched metadata header (simple, no regex, no rule extraction)
        # ------------------------------------------------------------------
        meta_lines = []

        if title:
            meta_lines.append(f"Tiêu đề: {title}")
        meta_lines.append(f"Tài liệu: {doc_name}")
        # if page_number is not None:
        #     meta_lines.append(f"Trang: {page_number}")
        # if chunk_index is not None:
        #     meta_lines.append(f"Chunk: {chunk_index}")
        # if doc_id:
        #     meta_lines.append(f"Doc ID: {doc_id}")

        metadata_str = "\n".join(meta_lines).strip()

        # Final enriched chunk returned to LLM
        enriched_chunk = f"{metadata_str}\n-----\n{text}"

        context_chunks.append(enriched_chunk)
        source_docs.append(doc_name)

        if len(context_chunks) >= max_chunks:
            break

    return context_chunks, set(source_docs)


def rag_query(question: str, stream: bool = True):
    """
    Router logic:

    1) Use catalog_retriever (doc_type='catalog') to get candidate catalog docs.
    2) Ask LLM (via query_model_with_image_b64 + CatalogSelection) which doc_name(s)
       are actually relevant.
       - If none => NO RAG: answer from general knowledge.
       - If some => RAG: retrieve chunks only from those doc_name(s) and answer using KB.
    """
    # Step 1 + 2: catalog → LLM-structured router
    # allowed_doc_names = select_relevant_docs_from_catalog(question)
    # use_rag = bool(allowed_doc_names)
    allowed_doc_names = []
    use_rag = True

    if use_rag:
        # Retrieve chunks from those docs only
        context_chunks, source_docs = _retrieve_chunks_for_docs(
            question=question,
            allowed_doc_names=allowed_doc_names,
            max_chunks=4,
        )

        context = "\n\n".join(context_chunks)
        sources_text = (
            "\n".join(f"- {name}" for name in source_docs)
            or "_Không tìm thấy nguồn phù hợp_"
        )

        user_content = f"Context:\n{context}\n\nQuestion: {question}"
        system_content = """
        You are an expert assistant that answers strictly and ONLY based on the provided internal documents.

When giving an answer, you must:
- Identify and quote the exact rule, điều luật, nghị định, thông tư, hoặc công văn được nêu trong tài liệu (nếu có).  
  Ví dụ:
    - “Theo quy định tại Điều 200 Luật Doanh nghiệp 2020…”
    - “Theo Công văn số 1234/BTC-QLKT ngày …”
- Use wording that clearly references the specific source available in the retrieved context.
- If multiple regulations appear, summarize them but still cite each one explicitly.
- If the required regulation or rule does not appear in the provided context, you MUST say:  
  **“Tài liệu không cung cấp thông tin, tôi không thể trả lời.”**

Forbidden:
- Do NOT guess or fabricate luật, nghị định, công văn.
- Do NOT rely on general knowledge.
- Do NOT fill missing details.

Your output must be precise, concise, and fully grounded in the retrieved context only.
"""
    else:
        answer = "Không có tài liệu phù hợp với thông tin yêu cầu."
        sources_text = "_Không tìm thấy nguồn phù hợp_"

        if stream:
            def _gen():
                yield answer, sources_text
            return _gen()
        else:
            return answer, sources_text

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

    if stream:
        def _gen():
            answer_so_far = ""
            for chunk in model.stream(messages):
                if getattr(chunk, "content", None):
                    answer_so_far += chunk.content
                    yield answer_so_far, sources_text

        return _gen()
    else:
        answer = model.invoke(messages).content
        return answer, sources_text


# --------- List docs ----------
def list_rag_docs() -> list[str]:
    """
    Return sorted list of distinct doc_name currently stored in RAG.
    """
    doc_names = set()
    offset = None

    while True:
        points, next_offset = qdrant_client.scroll(
            collection_name="rag_docs_catalog",
            limit=100,
            offset=offset,
            with_payload=True,
        )

        for p in points:
            name = (p.payload or {}).get("doc_name")
            if name:
                doc_names.add(name)

        if next_offset is None:
            break
        offset = next_offset

    return sorted(doc_names)