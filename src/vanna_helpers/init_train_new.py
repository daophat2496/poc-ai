from src.vanna_helpers.init_vanna import get_vanna

def add_column_name_list():
    vn = get_vanna()
    doc = """**IMPORTANT** Only use this set of columns in query generated, this is list of columns in balance_sheets_at_end_of_period table
id | company_name | stock_code | period_end_date | currency | created_at | updated_at | cash_and_cash_equivalents | short_term_receivables | inventories_total | other_short_term_assets_total | long_term_assets | total_assets | liabilities | short_term_debt | long_term_liabilities | long_term_liabilities_preference_shares | owner_equity_total | total_capital"""

    vn.add_documentation(documentation=doc)

def add_column_description():
    vn = get_vanna()
    doc = """Column name list and their description in *mini_balance_sheets_at_end_of_period_with_year_start* table, use this table for query:
id: system id for company (do not use in response)
company_name: name for the company
stock_code: stock code of the company
period_end_date: date of the balance sheet
currency: currency use in the balance sheet
cash_and_cash_equivalents: Tiền và các khoản tương đương tiền
short_term_receivables: Tài sản ngắn hạn
inventories_total: Hàng tồn kho
long_term_assets: Tài sản dài hạn
total_assets: Tổng tài sản
liabilities: Nợ phải trả
short_term_debt: Nợ ngắn hạn
long_term_liabilities: Nợ dài hạn
owner_equity: Vốn chủ sở hữu
contributions_from_owners: Vốn góp của chủ sở hữu
undistributed_post_tax_profits: Lợi nhuận sau thuế chưa phân phối
total_capital: Tổng nguồn vốn
total_profit: Tổng lợi nhuận
total_profit_after_tax: Lợi nhuận sau thuế
cash_and_cash_equivalents_year_start: Tiền và các khoản tương đương tiền vào đầu năm
short_term_receivables_year_start: Tài sản ngắn hạn vào đầu năm
inventories_total_year_start: Hàng tồn kho vào đầu năm
long_term_assets_year_start: Tài sản dài hạn vào đầu năm
total_assets_year_start: Tổng tài sản vào đầu năm
liabilities_year_start: Nợ phải trả vào đầu năm
short_term_debt_year_start: Nợ ngắn hạn vào đầu năm
long_term_liabilities_year_start: Nợ dài hạn vào đầu năm
owner_equity_year_start: Vốn chủ sở hữu vào đầu năm
contributions_from_owners_year_start: Vốn góp của chủ sở hữu vào đầu năm
undistributed_post_tax_profits_year_start: Lợi nhuận sau thuế chưa phân phối vào đầu năm
total_capital_year_start: Tổng nguồn vốn vào đầu năm
total_profit_year_start: Tổng lợi nhuận vào đầu năm
total_profit_after_tax_year_start: Lợi nhuận sau thuế vào đầu năm"""

    vn.train(documentation=doc)

def add_ddl():
    vn = get_vanna()
    ddl = """ -- ONLY USE THESE COLUMNS FOR QUERY
CREATE TABLE public.balance_sheets_at_end_of_period (
	id serial4 NOT NULL,
	company_name varchar(255) NOT NULL,
	stock_code varchar(20) NULL,
	period_end_date date NOT NULL,
	currency varchar(10) NULL,
	created_at timestamp DEFAULT now() NOT NULL,
	updated_at timestamp DEFAULT now() NOT NULL,
	cash_and_cash_equivalents numeric(20, 2) NULL,
	short_term_receivables numeric(20, 2) NULL,
	inventories_total numeric(20, 2) NULL,
	other_short_term_assets_total numeric(20, 2) NULL,
	long_term_assets numeric(20, 2) NULL,
	total_assets numeric(20, 2) NULL,
	liabilities numeric(20, 2) NULL,
	short_term_debt numeric(20, 2) NULL,
	long_term_liabilities numeric(20, 2) NULL,
	long_term_liabilities_preference_shares numeric(20, 2) NULL,
	owner_equity_total numeric(20, 2) NULL,
	total_capital numeric(20, 2) NULL,
	CONSTRAINT balance_sheets_at_end_of_period_pkey PRIMARY KEY (id)
);
);"""
    vn.train(ddl=ddl)

def add_balance_sheet_end_of_period_introduction():
    vn = get_vanna()
    doc = """
    VannaAI Training Document: balance_sheets_at_end_of_period Table
    Table Purpose:
    Use balance_sheets_at_end_of_period for queries about balance sheet data at period-end dates from PDF financial statements.
    Query Classification Rules:
    When to Use This Table:
    Balance Sheet Indicators:

    Direct mentions: balance sheet, statement of financial position
    Balance sheet components: assets, liabilities, equity, shareholders equity
    Specific line items: cash, inventory, accounts payable, retained earnings, etc.
    Financial ratios requiring balance sheet data: debt-to-equity, current ratio, book value

    Temporal Context:
    As of date or at date
    End of period/quarter/year
    No timeframe specified (use latest available)

    Company Identification Logic:
    Use OR statement to check both stock_code and company_name with lowercase conversion:
    Company identification pattern:
    WHERE (LOWER(stock_code) = LOWER(?) OR LOWER(company_name) LIKE LOWER(?))
    Examples:
    WHERE (LOWER(stock_code) = 'aapl' OR LOWER(company_name) LIKE '%aapl%')
    WHERE (LOWER(stock_code) = 'msft' OR LOWER(company_name) LIKE '%msft%')
    WHERE (LOWER(stock_code) = 'tsla' OR LOWER(company_name) LIKE '%tsla%')
    For partial matches, use LIKE with wildcards:
    WHERE (LOWER(stock_code) = 'googl' OR LOWER(company_name) LIKE '%googl%')
    WHERE (LOWER(stock_code) = 'meta' OR LOWER(company_name) LIKE '%meta%')
    Implementation Notes:
    Always convert both input and database values to lowercase
    Use exact match (=) for stock_code
    Use LIKE with wildcards (%) for company_name to handle partial matches
    Input preprocessing: strip whitespace and convert to lowercase before query

    Invalid date: Use closest available period_end_date"""

    vn.train(documentation=doc)

def add_company_query():
    vn = get_vanna()
    doc = """
VannaAI: Company identification pattern

Use this WHERE clause for company queries:
WHERE (LOWER(stock_code) = LOWER('code') OR LOWER(company_name) LIKE LOWER('%' || 'code' || '%'))

Examples:
- AAPL: WHERE (LOWER(stock_code) = 'aapl' OR LOWER(company_name) LIKE '%aapl%')
- Microsoft: WHERE (LOWER(stock_code) = 'microsoft' OR LOWER(company_name) LIKE '%microsoft%')

Rules: Always lowercase, exact match for stock_code, partial match for company_name
"""

    vn.train(documentation=doc)

def add_coalesce_for_total_doc():
    vn = get_vanna()
    doc = """VannaAI: Total calculation pattern

When calculating totals, always use COALESCE to handle NULL values:
field1 + field2 => COALESCE(field1, 0) + COALESCE(field2, 0)

Examples:
- Total debt: COALESCE(short_term_debt, 0) + COALESCE(long_term_liabilities, 0)
- Total assets: COALESCE(short_term_assets, 0) + COALESCE(fixed_assets, 0)

Rule: Wrap each field in COALESCE(field, 0) to prevent NULL results"""
    vn.train(documentation=doc)

if __name__ == "__main__":
    add_column_description()
    # add_column_name_list()
    # add_company_query()
    # add_ddl()
    # # add_balance_sheet_end_of_period_introduction()
    # # add_column_description()
    # add_coalesce_for_total_doc()