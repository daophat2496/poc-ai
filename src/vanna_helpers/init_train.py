from src.vanna_helpers.init_vanna import get_vanna

def add_ddl():
    vn = get_vanna()
    ddl = """
    -- public.balance_sheets_at_end_of_period definition

    -- Drop table

    -- DROP TABLE public.balance_sheets_at_end_of_period;

    CREATE TABLE public.balance_sheets_at_end_of_period (
        id serial4 NOT NULL,
        company_name varchar(255) NOT NULL,
        stock_code varchar(20) NULL,
        period_end_date date NOT NULL,
        currency varchar(10) NULL,
        created_at timestamp DEFAULT now() NOT NULL,
        updated_at timestamp DEFAULT now() NOT NULL,
        short_term_assets numeric(20, 2) NULL,
        cash_and_cash_equivalents numeric(20, 2) NULL,
        cash numeric(20, 2) NULL,
        cash_equivalents numeric(20, 2) NULL,
        short_term_financial_investments numeric(20, 2) NULL,
        trading_securities numeric(20, 2) NULL,
        provision_for_decrease_in_value_of_trading_securities numeric(20, 2) NULL,
        short_term_investments_held_to_maturity numeric(20, 2) NULL,
        short_term_receivables numeric(20, 2) NULL,
        short_term_receivables_from_customers numeric(20, 2) NULL,
        prepayments_to_sellers_in_short_term numeric(20, 2) NULL,
        short_term_intercompany_receivables numeric(20, 2) NULL,
        receivables_according_to_the_progress_of_construction_com numeric(20, 2) NULL,
        short_term_loan_receivables numeric(20, 2) NULL,
        other_short_term_receivables numeric(20, 2) NULL,
        provision_for_uncollectible_short_term_receivables numeric(20, 2) NULL,
        shortage_of_assets_awaiting_resolution numeric(20, 2) NULL,
        inventories_total numeric(20, 2) NULL,
        inventories numeric(20, 2) NULL,
        provision_against_devaluation_of_goods_in_stock numeric(20, 2) NULL,
        other_short_term_assets_total numeric(20, 2) NULL,
        short_term_prepaid_expenses numeric(20, 2) NULL,
        deductible_vat numeric(20, 2) NULL,
        taxes_and_other_revenues_to_the_state numeric(20, 2) NULL,
        purchase_and_resale_of_government_bonds numeric(20, 2) NULL,
        other_short_term_assets numeric(20, 2) NULL,
        long_term_assets numeric(20, 2) NULL,
        long_term_receivables numeric(20, 2) NULL,
        long_term_receivables_from_customers numeric(20, 2) NULL,
        prepayments_to_suppliers_in_long_term numeric(20, 2) NULL,
        working_capital_provided_to_subordinate_units numeric(20, 2) NULL,
        long_term_intercompany_receivables numeric(20, 2) NULL,
        receivables_on_long_term_loans numeric(20, 2) NULL,
        other_long_term_receivables numeric(20, 2) NULL,
        provision_for_doubtful_long_term_receivables numeric(20, 2) NULL,
        fixed_assets numeric(20, 2) NULL,
        tangible_fixed_assets numeric(20, 2) NULL,
        tangible_fixed_assets_historical_costs numeric(20, 2) NULL,
        tangible_fixed_assets_value_of_accumulated_depreciation numeric(20, 2) NULL,
        finance_lease_fixed_asset numeric(20, 2) NULL,
        finance_lease_fixed_asset_historical_costs numeric(20, 2) NULL,
        finance_lease_fixed_asset_value_of_accumulated_depreciation numeric(20, 2) NULL,
        intangible_fixed_assets numeric(20, 2) NULL,
        intangible_fixed_assets_historical_costs numeric(20, 2) NULL,
        intangible_fixed_assets_value_of_accumulated_depreciation numeric(20, 2) NULL,
        investment_real_property numeric(20, 2) NULL,
        investment_real_property_historical_costs numeric(20, 2) NULL,
        investment_real_property_value_of_accumulated_depreciation numeric(20, 2) NULL,
        long_term_unfinished_assets numeric(20, 2) NULL,
        cost_of_long_term_work_in_progress numeric(20, 2) NULL,
        cost_of_construction_in_progress numeric(20, 2) NULL,
        long_term_financial_investments numeric(20, 2) NULL,
        investments_in_subsidiaries numeric(20, 2) NULL,
        investments_in_associated_companies_and_joint_ventures numeric(20, 2) NULL,
        investments_in_other_units numeric(20, 2) NULL,
        provisions_for_long_term_financial_investments numeric(20, 2) NULL,
        long_term_investments_held_to_maturity numeric(20, 2) NULL,
        other_long_term_assets_total numeric(20, 2) NULL,
        long_term_prepaid_expenses numeric(20, 2) NULL,
        deferred_income_tax_assets numeric(20, 2) NULL,
        long_term_equipment_supplies_and_spare_parts numeric(20, 2) NULL,
        other_long_term_assets numeric(20, 2) NULL,
        total_assets numeric(20, 2) NULL,
        liabilities numeric(20, 2) NULL,
        short_term_debt numeric(20, 2) NULL,
        short_term_supplier_payables numeric(20, 2) NULL,
        short_term_deferred_revenues numeric(20, 2) NULL,
        taxes_and_other_payables_to_state numeric(20, 2) NULL,
        payables_to_employees numeric(20, 2) NULL,
        short_term_expenses_payable numeric(20, 2) NULL,
        short_term_intercompany_payables numeric(20, 2) NULL,
        payables_according_to_the_progress_of_construction_contract numeric(20, 2) NULL,
        short_term_unearned_revenue numeric(20, 2) NULL,
        other_short_term_payables numeric(20, 2) NULL,
        short_term_loans_and_finance_lease_liabilities numeric(20, 2) NULL,
        provision_for_short_term_payables numeric(20, 2) NULL,
        bonus_and_welfare_fund numeric(20, 2) NULL,
        price_stabilization_fund numeric(20, 2) NULL,
        long_term_liabilities numeric(20, 2) NULL,
        long_term_supplier_payables numeric(20, 2) NULL,
        long_term_deferred_revenues numeric(20, 2) NULL,
        long_term_expenses_payable numeric(20, 2) NULL,
        intercompany_payables_on_working_capital numeric(20, 2) NULL,
        long_term_intercompany_payables numeric(20, 2) NULL,
        long_term_unearned_revenue numeric(20, 2) NULL,
        other_long_term_payables numeric(20, 2) NULL,
        long_term_loans_and_finance_lease_liabilities numeric(20, 2) NULL,
        convertible_bonds numeric(20, 2) NULL,
        long_term_liabilities_preference_shares numeric(20, 2) NULL,
        deferred_income_tax numeric(20, 2) NULL,
        provision_for_long_term_payables numeric(20, 2) NULL,
        scientific_and_technological_development_fund numeric(20, 2) NULL,
        owner_equity_total numeric(20, 2) NULL,
        owner_equity numeric(20, 2) NULL,
        contributions_from_owners numeric(20, 2) NULL,
        ordinary_shares_with_voting_rights numeric(20, 2) NULL,
        owner_equity_preference_shares numeric(20, 2) NULL,
        share_premium numeric(20, 2) NULL,
        conversion_options_on_bond numeric(20, 2) NULL,
        other_capital_of_owners numeric(20, 2) NULL,
        treasury_shares numeric(20, 2) NULL,
        differences_upon_asset_revaluation numeric(20, 2) NULL,
        exchange_differences numeric(20, 2) NULL,
        development_investment_funds numeric(20, 2) NULL,
        enterprise_reorganization_assistance_fund numeric(20, 2) NULL,
        other_equity_fund numeric(20, 2) NULL,
        undistributed_post_tax_profits numeric(20, 2) NULL,
        undistributed_post_tax_profits_accumulated_by_the_end_of_the_pr numeric(20, 2) NULL,
        undistributed_post_tax_profits_of_current_period numeric(20, 2) NULL,
        capital_expenditure_fund numeric(20, 2) NULL,
        funding_and_other_funds numeric(20, 2) NULL,
        funding numeric(20, 2) NULL,
        funds_that_form_fixed_assets numeric(20, 2) NULL,
        total_capital numeric(20, 2) NULL,
        CONSTRAINT balance_sheets_at_end_of_period_pkey PRIMARY KEY (id)
    );
    CREATE INDEX ix_balance_sheets_at_end_of_period_company_name ON public.balance_sheets_at_end_of_period USING btree (company_name);
    """
    vn.train(ddl=ddl)

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