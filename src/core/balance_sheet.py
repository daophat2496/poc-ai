from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
import base64
from pydantic import BaseModel
import src.prompts.balance_sheet as BalanceSheetPrompt
from src.models.balance_sheet import BalanceSheet
from src.database2.database_helpers import get_engine, save_balance_sheet_to_db
from src.core.model import model
import shutil
import pandas as pd

def pdf_to_images(pdf_path, output_folder="image"):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    images = convert_from_path(pdf_path, dpi=100)
    for i, image in enumerate(images):
        image.save(f"{output_folder}/page_{i+1:03d}.jpg", "JPEG")
    return output_folder

def encode_image(image_path):
    image = Image.open(image_path).convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def query_model_with_image_b64(image_b64_list, prompt, structure: BaseModel = None):
    message = HumanMessage(
        content=[{"type": "text", "text": prompt}]
    )

    for image_b64 in image_b64_list:
        message.content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}})

    if not structure:
        return model.invoke([message]).content

    return model.with_structured_output(structure, method="function_calling").invoke([message])

def is_affirmative_response(response: str) -> bool:
    """Check if the input response is "Yes" for "ONLY answer 'Yes' or 'No'" prompt"""
    return "yes" in response.strip().lower()

def format_number(num):
    if isinstance(num, (int, float)):
        return f"{num:,.0f}".replace(",", ".")
    return num

def process_document(file):
    if not file:
        return "No file uploaded", ""
    
    try:
        images_folder = "./image"
        company_name = None
        stock_code = None
        balance_sheet = None
        is_prev_page_contain_balance_sheet = False
        is_curr_page_contain_balance_sheet = False
        is_balance_sheet_detected = False
        previous_b64_image = None
        balance_sheet_pages = []
        balance_sheet_pages_name = []
        # results = []

        # Save the uploaded file temporarily
        temp_pdf_path = f"temp_upload.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(file)

        images_folder = pdf_to_images(temp_pdf_path)

        for page_file in sorted(os.listdir(images_folder)):
            page_path = os.path.join(images_folder, page_file)
            b64_image = encode_image(page_path)

            # Try to extract company name
            if company_name is None:
                cname = query_model_with_image_b64([b64_image], BalanceSheetPrompt.PROMPT_COMPANY_NAME)
                if not cname.lower().startswith("no"):
                    print("Found company name in ", page_file, ": ", cname)
                    company_name = cname.strip()

            # Try to extract stock code
            if stock_code is None:
                scode = query_model_with_image_b64([b64_image], BalanceSheetPrompt.PROMPT_STOCK_CODE)
                if not scode.lower().startswith("no"):
                    print("Found stock code in ", page_file, ": ", scode)
                    stock_code = scode.strip()

            # Check does this page contain balance sheet
            if not is_balance_sheet_detected:
                if is_prev_page_contain_balance_sheet:
                    response = query_model_with_image_b64([previous_b64_image, b64_image], BalanceSheetPrompt.PROMPT_IS_BALANCE_SHEET_CONT)
                    print("page: ", page_file, " - Contains balance sheet? ", response, " with previous page include ", len(previous_b64_image))
                    is_curr_page_contain_balance_sheet = "yes" in response.lower()
                else:
                    response = query_model_with_image_b64([b64_image], BalanceSheetPrompt.PROMPT_IS_BALANCE_SHEET_FIRST)
                    print("page: ", page_file, " - Contains balance sheet? ", response)
                    is_curr_page_contain_balance_sheet = "yes" in response.lower()
                # response = query_model_with_image_b64([b64_image], BalanceSheetPrompt.PROMPT_IS_BALANCE_SHEET_FIRST)
                # print("page: ", page_file, " - Contains balance sheet? ", response)
                # is_curr_page_contain_balance_sheet = "yes" in response.lower()

                if is_curr_page_contain_balance_sheet:
                    balance_sheet_pages.append(b64_image)
                    previous_b64_image = b64_image
                    balance_sheet_pages_name.append({"page": page_file, "is_prev_page_contain_balance_sheet": is_prev_page_contain_balance_sheet})
                elif is_prev_page_contain_balance_sheet:
                    is_balance_sheet_detected = True
                    print("All page with balance sheet detected. Stop scan for it.")
                # else:
                #     previous_b64_image = None

                is_prev_page_contain_balance_sheet = is_curr_page_contain_balance_sheet
                # results.append(f"Processed page: {page_file}")
        
        print(f"Process {len(balance_sheet_pages)} page(s) which have balance sheet.")

        # Process each balance sheet page individually
        all_balance_sheet_items = []
        period_end_date = None
        currency = None

        for i, page_b64 in enumerate(balance_sheet_pages):
            print(f"Extracting data from balance sheet page {i+1}/{len(balance_sheet_pages)}")
            
            try:
                page_balance_sheet = query_model_with_image_b64([page_b64], BalanceSheetPrompt.PROMPT_BALANCE_SHEET, BalanceSheet)
                
                # Collect period_end_date and currency from first successful extraction
                if period_end_date is None and page_balance_sheet.period_end_date:
                    period_end_date = page_balance_sheet.period_end_date
                if currency is None and page_balance_sheet.currency:
                    currency = page_balance_sheet.currency
                    
                # Add all items from this page
                all_balance_sheet_items.extend(page_balance_sheet.balance_sheet_items)
                
            except Exception as e:
                print(f"Error processing balance sheet page {i+1}: {str(e)}")
                continue

        # Create combined balance sheet object
        balance_sheet = BalanceSheet(
            period_end_date=period_end_date,
            currency=currency or "VND",  # Default to VND if not found
            balance_sheet_items=all_balance_sheet_items
        )


        balance_sheet_item_list = [
            [
                item.code,
                item.name,
                item.amount_end_of_period,
                item.amount_beginning_of_year
            ]
            for item in balance_sheet.balance_sheet_items
        ]

        save_balance_sheet_to_db(company_name, stock_code, balance_sheet)

        # Clean up
        os.remove(temp_pdf_path)
        shutil.rmtree(images_folder)

        df = pd.DataFrame(
            balance_sheet_item_list,
            columns=["Mã số", "Mục", "Số liệu cuối kỳ", "Số liệu đầu năm"]
        )
        # Apply formatting to the numeric columns
        df["Số liệu cuối kỳ"] = df["Số liệu cuối kỳ"].apply(format_number)
        df["Số liệu đầu năm"] = df["Số liệu đầu năm"].apply(format_number)

        return (
            "Status: Processing completed successfully"
            , company_name
            , stock_code
            , balance_sheet.period_end_date.strftime("%Y-%m-%d")
            , balance_sheet.currency
            , df
        )
    
    except Exception as e:
        print(str(e))
        return (
            f"Status: Error processing document - {str(e)}"
            , "", "", "", ""
            , pd.DataFrame(columns=["Mã số", "Mục", "Số liệu cuối kỳ", "Số liệu đầu năm"])
        )