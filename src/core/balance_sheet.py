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
from src.database2.database_helpers import get_engine, save_balance_sheet_to_db, save_balance_sheet_year_start_to_db
from src.core.model import model
from src.core.util import verify_balance_sheet_sums
from src.database2.database_helpers import run_query
import shutil
import pandas as pd
from typing import Dict, Optional
from uuid import uuid4
from datetime import datetime
from decimal import Decimal

UPLOAD_DIR = "uploads"

def pdf_to_images(pdf_path: str, output_root="image"):
    """
    Convert a PDF into images inside:
        image/<pdf_name_without_ext>/image_001.jpg
    No deletion of parent folders.
    """

    os.makedirs(output_root, exist_ok=True)

    # Get clean name: remove extension but KEEP timestamp
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Create folder: image/<pdf_name>/
    output_folder = os.path.join(output_root, pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF → images
    images = convert_from_path(pdf_path, dpi=100)

    for i, image in enumerate(images, start=1):
        img_path = os.path.join(output_folder, f"image_{i:03d}.jpg")
        image.save(img_path, "JPEG")
        # print("Saved image:", img_path)

    return output_folder

def encode_image(image_path):
    image = Image.open(image_path).convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def query_model_with_image_b64(image_b64_list, prompt, structure: BaseModel = None, system_message = None, stream: bool = False):
    messages = []
    
    # Add system message if provided
    if system_message:
        messages.append(SystemMessage(
            content=[{"type": "text", "text": system_message}
                        , {"type": "text", "text": "Give the answer only. No explanation. No reasoning."}
                    ]
        ))
    else:
        messages.append(SystemMessage(
            content=[{"type": "text", "text": "Give the answer only. No explanation. No reasoning."}]
        ))

    human_message = HumanMessage(
        content=[{"type": "text", "text": prompt}]
    )

    for image_b64 in image_b64_list:
        human_message.content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}})
    
    messages.append(human_message)

    if not structure:
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

    return model.with_structured_output(structure, method="function_calling").invoke(messages)

def is_affirmative_response(response: str) -> bool:
    """Check if the input response is "Yes" for "ONLY answer 'Yes' or 'No'" prompt"""
    return "yes" in response.strip().lower()

def format_number(num):
    if isinstance(num, (int, float, Decimal)):
        return f"{num:,.0f}".replace(",", ".")
    return num

def process_document(file_path: str):
    if not file_path:
        return "No file uploaded", "", "", "", "", pd.DataFrame()
    
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
        balance_sheet_page_paths = []
        # results = []

        # Ensure uploads folder exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        original_name = os.path.basename(file_path)
        base, ext = os.path.splitext(original_name)
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{base}_{ts}{ext}"
        saved_path = os.path.join(UPLOAD_DIR, new_filename)
        shutil.copy(file_path, saved_path)
        print(f"Saved upload to: {saved_path}")


        # Save the uploaded file temporarily
        # temp_pdf_name = str(uuid4())
        # temp_pdf_path = f"{temp_pdf_name}.pdf"
        # with open(temp_pdf_path, "wb") as f:
        #     f.write(file)

        images_folder = pdf_to_images(saved_path)

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
                    balance_sheet_page_paths.append(page_path)
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
        save_balance_sheet_year_start_to_db(company_name, stock_code, balance_sheet)

        # Clean up
        # os.remove(temp_pdf_path)
        # shutil.rmtree(images_folder)

        df = pd.DataFrame(
            balance_sheet_item_list,
            columns=["Mã số", "Mục", "Số liệu cuối kỳ", "Số liệu đầu năm"]
        )
        # Apply formatting to the numeric columns
        df["Số liệu cuối kỳ"] = df["Số liệu cuối kỳ"].apply(format_number)
        df["Số liệu đầu năm"] = df["Số liệu đầu năm"].apply(format_number)

        #### Checksum
        status = ""
        if verify_balance_sheet_sums(all_balance_sheet_items):
            status = "Trạng thái: 🟢 Xử lý thành công. 🟢 Đối chiếu tổng khớp."
        else:
            status = "Trạng thái: 🟢 Xử lý thành công. 🔴 Đối chiếu tổng chưa khớp."

        return (
            status
            , company_name
            , stock_code
            , balance_sheet.period_end_date.strftime("%Y-%m-%d")
            , balance_sheet.currency
            , df
            , balance_sheet_page_paths
        )
    
    except Exception as e:
        print(str(e))
        return (
            f"Trạng thái: 🔴 Xử lý không thành công. - {str(e)}"
            , "", "", "", ""
            , pd.DataFrame(columns=["Mã số", "Mục", "Số liệu cuối kỳ", "Số liệu đầu năm"])
            , []
        )

def get_balance_sheets_general_info():
    query = """SELECT
    company_name AS "Công ty"
    , stock_code AS "Mã"
    , period_end_date AS "Kỳ báo cáo"
    , cash_and_cash_equivalents AS "Tiền và các khoản tương đương tiền"
    , short_term_receivables AS "Tài sản ngắn hạn"
    , inventories_total AS "Hàng tồn kho"
    , long_term_assets AS "Tài sản dài hạn"
    , total_assets AS "Tổng tài sản"
    , liabilities AS "Nợ phải trả"
    , short_term_debt AS "Nợ ngắn hạn"
    , long_term_liabilities AS "Nợ dài hạn"
    , owner_equity AS "Vốn chủ sở hữu"
    , contributions_from_owners AS "Vốn thực góp của chủ sở hữu"
    , undistributed_post_tax_profits AS "Lợi nhuận sau thuế chưa phân phối"
    , total_capital AS "Tổng nguồn vốn"
    , total_profit AS "Tổng lợi nhuận"
    , total_profit_after_tax AS "Lợi nhuận sau thuế"
FROM mini_balance_sheets_at_end_of_period_with_year_start 
ORDER BY stock_code, period_end_date DESC"""

    rows = run_query(query)  # returns list of dict
    df = pd.DataFrame(rows)  # convert to dataframe

    # optional: format dates nicely
    if "Kỳ báo cáo" in df.columns:
        df["Kỳ báo cáo"] = pd.to_datetime(df["Kỳ báo cáo"]).dt.strftime("%d/%m/%Y")
    if "Cập nhật lúc" in df.columns:
        df["Cập nhật lúc"] = pd.to_datetime(df["Cập nhật lúc"]).dt.strftime("%d/%m/%Y %H:%M")

    # --- Apply format_number to ALL numeric columns except excluded ones ---
    exclude = {"Công ty", "Mã", "Kỳ báo cáo"}

    for col in df.columns:
        # print(f"Column: {col}")
        if col not in exclude:
            df[col] = df[col].apply(format_number)

    return df

def parse_balance_sheet_spreadsheet(file_bytes: bytes) -> Dict[str, list[float | None]]:
    """
    Parse the uploaded spreadsheet (Excel/CSV) and return a mapping:
        { balance_sheet_code (str): value_from_spreadsheet (float or None) }

    New template:
    - Use column "Mã chỉ tiêu" as the code
    - Use column "Số cuối kỳ" as the value
    - Scan all rows and keep ALL codes found in the sheet
    """

    buffer = BytesIO(file_bytes)

    # First load raw
    try:
        buffer.seek(0)
        df_raw = pd.read_excel(buffer, header=None)
    except Exception as e:
        raise ValueError(
            f"Không đọc được file Excel."
            f"Hãy chắc chắn file là .xls hoặc .xlsx"
            f"Chi tiết: {e}"
        )

    if df_raw.empty:
        return {}

    # detect header row (search first 20 rows)
    header_row = None
    for i in range(min(20, len(df_raw))):
        row_values = [str(v).strip().lower() for v in df_raw.iloc[i].tolist()]
        if "mã chỉ tiêu" in row_values and "số cuối kỳ" in row_values:
            header_row = i
            break

    if header_row is None:
        return {}

    # re-read the file with correct header row
    buffer.seek(0)
    try:
        df = pd.read_excel(buffer, header=header_row)
    except Exception:
        buffer.seek(0)
        df = pd.read_csv(buffer, header=header_row)

    # normalize headers
    df.columns = [str(c).strip() for c in df.columns]

    CODE_HEADER = "Mã chỉ tiêu"
    VALUE_HEADER = "Số cuối kỳ"
    VALUE_HEADER_START_YEAR = "Số đầu năm"

    result: Dict[str, list[float | None]] = {}

    for _, row in df.iterrows():
        raw_code = row.get(CODE_HEADER)
        if pd.isna(raw_code):
            continue

        code = str(raw_code).strip()
        if not code:
            continue

        raw_value = row.get(VALUE_HEADER)
        numeric_value = _parse_numeric(raw_value)

        raw_value_start_year = row.get(VALUE_HEADER_START_YEAR)
        numeric_value_start_year = _parse_numeric(raw_value_start_year)

        result[code] = [numeric_value, numeric_value_start_year]

    return result

# Use for POC, will refactor later
# CODE_TO_NAME = {
#     "110": "cash_and_cash_equivalents",
#     "111": "cash",
#     "112": "cash_equivalents",
#     "140": "inventories_total",
#     "141": "inventories",
#     "270": "total_assets",
#     "300": "liabilities",
#     "400": "owner_equity_total",
#     "410": "owner_equity",
#     "440": "total_capital",
# }

def _parse_numeric(value):
    if value is None:
        return None

    s = str(value).strip()
    if not s:
        return None

    # ----- CASE 1: Dot-grouped integer like 222.104.376 or -222.104.376 -----
    # Pattern: digits and dots only, possibly starting with '-'
    import re
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):
        # Treat as thousand separators
        return float(s.replace(".", ""))

    # ----- CASE 2: Normal decimal or integer (e.g., 123.0, -456.7) -----
    try:
        return float(s)
    except ValueError:
        pass

    # ----- CASE 3: Remove commas (Excel export) -----
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def build_pdf_metric_dict_from_df(df: pd.DataFrame) -> Dict[str, list[float | None]]:
    metrics: Dict[str, list[float | None]] = {}

    if df is None or df.empty:
        return metrics

    for _, row in df.iterrows():
        code = str(row.get("Mã số", "")).strip()
        if not code:
            continue

        pdf_end = _parse_numeric(row.get("Số liệu cuối kỳ"))
        pdf_start = _parse_numeric(row.get("Số liệu đầu năm"))

        metrics[code] = [pdf_end, pdf_start]

    return metrics


def validate_balance_sheet_against_spreadsheet(
    balance_sheet_df: pd.DataFrame,
    spreadsheet_bytes: bytes,
    tolerance: float = 0.0,
) -> pd.DataFrame:

    pdf_metrics = build_pdf_metric_dict_from_df(balance_sheet_df)
    excel_metrics = parse_balance_sheet_spreadsheet(spreadsheet_bytes)

    # Lookup names
    name_lookup = {
        str(row["Mã số"]).strip(): str(row["Mục"]).strip()
        for _, row in balance_sheet_df.iterrows()
        if str(row.get("Mã số", "")).strip()
    }

    # union of codes
    all_codes = sorted(set(pdf_metrics) | set(excel_metrics))

    rows = []

    for code in all_codes:
        name = name_lookup.get(code, "")

        # SAFE GET → ALWAYS returns a list of 2 items
        pdf_vals = pdf_metrics.get(code, [None, None])
        excel_vals = excel_metrics.get(code, [None, None])

        pdf_end, pdf_start = pdf_vals
        excel_end, excel_start = excel_vals

        # --- END OF PERIOD ---
        diff_end = None
        is_match_end = None
        if pdf_end is not None and excel_end is not None:
            diff_end = excel_end - pdf_end
            is_match_end = abs(diff_end) <= tolerance
        
        if not is_match_end:
            print(f"Excel value: {excel_end}")
            print(f"PDF value: {pdf_end}")

        # --- START OF YEAR ---
        diff_start = None
        is_match_start = None
        if pdf_start is not None and excel_start is not None:
            diff_start = excel_start - pdf_start
            is_match_start = abs(diff_start) <= tolerance

        if not is_match_start:
            print(f"Excel value: {excel_start}")
            print(f"PDF value: {pdf_start}")

        rows.append({
            "code": code,
            "name": name,
            "pdf_value": pdf_end,
            "excel_value": excel_end,
            "difference": diff_end,
            "is_match": is_match_end,
            "excel_value_start_year": excel_start,
            "difference_start_year": diff_start,
            "is_match_start_year": is_match_start,
        })

    return pd.DataFrame(rows)

EMPTY_VALIDATION_DF = pd.DataFrame(
    columns=["code", "name", "pdf_value", "excel_value", "difference", "is_match", "excel_value_start_year", "difference_start_year", "is_match_start_year"]
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

        # Safety: if validate_balance_sheet_against_spreadsheet returns None or empty
        if validation_df is None or validation_df.empty:
            return "Không tìm thấy dữ liệu hợp lệ để đối chiếu trong file Excel.", df

        # Map code -> excel_value / is_match
        code_series = validation_df["code"].astype(str)

        # Main period (cuối kỳ)
        excel_value_series = validation_df.get("excel_value")
        is_match_series = validation_df.get("is_match")

        excel_map = dict(zip(code_series, excel_value_series)) if excel_value_series is not None else {}
        match_map = dict(zip(code_series, is_match_series)) if is_match_series is not None else {}

        # Start-year (đầu năm) – optional, chỉ dùng nếu có cột
        excel_start_series = validation_df.get("excel_value_start_year")
        match_start_series = validation_df.get("is_match_start_year")

        excel_map_start_year = (
            dict(zip(code_series, excel_start_series)) if excel_start_series is not None else {}
        )
        match_map_start_year = (
            dict(zip(code_series, match_start_series)) if match_start_series is not None else {}
        )

        # Make sure we are mapping by "Mã số"
        codes = df["Mã số"].astype(str).str.strip()

        def with_icon(value, is_match):
            if value is None:
                return ""
            icon = ""
            if is_match is True:
                icon = "🟢 "
            elif is_match is False:
                icon = "🔴 "
            return icon + format_number(value)

        # 🔹 Số kiểm chứng (cuối kỳ) – chèn icon trực tiếp, KHÔNG thêm cột Tình trạng
        df["Số kiểm chứng"] = codes.map(
            lambda c: with_icon(excel_map.get(c), match_map.get(c))
        )

        # 🔹 Số kiểm chứng đầu năm (nếu có dữ liệu đầu năm)
        if excel_map_start_year:
            df["Số kiểm chứng đầu năm"] = codes.map(
                lambda c: with_icon(
                    excel_map_start_year.get(c),
                    match_map_start_year.get(c),
                )
            )

        # Đếm số chỉ tiêu lệch (cả cuối kỳ + đầu năm nếu có)
        mismatches_end = sum(1 for v in match_map.values() if v is False)
        mismatches_start = sum(1 for v in match_map_start_year.values() if v is False)
        mismatches = mismatches_end + mismatches_start

        status = f"Đã đối chiếu xong. Số chỉ tiêu lệch: {mismatches}."

        # --- Reorder table columns ---
        desired_order = [
            "Mã số",
            "Mục",
            "Số liệu cuối kỳ",
            "Số kiểm chứng",
            "Số liệu đầu năm",
            "Số kiểm chứng đầu năm",
        ]

        df = df[[c for c in desired_order if c in df.columns]]
        return status, df

    except Exception as e:
        return f"Lỗi khi đối chiếu: {e}", df