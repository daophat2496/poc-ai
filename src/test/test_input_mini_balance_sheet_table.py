from datetime import date
from typing import Optional, Dict

from sqlalchemy.orm import Session

from src.core.balance_sheet import parse_balance_sheet_spreadsheet
from src.database2.schema.balance_sheet import BalanceSheetAtEndOfPeriodWithYearStartORM
from src.database2.schema.balance_sheet import BalanceSheetItemStandardizedORM


def to_snake_case(s: str) -> str:
    """Convert Vietnamese/English name to snake_case."""
    import re, unicodedata

    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_").lower()


def build_field_mapping(session: Session) -> Dict[str, str]:
    """
    Build dynamic map:
    code (e.g. '110') → ORM field_name (e.g. 'cash_and_cash_equivalents')
    based on BalanceSheetItemStandardizedORM.name
    """

    mapping = {}
    items = session.query(BalanceSheetItemStandardizedORM).all()

    for item in items:
        snake = to_snake_case(item.name)
        mapping[item.code] = snake

    return mapping


def upsert_mini_balance_sheet_from_spreadsheet(
    session: Session,
    spreadsheet_bytes: bytes,
    company_name: str,
    stock_code: Optional[str],
    period_end_date: date,
    currency: str = "VND",
) -> BalanceSheetAtEndOfPeriodWithYearStartORM:
    """
    excel_metrics is expected to be:
        Dict[str, list[float | None]]
        code -> [end_of_period, year_start]
    """

    # 1) Parse spreadsheet → {"code": [end_of_period, year_start]}
    excel_metrics: Dict[str, Any] = parse_balance_sheet_spreadsheet(spreadsheet_bytes)

    # 2) Build dynamic mapping: code → base ORM field
    code_to_field = build_field_mapping(session)

    # 3) Find or create row
    mini_obj = (
        session.query(BalanceSheetAtEndOfPeriodWithYearStartORM)
        .filter(
            BalanceSheetAtEndOfPeriodWithYearStartORM.company_name == company_name,
            BalanceSheetAtEndOfPeriodWithYearStartORM.stock_code == stock_code,
            BalanceSheetAtEndOfPeriodWithYearStartORM.period_end_date == period_end_date,
        )
        .one_or_none()
    )

    if mini_obj is None:
        mini_obj = BalanceSheetAtEndOfPeriodWithYearStartORM(
            company_name=company_name,
            stock_code=stock_code,
            period_end_date=period_end_date,
            currency=currency,
        )
        session.add(mini_obj)

    # 4) Fill metrics
    for code, raw_values in excel_metrics.items():
        if code not in code_to_field:
            continue

        base_field = code_to_field[code]

        # excel_metrics may return scalar or [eop, year_start]
        if isinstance(raw_values, (list, tuple)):
            end_of_period = raw_values[0] if len(raw_values) > 0 else None
            year_start = raw_values[1] if len(raw_values) > 1 else None
        else:
            end_of_period = raw_values
            year_start = None

        # End-of-period column
        if hasattr(mini_obj, base_field) and end_of_period is not None:
            setattr(mini_obj, base_field, end_of_period)

        # Year-start column (base_field + "_year_start")
        year_start_field = f"{base_field}_year_start"
        if hasattr(mini_obj, year_start_field) and year_start is not None:
            setattr(mini_obj, year_start_field, year_start)

    session.commit()
    session.refresh(mini_obj)

    return mini_obj

from datetime import date
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from src.database2.database_helpers import get_engine

engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def process_excel_to_mini_bs(
    file_path: str,
    company_name: str,
    stock_code: str,
    period_end: date,
):
    # 1. Load Excel file bytes
    with open(file_path, "rb") as f:
        spreadsheet_bytes = f.read()

    # 2. Open DB session
    session: Session = SessionLocal()

    try:
        # 3. Call your upsert function
        result = upsert_mini_balance_sheet_from_spreadsheet(
            session=session,
            spreadsheet_bytes=spreadsheet_bytes,
            company_name=company_name,
            stock_code=stock_code,
            period_end_date=period_end,
        )

        print("Inserted/Updated Mini Balance Sheet:")
        print(result)

    finally:
        session.close()


# ==== Usage example ====

if __name__ == "__main__":
    process_excel_to_mini_bs(
        file_path="C:/Users/Phat Dao/Downloads/POC AI/HAF/DN - BẢNG CÂN ĐỐI KẾ TOÁN (2).xls",
        company_name="Công ty Cổ phần Thực phẩm Hà Nội",
        stock_code="HAF",
        period_end=date(2024, 12, 31),
    )