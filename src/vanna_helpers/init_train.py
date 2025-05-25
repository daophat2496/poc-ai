from src.vanna_helpers.init_vanna import get_vanna

def add_ddl():
    vn = get_vanna()
    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
    plan = vn.get_training_plan_generic(df_information_schema)
    print(plan)
    vn.train(plan=plan)

def add_balance_sheet_end_of_period_introduction():
    vn = get_vanna()
    doc = """
    **Training Document for Vanna AI (RAG - Qdrant)**
    ---
    ### **Document Title:**  
    When to Use the "balance_sheets_at_end_of_period" Table
    ### **Summary:**  
    Use the `balance_sheets_at_end_of_period` table when the query relates to balance sheet data at the end of a reporting period.
    ---
    ### **Conditions for Using This Table:**
    1. **Topic Match:**  
    The question is about:
    - A balance sheet
    - Values or terms related to balance sheet items (e.g., assets, liabilities, equity)
    2. **Timeframe:**  
    - Refers to the balance sheet at the **end of a specific period**
    - Or does **not specify** a timeframe (default to latest available data)
    3. **Company Identification:**  
    - Extract and use the **stock code** if provided
    - If no stock code is present, use the **company name**
    4. **Period Date Handling:**  
    - If a **period date is specified**, filter using that date
    - If **no date is given**, retrieve the **latest record** by `period_date` from the database
    ---
    ### **Example Scenarios:**
    - *"What was Apple's total equity as of 2023-12-31?"*  
    → Use this table with company = Apple (AAPL), date = 2023-12-31

    - *"Show Microsoft's assets at the end of last year."*  
    → Use this table with company = Microsoft (MSFT), latest record for previous year

    - *"What is the current liability structure of Tesla?"*  
    → Use this table with company = Tesla (TSLA), latest period
    ---
    ### **Tag Keywords (for RAG indexing):**  
    `balance sheet`, `end of period`, `financial statement`, `assets`, `liabilities`, `equity`, `stock code`, `company name`, `period date`
    --- 
    This document is optimized for retrieval by Vanna AI using RAG (Qdrant). Keep it structured and keyword-rich for better semantic search performance.
    """

    vn.train(documentation=doc)

if __name__ == "__main__":
    add_ddl()
    add_balance_sheet_end_of_period_introduction()