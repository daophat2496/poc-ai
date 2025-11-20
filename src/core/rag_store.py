import os
import base64
from io import BytesIO
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
# from docx import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from langchain_openai import OpenAIEmbeddings
from src.core.model import model, qdrant_client

EMBED_DIM = 1536  # openai embedding dimension
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

collections = qdrant_client.get_collections().collections
print(f"List of Qdrant collection: {collections}")
if not any(c.name == "rag_docs" for c in collections):
    qdrant_client.create_collection(
        collection_name="rag_docs",
        vectors_config=VectorParams(size=EMBED_DIM, distance="Cosine"),
    )

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
def add_doc_to_rag_store(text, metadata=None):
    chunks = [c.strip() for c in text.split("\n") if c.strip()]

    vectors = embedder.embed_documents(chunks)

    qdrant_client.upsert(
        collection_name="rag_docs",
        points=[
            {
                "id": i,
                "vector": vectors[i],
                "payload": {
                    "text": chunks[i],
                    **(metadata or {})
                }
            }
            for i in range(len(chunks))
        ]
    )


# --------- Query ----------
def rag_query(question: str, stream: bool = True):
    q_vec = embedder.embed_query(question)

    hits = qdrant_client.search(
        collection_name="rag_docs",
        query_vector=q_vec,
        limit=5
    )

    context = "\n\n".join([h.payload["text"] for h in hits])

    messages = [
        {"role": "system", "content": "You are an expert assistant. Use ONLY the context to answer."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    if stream:
        # ✅ return a generator of text chunks, using OpenAI streaming via LangChain
        def _gen():
            for chunk in model.stream(messages):
                if getattr(chunk, "content", None):
                    yield chunk.content

        return _gen()
    else:
        # Non-streaming: single full response
        return model.invoke(messages).content