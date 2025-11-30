import os
from pathlib import Path

from src.core.rag_store import extract_text_from_pdf_image_based


def extract_text_for_folder(folder_path: str) -> dict[str, str]:
    """
    Iterate all PDF files in the given folder, run OCR extraction for each,
    and move 'ocr_output.txt' to `<pdf_stem>.txt` in the same folder.

    Returns:
        dict[file_name] = extracted_text
    """
    results: dict[str, str] = {}

    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid folder")

    for entry in sorted(os.listdir(folder_path)):
        if not entry.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder_path, entry)
        print(f"extract text from {pdf_path}")
        # # Ensure stale ocr_output.txt is removed before each run
        # if os.path.exists("ocr_output.txt"):
        #     os.remove("ocr_output.txt")

        # with open(pdf_path, "rb") as f:
        #     file_bytes = f.read()

        # This call will append text to ocr_output.txt internally
        extract_text_from_pdf_image_based(pdf_path)
        # results[entry] = text

        # After each call, rename ocr_output.txt to match the PDF name
        # ocr_tmp = "ocr_output.txt"
        # if os.path.exists(ocr_tmp):
        #     stem = Path(pdf_path).stem
        #     dest_path = os.path.join(folder_path, f"{stem}.txt")
        #     os.replace(ocr_tmp, dest_path)

    # return results

# Call the OCR function
extract_text_for_folder("uploads")

# # Save full result to a txt file
# with open("output.txt", "w", encoding="utf-8") as f:
#     f.write(text)

print("OCR completed. Saved to output.txt")
