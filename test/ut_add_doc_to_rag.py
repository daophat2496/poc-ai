from src.core.rag_store import add_doc_to_rag_store, add_catalog_entry

# === Load .txt file and push to RAG ===
def load_txt_to_rag(txt_path: str):
    # 1) Read raw text
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2) Metadata for this document
    file_name = "Nghị định về Kiểm toán nội bộ 05-2019-NĐ-CP.pdf"
    metadata = {
        "doc_name": file_name,
        "title": "Nghị định về Kiểm toán nội bộ 05/2019/NĐ-CP",
        "description": f"Nghị định về Kiểm toán nội bộ, số 05/2019/NĐ-CP, phát hành ngày 22/01/2019, Chính phủ ban hành Nghị định về kiểm toán nội bộ, Theo đề nghị của Bộ trưởng Bộ Tài chính",
    }

    # 3) Store text chunks into RAG
    add_doc_to_rag_store(text, metadata)

    # 4) Add catalog entry for routing
    add_catalog_entry(metadata)

    print(f"Done: added {file_name} to RAG.")


# ==== Example Usage ====
load_txt_to_rag("New folder/05-2019-NĐ-CP.txt")
