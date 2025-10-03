from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import date
from pydantic import BaseModel
from src.database2.schema.balance_sheet import BalanceSheetItemStandardizedORM, BalanceSheetAtEndOfPeriodORM
from src.database2.schema.balance_sheet import Base
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv(override=True)

DB_CONFIG = {
    "type": os.getenv("DB_TYPE")  # Options: 'sqlite', 'postgresql', 'mysql', etc.
    , "database_name": os.getenv("DB_DATABASE_NAME")
    , "username": os.getenv("DB_USERNAME")
    , "password": os.getenv("DB_PASSWORD")
    , "host": os.getenv("DB_HOST")
    , "port": os.getenv("DB_PORT")
}

def get_engine(config=DB_CONFIG):
    db_type = config["type"].lower()

    if db_type == "sqlite":
        db_url = f"sqlite:///{config['database_name']}"

    elif db_type == "postgresql":
        db_url = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config.get('port', 5432)}/{config['database_name']}"

    elif db_type == "mysql":
        db_url = f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config.get('port', 3306)}/{config['database_name']}"

    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return create_engine(db_url, echo=False)

def run_query(query: str, params: dict = None):
    """
    Run a raw SQL query and return results as list of dicts.
    """
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            rows = [dict(row._mapping) for row in result]
            return rows
    except SQLAlchemyError as e:
        print(f"Query failed: {e}")
        return []

def save_balance_sheet_to_db(
    company_name: str,
    stock_code: str,
    balance_sheet: BaseModel,
):
    """
    Saves company and balance sheet data to the database.

    Args:
        db: SQLAlchemy session
        company_name: Name of the company
        stock_code: Stock code (e.g., AAPL)
        balance_sheet: Instance of BalanceSheet Pydantic model
    """

    # Set up Engine & Session Factory
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    balance_sheet_item_dict = dict(
        db.query(BalanceSheetItemStandardizedORM.code,
                BalanceSheetItemStandardizedORM.name).all()
    )

    balance_sheet_data = {
        balance_sheet_item_dict[item.code]: item.amount_end_of_period
        for item in balance_sheet.balance_sheet_items
        if item.code in balance_sheet_item_dict
    }

    balance_sheet_data.update({
        "company_name": company_name,
        "stock_code": stock_code,
        "period_end_date": balance_sheet.period_end_date,
        "currency": balance_sheet.currency
    })

    try:
        existing_record = db.query(BalanceSheetAtEndOfPeriodORM).filter(
            BalanceSheetAtEndOfPeriodORM.period_end_date == balance_sheet.period_end_date,
            (BalanceSheetAtEndOfPeriodORM.company_name == company_name) | (BalanceSheetAtEndOfPeriodORM.stock_code == stock_code)
        ).first()

        if existing_record:
            for key, value in balance_sheet_data.items():
                setattr(existing_record, key, value)
            db.commit()
            db.refresh(existing_record)
            print(f"Updated balance sheet for {company_name} as of {balance_sheet.period_end_date}")
            return existing_record
        else:
            db_balance_sheet = BalanceSheetAtEndOfPeriodORM(**balance_sheet_data)
            db.add(db_balance_sheet)
            db.commit()
            db.refresh(db_balance_sheet)
            print(f"Saved balance sheet for {company_name} as of {balance_sheet.period_end_date}")
            return db_balance_sheet

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to save balance sheet: {e}")
        return None

def get_column_name_and_description(table_name):
    engine = get_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    
    return [
        (column["name"], column.get("comment", "") or "")
        for column in columns
    ]