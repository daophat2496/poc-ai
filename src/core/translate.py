from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.balance_sheet import pdf_to_images, encode_image, query_model_with_image_b64
from core.model import model
from dotenv import load_dotenv
import os
from io import BytesIO
import shutil

def stream_translate_live(text: str, direction: str):
    text = text.strip()
    if not text:
        yield ""
        return

    if direction == "VI → EN":
        sys_prompt = (
            "You are a translation engine. "
            "Translate from Vietnamese to English. "
            "Return only the translation."
        )
    else:  # EN → VI
        sys_prompt = (
            "You are a translation engine. "
            "Translate from English to Vietnamese. "
            "Return only the translation."
        )

    messages = [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=text),
    ]

    partial = ""
    for chunk in model.stream(messages):
        if chunk.content:
            partial += chunk.content
            yield partial

def stream_translate_pdf(file_bytes: bytes, direction: str):
    """
    Stream translation of an image-based PDF page by page.
    - file_bytes: raw bytes from Gradio File(type="binary")
    - direction: "VI → EN" or "EN → VI"
    """
    if not file_bytes:
        yield "Chưa chọn file PDF."
        return

    temp_pdf_path = "temp_translate.pdf"
    images_folder = "image_translate"

    with open(temp_pdf_path, "wb") as f:
        f.write(file_bytes)

    try:
        images_folder = pdf_to_images(temp_pdf_path, output_root=images_folder)
        page_files = sorted(os.listdir(images_folder))
        if not page_files:
            yield "Không tìm thấy trang nào trong PDF."
            return

        if direction == "VI → EN":
            sys_prompt = (
                "You are a translation engine. "
                "Translate all readable Vietnamese text in the image into natural English. "
                "Return only the English translation, no explanations."
            )
        else:  # EN → VI
            sys_prompt = (
                "You are a translation engine. "
                "Translate all readable English text in the image into natural Vietnamese. "
                "Return only the Vietnamese translation, no explanations."
            )

        full_text = ""

        for idx, page_file in enumerate(page_files, start=1):
            page_path = os.path.join(images_folder, page_file)
            b64_image = encode_image(page_path)

            # --- header for this page ---
            header = f"--- Page {idx} ---\n"
            full_text += header
            yield full_text  # show page header immediately

            # 🔥 stream from OpenAI + stream to UI
            chunk_iter = query_model_with_image_b64(
                [b64_image],
                prompt=(
                    "Translate all readable text on this page."
                    "Start directly with the translation."
                ),
                structure=None,
                system_message=sys_prompt,
                stream=True,  # <- now returns a generator of chunks
            )

            for chunk in chunk_iter:
                if not chunk:
                    continue
                full_text += chunk
                yield full_text  # incremental updates, similar to ChatGPT

            full_text += "\n\n"
            yield full_text  # final state for this page

    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        if os.path.exists(images_folder):
            shutil.rmtree(images_folder, ignore_errors=True)