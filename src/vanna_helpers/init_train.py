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
    Comparative requests: compare 2023 vs 2022 balance sheet

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

    Table: balance_sheets_at_end_of_period
    Filter: (LOWER(stock_code) = 'aapl' OR LOWER(company_name) LIKE '%aapl%') AND period_end_date = '2023-12-31'
    Field: total_assets

    Example 2: Show Tesla's current liabilities

    Table: balance_sheets_at_end_of_period
    Filter: (LOWER(stock_code) = 'tsla' OR LOWER(company_name) LIKE '%tsla%') AND latest period_end_date
    Field: current_liabilities

    Error Handling:

    Invalid date: Use closest available period_end_date
    No data found: Suggest alternative timeframes or company variations

    RAG Keywords:
    balance_sheet, financial_position, assets, liabilities, equity, shareholders_equity, period_end, quarterly, annual, cash, debt, retained_earnings, current_ratio, book_value, financial_statement, PDF_extraction
    """

    vn.train(documentation=doc)

def add_column_description():
    vn = get_vanna()
    doc = """
    Columns' description: balance_sheets_at_end_of_period table

    short_term_assets: Total value of all current assets expected to be converted to cash within one year | Tổng giá trị tất cả tài sản ngắn hạn dự kiến chuyển đổi thành tiền trong vòng một năm    
    cash_and_cash_equivalents: Highly liquid assets including cash and short-term investments | Tài sản có tính thanh khoản cao bao gồm tiền mặt và các khoản đầu tư ngắn hạn
    cash: Physical currency, coins, and balances in checking accounts | Tiền mặt vật lý, tiền xu và số dư trong tài khoản séc
    cash_equivalents: Short-term, highly liquid investments that are readily convertible to cash | Các khoản đầu tư ngắn hạn, có tính thanh khoản cao dễ dàng chuyển đổi thành tiền mặt
    short_term_financial_investments: Investments intended to be held for less than one year | Các khoản đầu tư tài chính dự định nắm giữ dưới một năm
    trading_securities: Securities bought and held principally for selling in the near term | Chứng khoán mua và nắm giữ chủ yếu để bán trong thời gian ngắn
    provision_for_decrease_in_value_of_trading_securities: Allowance for potential loss in value of trading securities | Dự phòng cho khoản lỗ tiềm tàng về giá trị của chứng khoán kinh doanh       
    short_term_investments_held_to_maturity: Debt securities the company intends to hold until maturity and are due within one year | Chứng khoán nợ mà công ty dự định nắm giữ đến ngày đáo hạn và có thời hạn dưới một năm
    short_term_receivables: Amounts expected to be received within one year | Các khoản dự kiến sẽ nhận được trong vòng một năm
    short_term_receivables_from_customers: Amounts owed by customers that are due within one year | Các khoản khách hàng nợ đến hạn trong vòng một năm
    prepayments_to_sellers_in_short_term: Advance payments made to suppliers for goods or services to be received within one year | Thanh toán trước cho nhà cung cấp đối với hàng hóa hoặc dịch vụ sẽ nhận được trong vòng một năm
    short_term_intercompany_receivables: Amounts owed to the company by related entities within one year | Các khoản các thực thể liên quan nợ công ty trong vòng một năm
    receivables_according_to_the_progress_of_construction_com: Amounts receivable based on percentage of completion of construction contracts | Các khoản phải thu theo tiến độ hoàn thành hợp đồng xây dựng
    short_term_loan_receivables: Short-term loans made to others that are due within one year | Các khoản cho vay ngắn hạn đến hạn trong vòng một năm
    other_short_term_receivables: Other amounts due to the company within one year not elsewhere classified | Các khoản phải thu ngắn hạn khác không được phân loại ở nơi khác
    provision_for_uncollectible_short_term_receivables: Allowance for doubtful short-term receivables | Dự phòng cho các khoản phải thu ngắn hạn khó đòi
    shortage_of_assets_awaiting_resolution: Shortages of assets that are pending investigation and resolution | Thiếu hụt tài sản đang chờ điều tra và giải quyết
    inventories_total: Total value of goods held for sale or in production | Tổng giá trị hàng hóa nắm giữ để bán hoặc trong sản xuất
    inventories: Raw materials, work in progress and finished goods | Nguyên liệu, sản phẩm dở dang và thành phẩm
    provision_against_devaluation_of_goods_in_stock: Allowance for potential loss in value of inventory | Dự phòng giảm giá hàng tồn kho
    other_short_term_assets_total: Total of other current assets not elsewhere classified | Tổng các tài sản ngắn hạn khác không được phân loại ở nơi khác
    short_term_prepaid_expenses: Expenses paid in advance that will be recognized within one year | Chi phí trả trước sẽ được ghi nhận trong vòng một năm
    deductible_vat: Value added tax that can be deducted | Giá trị gia tăng được khấu trừ
    taxes_and_other_revenues_to_the_state: Taxes and other amounts payable to government authorities | Thuế và các khoản khác phải nộp nhà nước
    purchase_and_resale_of_government_bonds: Government bonds purchased for resale | Trái phiếu chính phủ mua để bán lại
    other_short_term_assets: Other current assets not elsewhere specified | Các tài sản ngắn hạn khác không được chỉ định ở nơi khác
    long_term_assets: Assets that provide value for more than one year | Tài sản cung cấp giá trị trong hơn một năm
    long_term_receivables: Amounts expected to be received after one year | Các khoản dự kiến sẽ nhận được sau một năm
    long_term_receivables_from_customers: Amounts owed by customers that are due after one year | Các khoản khách hàng nợ đến hạn sau một năm
    prepayments_to_suppliers_in_long_term: Advance payments made to suppliers for goods or services to be received after one year | Thanh toán trước cho nhà cung cấp đối với hàng hóa hoặc dịch vụ sẽ nhận được sau một năm
    working_capital_provided_to_subordinate_units: Capital provided to subsidiaries and affiliates | Vốn lưu động cung cấp cho các đơn vị trực thuộc
    long_term_intercompany_receivables: Amounts owed to the company by related entities after one year | Các khoản các thực thể liên quan nợ công ty sau một năm
    receivables_on_long_term_loans: Long-term loans made to others | Các khoản cho vay dài hạn cho bên khác
    other_long_term_receivables: Other amounts due to the company after one year not elsewhere classified | Các khoản phải thu dài hạn khác không được phân loại ở nơi khác
    provision_for_doubtful_long_term_receivables: Allowance for doubtful long-term receivables | Dự phòng cho các khoản phải thu dài hạn khó đòi
    fixed_assets: Long-term tangible and intangible assets used in operations | Tài sản hữu hình và vô hình dài hạn sử dụng trong hoạt động
    tangible_fixed_assets: Physical assets used in operations | Tài sản cố định hữu hình
    tangible_fixed_assets_historical_costs: Original acquisition cost of tangible fixed assets | Nguyên giá tài sản cố định hữu hình
    tangible_fixed_assets_value_of_accumulated_depreciation: Total depreciation accumulated on tangible fixed assets | Giá trị hao mòn lũy kế tài sản cố định hữu hình
    finance_lease_fixed_asset: Assets acquired under finance lease arrangements | Tài sản thuê tài chính
    finance_lease_fixed_asset_historical_costs: Original cost of finance leased assets | Nguyên giá tài sản thuê tài chính
    finance_lease_fixed_asset_value_of_accumulated_depreciation: Total depreciation accumulated on finance leased assets | Giá trị hao mòn lũy kế tài sản thuê tài chính
    intangible_fixed_assets: Non-physical assets with long-term value | Tài sản cố định vô hình
    intangible_fixed_assets_historical_costs: Original acquisition cost of intangible fixed assets | Nguyên giá tài sản cố định vô hình
    intangible_fixed_assets_value_of_accumulated_depreciation: Total amortization accumulated on intangible fixed assets | Giá trị hao mòn lũy kế tài sản cố định vô hình
    investment_real_property: Real estate held for investment purposes | Bất động sản đầu tư
    investment_real_property_historical_costs: Original acquisition cost of investment property | Nguyên giá bất động sản đầu tư
    investment_real_property_value_of_accumulated_depreciation: Total depreciation accumulated on investment property | Giá trị hao mòn lũy kế bất động sản đầu tư
    long_term_unfinished_assets: Assets under construction or development | Tài sản dở dang dài hạn
    cost_of_long_term_work_in_progress: Costs incurred for long-term projects not yet completed | Chi phí cho các dự án dài hạn chưa hoàn thành
    cost_of_construction_in_progress: Costs incurred for construction projects not yet completed | Chi phí xây dựng dở dang
    long_term_financial_investments: Investments intended to be held for more than one year | Đầu tư tài chính dài hạn
    investments_in_subsidiaries: Investments in companies where the parent has control | Đầu tư vào công ty con
    investments_in_associated_companies_and_joint_ventures: Investments in companies where the investor has significant influence | Đầu tư vào công ty liên kết và liên doanh
    investments_in_other_units: Other long-term equity investments | Đầu tư vào các đơn vị khác
    provisions_for_long_term_financial_investments: Allowance for potential loss on long-term investments | Dự phòng giảm giá đầu tư tài chính dài hạn
    long_term_investments_held_to_maturity: Debt securities the company intends to hold until maturity and are due after one year | Chứng khoán nợ mà công ty dự định nắm giữ đến ngày đáo hạn và có 
    thời hạn trên một năm
    other_long_term_assets_total: Total of other non-current assets not elsewhere classified | Tổng các tài sản dài hạn khác không được phân loại ở nơi khác
    long_term_prepaid_expenses: Expenses paid in advance that will be recognized after one year | Chi phí trả trước dài hạn
    deferred_income_tax_assets: Taxes paid in advance or tax benefits to be realized in future periods | Tài sản thuế thu nhập hoãn lại
    long_term_equipment_supplies_and_spare_parts: Long-term inventory of equipment and spare parts | Vật tư, phụ tùng thay thế dài hạn
    other_long_term_assets: Other non-current assets not elsewhere specified | Tài sản dài hạn khác
    total_assets: Sum of all assets | Tổng tài sản
    liabilities: Total obligations owed to external parties including both short-term and long-term debts | Tổng các khoản nợ phải trả cho bên ngoài bao gồm nợ ngắn hạn và dài hạn
    short_term_debt: Obligations due within one year | Nợ ngắn hạn
    short_term_supplier_payables: Amounts owed to suppliers due within one year | Phải trả người bán ngắn hạn
    short_term_deferred_revenues: Payments received in advance for services to be provided within one year | Doanh thu chưa thực hiện ngắn hạn
    taxes_and_other_payables_to_state: Taxes and other amounts payable to government within one year | Thuế và các khoản phải nộp nhà nước ngắn hạn
    payables_to_employees: Wages and benefits owed to employees | Phải trả người lao động
    short_term_expenses_payable: Accrued expenses to be paid within one year | Chi phí phải trả ngắn hạn
    short_term_intercompany_payables: Amounts owed to related entities within one year | Phải trả nội bộ ngắn hạn
    payables_according_to_the_progress_of_construction_contract: Amounts payable based on percentage of completion of construction contracts | Phải trả theo tiến độ hợp đồng xây dựng
    short_term_unearned_revenue: Payments received for services not yet performed | Doanh thu chưa thực hiện ngắn hạn
    other_short_term_payables: Other current liabilities not elsewhere classified | Các khoản phải trả ngắn hạn khác
    short_term_loans_and_finance_lease_liabilities: Short-term borrowings and lease obligations | Vay ngắn hạn và nợ thuê tài chính ngắn hạn
    provision_for_short_term_payables: Allowance for uncertain short-term liabilities | Dự phòng phải trả ngắn hạn
    bonus_and_welfare_fund: Reserves for employee bonuses and welfare | Quỹ khen thưởng, phúc lợi
    price_stabilization_fund: Reserve for price stabilization purposes | Quỹ bình ổn giá
    long_term_liabilities: Obligations due after one year | Nợ dài hạn
    long_term_supplier_payables: Amounts owed to suppliers due after one year | Phải trả người bán dài hạn
    long_term_deferred_revenues: Payments received in advance for services to be provided after one year | Doanh thu chưa thực hiện dài hạn
    long_term_expenses_payable: Accrued expenses to be paid after one year | Chi phí phải trả dài hạn
    intercompany_payables_on_working_capital: Amounts owed to related entities for working capital | Phải trả nội bộ về vốn kinh doanh
    long_term_intercompany_payables: Amounts owed to related entities after one year | Phải trả nội bộ dài hạn
    long_term_unearned_revenue: Payments received for services to be performed after one year | Doanh thu chưa thực hiện dài hạn
    other_long_term_payables: Other non-current liabilities not elsewhere classified | Các khoản phải trả dài hạn khác
    long_term_loans_and_finance_lease_liabilities: Long-term borrowings and lease obligations | Vay dài hạn và nợ thuê tài chính dài hạn
    convertible_bonds: Bonds that can be converted into equity | Trái phiếu chuyển đổi
    long_term_liabilities_preference_shares: Preferred shares classified as liabilities | Cổ phiếu ưu đãi xếp vào nợ phải trả
    deferred_income_tax: Taxes payable in future periods | Thuế thu nhập hoãn lại phải trả
    provision_for_long_term_payables: Allowance for uncertain long-term liabilities | Dự phòng phải trả dài hạn
    scientific_and_technological_development_fund: Reserve for research and development activities | Quỹ phát triển khoa học và công nghệ
    owner_equity_total: Total owners equity | Tổng vốn chủ sở hữu
    owner_equity: Owners claim on company assets | Vốn chủ sở hữu
    contributions_from_owners: Capital contributed by owners | Vốn góp của chủ sở hữu
    ordinary_shares_with_voting_rights: Common stock with voting privileges | Cổ phiếu phổ thông có quyền biểu quyết
    owner_equity_preference_shares: Preferred shares classified as equity | Cổ phiếu ưu đãi xếp vào vốn chủ sở hữu
    share_premium: Amount received above par value of shares | Thặng dư vốn cổ phần
    conversion_options_on_bond: Value of conversion options on convertible bonds | Quyền chọn chuyển đổi trái phiếu
    other_capital_of_owners: Other capital contributions from owners | Vốn khác của chủ sở hữu
    treasury_shares: Company own shares repurchased | Cổ phiếu quỹ
    differences_upon_asset_revaluation: Gains/losses from asset revaluations | Chênh lệch đánh giá lại tài sản
    exchange_differences: Gains/losses from currency translation | Chênh lệch tỷ giá
    development_investment_funds: Reserves for development and investment | Quỹ đầu tư phát triển
    enterprise_reorganization_assistance_fund: Reserve for enterprise restructuring | Quỹ hỗ trợ sắp xếp doanh nghiệp
    other_equity_fund: Other equity reserves | Quỹ khác thuộc vốn chủ sở hữu
    undistributed_post_tax_profits: Retained earnings | Lợi nhuận sau thuế chưa phân phối
    undistributed_post_tax_profits_accumulated_by_the_end_of_the_pr: Retained earnings from prior periods | Lợi nhuận sau thuế chưa phân phối lũy kế đến cuối kỳ trước
    undistributed_post_tax_profits_of_current_period: Current period net income not yet distributed | Lợi nhuận sau thuế chưa phân phối kỳ hiện tại
    capital_expenditure_fund: Reserve for capital expenditures | Quỹ đầu tư phát triển
    funding_and_other_funds: Government grants and other funding | Nguồn kinh phí và quỹ khác
    funding: Government financial assistance | Nguồn kinh phí
    funds_that_form_fixed_assets: Funding used to acquire fixed assets | Nguồn vốn đầu tư XDCB
    total_capital: Total liabilities and equity | Tổng nguồn vốn
    """

    vn.train(documentation=doc)

if __name__ == "__main__":
    # add_ddl()
    add_balance_sheet_end_of_period_introduction()
    # add_column_description()