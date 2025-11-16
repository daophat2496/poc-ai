from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
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
from src.database2.database_helpers import run_query
import shutil
import pandas as pd
from typing import Dict, Optional

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

def query_model_with_image_b64(image_b64_list, prompt, structure: BaseModel = None, system_message = None):
    messages = []
    
    # Add system message if provided
    if system_message:
        messages.append(SystemMessage(
            content=[{"type": "text", "text": system_message}]
        ))

    human_message = HumanMessage(
        content=[{"type": "text", "text": prompt}]
    )

    for image_b64 in image_b64_list:
        human_message.content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}})
    
    messages.append(human_message)

    if not structure:
        return model.invoke(messages).content

    return model.with_structured_output(structure, method="function_calling").invoke(messages)

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
    
    print("Start processing document")
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
                yes_no_system_prompt = "You are a document classification system that outputs binary decisions. Your responses must be exactly 'Yes' or 'No' - nothing else. No explanations, no punctuation, no additional words."
                if is_prev_page_contain_balance_sheet:
                    response = query_model_with_image_b64([previous_b64_image, b64_image], BalanceSheetPrompt.PROMPT_IS_BALANCE_SHEET_CONT, None, yes_no_system_prompt)
                    print("page: ", page_file, " - Contains balance sheet? ", response, " with previous page include ", len(previous_b64_image))
                    is_curr_page_contain_balance_sheet = "yes" in response.lower()
                else:
                    response = query_model_with_image_b64([b64_image], BalanceSheetPrompt.PROMPT_IS_BALANCE_SHEET_FIRST, None, yes_no_system_prompt)
                    print("page: ", page_file, " - Contains balance sheet? ", response)
                    is_curr_page_contain_balance_sheet = "yes" in response.lower()

                if is_curr_page_contain_balance_sheet:
                    balance_sheet_pages.append(b64_image)
                    previous_b64_image = b64_image
                    balance_sheet_pages_name.append({"page": page_file, "is_prev_page_contain_balance_sheet": is_prev_page_contain_balance_sheet})
                elif is_prev_page_contain_balance_sheet:
                    is_balance_sheet_detected = True
                    print("All page with balance sheet detected. Stop scan for it.")

                is_prev_page_contain_balance_sheet = is_curr_page_contain_balance_sheet
        
        print(f"Process {len(balance_sheet_pages)} page(s) which have balance sheet.")

        # Process each balance sheet page individually
        all_balance_sheet_items = []
        period_end_date = None
        currency = None

        for i, page_b64 in enumerate(balance_sheet_pages):
            print(f"Extracting data from balance sheet page {i+1}/{len(balance_sheet_pages)}")
            
            try:
                system_prompt = """You are a specialized financial statement data extraction system. Your role is to:
1. Extract structured financial data from balance sheet images
2. Output ONLY valid JSON format without any markdown, explanations, or additional text
3. Follow the exact schema requirements
4. Never add commentary, warnings, or explanations - only return the requested JSON structure
5. Process all provided images comprehensively and combine their data into a single output."""
                page_balance_sheet = query_model_with_image_b64([page_b64], BalanceSheetPrompt.PROMPT_BALANCE_SHEET, BalanceSheet, system_prompt)
                
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

def get_balance_sheets_general_info():
    query = """SELECT
    company_name AS "Công ty"
    , stock_code AS "Mã"
    , period_end_date AS "Kỳ báo cáo"
    , currency AS "Đơn vị tiền tệ"
    , updated_at AS "Cập nhật lúc"
FROM balance_sheets_at_end_of_period 
ORDER BY updated_at DESC"""

    rows = run_query(query)  # returns list of dict
    df = pd.DataFrame(rows)  # convert to dataframe

    # optional: format dates nicely
    if "Kỳ báo cáo" in df.columns:
        df["Kỳ báo cáo"] = pd.to_datetime(df["Kỳ báo cáo"]).dt.strftime("%d/%m/%Y")
    if "Cập nhật lúc" in df.columns:
        df["Cập nhật lúc"] = pd.to_datetime(df["Cập nhật lúc"]).dt.strftime("%d/%m/%Y %H:%M")

    return df

def parse_balance_sheet_spreadsheet(file_bytes: bytes) -> Dict[str, float]:
    """
    Parse the uploaded spreadsheet (Excel/CSV) and return a mapping:
        { balance_sheet_code (str): value_from_spreadsheet (float or None) }

    Assumptions (POC):
    - File has normal tabular structure with a header row.
    - We only care about the *first data row* (index 0).
    - Only the 10 metrics in SPREADSHEET_METRIC_MAPPING are read.
    """

    # for POC: 10 metrics we want to validate
    # key = balance sheet "code"
    # value = column name in the Excel/CSV file
    SPREADSHEET_METRIC_MAPPING: Dict[str, str] = {
        "110": "cashAndCashEquivalents",      # cash_and_cash_equivalents
        "111": "cash",                        # cash
        "112": "cashEquivalents",             # cash_equivalents
        "140": "inventoriesNet",              # inventories_total (net)
        "141": "inventories",                 # inventories
        "270": "totalAssets",                 # total_assets
        "300": "liabilities",                 # liabilities
        "400": "sharholdersEquity",           # owner_equity_total
        "410": "ownersEquity",                # owner_equity
        "440": "totalResources",              # total_capital (assets = resources)
    }

    buffer = BytesIO(file_bytes)

    # Try Excel first, fall back to CSV (your sample file is CSV)
    try:
        df = pd.read_excel(buffer)
    except Exception:
        buffer.seek(0)
        df = pd.read_csv(buffer)

    if df.empty:
        return {}

    # Use only the first data row, ignore all others for POC
    first_row = df.iloc[0]

    result: Dict[str, float] = {}

    for code, column_name in SPREADSHEET_METRIC_MAPPING.items():
        if column_name not in df.columns:
            # Column missing in spreadsheet (POC: just store None)
            result[code] = None
            continue

        raw_value = first_row[column_name]

        if pd.isna(raw_value):
            result[code] = None
            continue

        # Try to coerce to float, handling things like "1,234" or "5.57E+10"
        value: float | None
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            try:
                cleaned = str(raw_value).replace(",", "").strip()
                value = float(cleaned)
            except (TypeError, ValueError):
                value = None

        result[code] = value

    return result

# Use for POC, will refactor later
CODE_TO_NAME = {
    "110": "cash_and_cash_equivalents",
    "111": "cash",
    "112": "cash_equivalents",
    "140": "inventories_total",
    "141": "inventories",
    "270": "total_assets",
    "300": "liabilities",
    "400": "owner_equity_total",
    "410": "owner_equity",
    "440": "total_capital",
}

def _parse_numeric(value) -> Optional[float]:
    """Convert formatted strings like '1,234,567' or '5.57E+10' to float."""
    if pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        try:
            cleaned = str(value).replace(",", "").replace(" ", "").replace(".", "").strip()
            if cleaned == "":
                return None
            return float(cleaned)
        except (TypeError, ValueError):
            return None


def build_pdf_metric_dict_from_df(df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    Build mapping: code -> amount_end_of_period
    from the DataFrame returned by process_document.
    """
    metrics: Dict[str, Optional[float]] = {}

    if df is None or df.empty:
        return metrics

    for _, row in df.iterrows():
        code = str(row.get("Mã số", "")).strip()
        if code in CODE_TO_NAME:
            pdf_value = _parse_numeric(row.get("Số liệu cuối kỳ"))
            metrics[code] = pdf_value

    return metrics

def validate_balance_sheet_against_spreadsheet(
    balance_sheet_df: pd.DataFrame,
    spreadsheet_bytes: bytes,
    tolerance: float = 0.0,
) -> pd.DataFrame:
    """
    Compare 10 key metrics between:
      - PDF extraction (DataFrame from process_document)
      - Spreadsheet (Excel/CSV bytes)

    Returns a DataFrame with:
      code, name, pdf_value, excel_value, difference, is_match
    """

    # PDF values: code -> amount_end_of_period
    pdf_metrics: Dict[str, Optional[float]] = {
        code: None for code in CODE_TO_NAME.keys()
    }
    pdf_metrics.update(build_pdf_metric_dict_from_df(balance_sheet_df))

    # Spreadsheet values: code -> excel_value (from earlier function)
    excel_metrics: Dict[str, Optional[float]] = parse_balance_sheet_spreadsheet(
        spreadsheet_bytes
    )

    rows = []

    for code, name in CODE_TO_NAME.items():
        pdf_value = pdf_metrics.get(code)
        excel_value = excel_metrics.get(code)

        difference = None
        is_match = None
        if pdf_value is not None and excel_value is not None:
            difference = excel_value - pdf_value
            is_match = abs(difference) <= tolerance

        rows.append(
            {
                "code": code,
                "name": name,
                "pdf_value": pdf_value,
                "excel_value": excel_value,
                "difference": difference,
                "is_match": is_match,
            }
        )

    return pd.DataFrame(
        rows,
        columns=["code", "name", "pdf_value", "excel_value", "difference", "is_match"],
    )

EMPTY_VALIDATION_DF = pd.DataFrame(
    columns=["code", "name", "pdf_value", "excel_value", "difference", "is_match"]
)

def validate_spreadsheet(balance_sheet_df, spreadsheet_file):
    """
    Wrapper for Gradio:
    - balance_sheet_df: whatever comes from gr.Dataframe (list or DataFrame)
    - spreadsheet_file: bytes from gr.File(type="binary")
    """
    df = pd.DataFrame(balance_sheet_df)  # safe for list-of-lists or DF

    if df.empty:
        return "Chưa có dữ liệu bảng cân đối để đối chiếu.", df

    if spreadsheet_file is None:
        return "Chưa chọn file Excel để đối chiếu.", df

    try:
        validation_df = validate_balance_sheet_against_spreadsheet(df, spreadsheet_file)

        # Map code -> excel_value / is_match
        code_series = validation_df["code"].astype(str)
        excel_map = dict(zip(code_series, validation_df["excel_value"]))
        match_map = dict(zip(code_series, validation_df["is_match"]))

        # Make sure we are mapping by "Mã số"
        codes = df["Mã số"].astype(str).str.strip()

        # New column: Số kiểm chứng
        df["Số kiểm chứng"] = codes.map(excel_map)

        # New column: Tình trạng (match / not match)
        def status_from_code(code: str) -> str:
            v = match_map.get(code)
            if v is True:
                return "✔ Khớp"
            if v is False:
                return "✘ Lệch"
            return ""

        df["Tình trạng"] = codes.map(status_from_code)

        mismatches = validation_df[validation_df["is_match"] == False].shape[0]
        status = f"Đã đối chiếu xong. Số chỉ tiêu lệch: {mismatches}."
        return status, df

    except Exception as e:
        return f"Lỗi khi đối chiếu: {e}", df