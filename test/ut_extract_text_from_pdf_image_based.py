from src.core.rag_store import extract_text_from_pdf_image_based

# Path to your PDF
pdf_path = "65-2022-NĐ-CP.pdf"

# Read file bytes
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Call the OCR function
extract_text_from_pdf_image_based(pdf_bytes)

# # Save full result to a txt file
# with open("output.txt", "w", encoding="utf-8") as f:
#     f.write(text)

print("OCR completed. Saved to output.txt")