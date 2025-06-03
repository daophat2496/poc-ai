from src.vanna_helpers.init_vanna import get_vanna

def add_column_name_list():
    vn = get_vanna()
    doc = """**IMPORTANT** Only use this set of columns in query generated, this is list of columns in balance_sheets_at_end_of_period table
id | company_name | stock_code | period_end_date | currency | created_at | updated_at | short_term_assets | cash_and_cash_equivalents | cash | cash_equivalents | short_term_financial_investments | trading_securities | provision_for_decrease_in_value_of_trading_securities | short_term_investments_held_to_maturity | short_term_receivables | short_term_receivables_from_customers | prepayments_to_sellers_in_short_term | short_term_intercompany_receivables | receivables_according_to_the_progress_of_construction_com | short_term_loan_receivables | other_short_term_receivables | provision_for_uncollectible_short_term_receivables | shortage_of_assets_awaiting_resolution | inventories_total | inventories | provision_against_devaluation_of_goods_in_stock | other_short_term_assets_total | short_term_prepaid_expenses | deductible_vat | taxes_and_other_revenues_to_the_state | purchase_and_resale_of_government_bonds | other_short_term_assets | long_term_assets | long_term_receivables | long_term_receivables_from_customers | prepayments_to_suppliers_in_long_term | working_capital_provided_to_subordinate_units | long_term_intercompany_receivables | receivables_on_long_term_loans | other_long_term_receivables | provision_for_doubtful_long_term_receivables | fixed_assets | tangible_fixed_assets | tangible_fixed_assets_historical_costs | tangible_fixed_assets_value_of_accumulated_depreciation | finance_lease_fixed_asset | finance_lease_fixed_asset_historical_costs | finance_lease_fixed_asset_value_of_accumulated_depreciation | intangible_fixed_assets | intangible_fixed_assets_historical_costs | intangible_fixed_assets_value_of_accumulated_depreciation | investment_real_property | investment_real_property_historical_costs | investment_real_property_value_of_accumulated_depreciation | long_term_unfinished_assets | cost_of_long_term_work_in_progress | cost_of_construction_in_progress | long_term_financial_investments | investments_in_subsidiaries | investments_in_associated_companies_and_joint_ventures | investments_in_other_units | provisions_for_long_term_financial_investments | long_term_investments_held_to_maturity | other_long_term_assets_total | long_term_prepaid_expenses | deferred_income_tax_assets | long_term_equipment_supplies_and_spare_parts | other_long_term_assets | total_assets | liabilities | short_term_debt | short_term_supplier_payables | short_term_deferred_revenues | taxes_and_other_payables_to_state | payables_to_employees | short_term_expenses_payable | short_term_intercompany_payables | payables_according_to_the_progress_of_construction_contract | short_term_unearned_revenue | other_short_term_payables | short_term_loans_and_finance_lease_liabilities | provision_for_short_term_payables | bonus_and_welfare_fund | price_stabilization_fund | long_term_liabilities | long_term_supplier_payables | long_term_deferred_revenues | long_term_expenses_payable | intercompany_payables_on_working_capital | long_term_intercompany_payables | long_term_unearned_revenue | other_long_term_payables | long_term_loans_and_finance_lease_liabilities | convertible_bonds | long_term_liabilities_preference_shares | deferred_income_tax | provision_for_long_term_payables | scientific_and_technological_development_fund | owner_equity_total | owner_equity | contributions_from_owners | ordinary_shares_with_voting_rights | owner_equity_preference_shares | share_premium | conversion_options_on_bond | other_capital_of_owners | treasury_shares | differences_upon_asset_revaluation | exchange_differences | development_investment_funds | enterprise_reorganization_assistance_fund | other_equity_fund | undistributed_post_tax_profits | undistributed_post_tax_profits_accumulated_end_of_prv_period | undistributed_post_tax_profits_of_current_period | capital_expenditure_fund | funding_and_other_funds | funding | funds_that_form_fixed_assets | total_capital"""

    vn.add_documentation(documentation=doc)

def add_column_description():
    vn = get_vanna()
    doc = """Column name list and their description in balance_sheets_at_end_of_period table:
id: system id for company (do not use in response)
company_name: name for the company
stock_code: stock code of the company
period_end_date: date of the balance sheet
currency: currency use in the balance sheet
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
long_term_investments_held_to_maturity: Debt securities the company intends to hold until maturity and are due after one year | Chứng khoán nợ mà công ty dự định nắm giữ đến ngày đáo hạn và có thời hạn trên một năm        
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
undistributed_post_tax_profits_accumulated_end_of_prv_period: Retained earnings from prior periods | Lợi nhuận sau thuế chưa phân phối lũy kế đến cuối kỳ trước
undistributed_post_tax_profits_of_current_period: Current period net income not yet distributed | Lợi nhuận sau thuế chưa phân phối kỳ hiện tại
capital_expenditure_fund: Reserve for capital expenditures | Quỹ đầu tư phát triển
funding_and_other_funds: Government grants and other funding | Nguồn kinh phí và quỹ khác
funding: Government financial assistance | Nguồn kinh phí
funds_that_form_fixed_assets: Funding used to acquire fixed assets | Nguồn vốn đầu tư XDCB
total_capital: Total liabilities and equity | Tổng nguồn vốn"""

    vn.train(documentation=doc)

def add_ddl():
    vn = get_vanna()
    ddl = """ -- ONLY USE THESE COLUMNS FOR QUERY
CREATE TABLE public.balance_sheets_at_end_of_period (
    id integer NOT NULL,
    company_name character varying(255) NOT NULL,
    stock_code character varying(20),
    period_end_date date NOT NULL,
    currency character varying(10),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    short_term_assets numeric(20,2),
    cash_and_cash_equivalents numeric(20,2),
    cash numeric(20,2),
    cash_equivalents numeric(20,2),
    short_term_financial_investments numeric(20,2),
    trading_securities numeric(20,2),
    provision_for_decrease_in_value_of_trading_securities numeric(20,2),
    short_term_investments_held_to_maturity numeric(20,2),
    short_term_receivables numeric(20,2),
    short_term_receivables_from_customers numeric(20,2),
    prepayments_to_sellers_in_short_term numeric(20,2),
    short_term_intercompany_receivables numeric(20,2),
    receivables_according_to_the_progress_of_construction_com numeric(20,2),
    short_term_loan_receivables numeric(20,2),
    other_short_term_receivables numeric(20,2),
    provision_for_uncollectible_short_term_receivables numeric(20,2),
    shortage_of_assets_awaiting_resolution numeric(20,2),
    inventories_total numeric(20,2),
    inventories numeric(20,2),
    provision_against_devaluation_of_goods_in_stock numeric(20,2),
    other_short_term_assets_total numeric(20,2),
    short_term_prepaid_expenses numeric(20,2),
    deductible_vat numeric(20,2),
    taxes_and_other_revenues_to_the_state numeric(20,2),
    purchase_and_resale_of_government_bonds numeric(20,2),
    other_short_term_assets numeric(20,2),
    long_term_assets numeric(20,2),
    long_term_receivables numeric(20,2),
    long_term_receivables_from_customers numeric(20,2),
    prepayments_to_suppliers_in_long_term numeric(20,2),
    working_capital_provided_to_subordinate_units numeric(20,2),
    long_term_intercompany_receivables numeric(20,2),
    receivables_on_long_term_loans numeric(20,2),
    other_long_term_receivables numeric(20,2),
    provision_for_doubtful_long_term_receivables numeric(20,2),
    fixed_assets numeric(20,2),
    tangible_fixed_assets numeric(20,2),
    tangible_fixed_assets_historical_costs numeric(20,2),
    tangible_fixed_assets_value_of_accumulated_depreciation numeric(20,2),
    finance_lease_fixed_asset numeric(20,2),
    finance_lease_fixed_asset_historical_costs numeric(20,2),
    finance_lease_fixed_asset_value_of_accumulated_depreciation numeric(20,2),
    intangible_fixed_assets numeric(20,2),
    intangible_fixed_assets_historical_costs numeric(20,2),
    intangible_fixed_assets_value_of_accumulated_depreciation numeric(20,2),
    investment_real_property numeric(20,2),
    investment_real_property_historical_costs numeric(20,2),
    investment_real_property_value_of_accumulated_depreciation numeric(20,2),
    long_term_unfinished_assets numeric(20,2),
    cost_of_long_term_work_in_progress numeric(20,2),
    cost_of_construction_in_progress numeric(20,2),
    long_term_financial_investments numeric(20,2),
    investments_in_subsidiaries numeric(20,2),
    investments_in_associated_companies_and_joint_ventures numeric(20,2),
    investments_in_other_units numeric(20,2),
    provisions_for_long_term_financial_investments numeric(20,2),
    long_term_investments_held_to_maturity numeric(20,2),
    other_long_term_assets_total numeric(20,2),
    long_term_prepaid_expenses numeric(20,2),
    deferred_income_tax_assets numeric(20,2),
    long_term_equipment_supplies_and_spare_parts numeric(20,2),
    other_long_term_assets numeric(20,2),
    total_assets numeric(20,2),
    liabilities numeric(20,2),
    short_term_debt numeric(20,2),
    short_term_supplier_payables numeric(20,2),
    short_term_deferred_revenues numeric(20,2),
    taxes_and_other_payables_to_state numeric(20,2),
    payables_to_employees numeric(20,2),
    short_term_expenses_payable numeric(20,2),
    short_term_intercompany_payables numeric(20,2),
    payables_according_to_the_progress_of_construction_contract numeric(20,2),
    short_term_unearned_revenue numeric(20,2),
    other_short_term_payables numeric(20,2),
    short_term_loans_and_finance_lease_liabilities numeric(20,2),
    provision_for_short_term_payables numeric(20,2),
    bonus_and_welfare_fund numeric(20,2),
    price_stabilization_fund numeric(20,2),
    long_term_liabilities numeric(20,2),
    long_term_supplier_payables numeric(20,2),
    long_term_deferred_revenues numeric(20,2),
    long_term_expenses_payable numeric(20,2),
    intercompany_payables_on_working_capital numeric(20,2),
    long_term_intercompany_payables numeric(20,2),
    long_term_unearned_revenue numeric(20,2),
    other_long_term_payables numeric(20,2),
    long_term_loans_and_finance_lease_liabilities numeric(20,2),
    convertible_bonds numeric(20,2),
    long_term_liabilities_preference_shares numeric(20,2),
    deferred_income_tax numeric(20,2),
    provision_for_long_term_payables numeric(20,2),
    scientific_and_technological_development_fund numeric(20,2),
    owner_equity_total numeric(20,2),
    owner_equity numeric(20,2),
    contributions_from_owners numeric(20,2),
    ordinary_shares_with_voting_rights numeric(20,2),
    owner_equity_preference_shares numeric(20,2),
    share_premium numeric(20,2),
    conversion_options_on_bond numeric(20,2),
    other_capital_of_owners numeric(20,2),
    treasury_shares numeric(20,2),
    differences_upon_asset_revaluation numeric(20,2),
    exchange_differences numeric(20,2),
    development_investment_funds numeric(20,2),
    enterprise_reorganization_assistance_fund numeric(20,2),
    other_equity_fund numeric(20,2),
    undistributed_post_tax_profits numeric(20,2),
    undistributed_post_tax_profits_accumulated_end_of_prv_period numeric(20,2),
    undistributed_post_tax_profits_of_current_period numeric(20,2),
    capital_expenditure_fund numeric(20,2),
    funding_and_other_funds numeric(20,2),
    funding numeric(20,2),
    funds_that_form_fixed_assets numeric(20,2),
    total_capital numeric(20,2)
);"""
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_assets IS 'Total value of all current assets expected to be converted to cash within one year | Tổng giá trị tất cả tài sản ngắn hạn dự kiến chuyển đổi thành tiền trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.cash_and_cash_equivalents IS 'Highly liquid assets including cash and short-term investments | Tài sản có tính thanh khoản cao bao gồm tiền mặt và các khoản đầu tư ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.cash IS 'Physical currency, coins, and balances in checking accounts | Tiền mặt vật lý, tiền xu và số dư trong tài khoản séc';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.cash_equivalents IS 'Short-term, highly liquid investments that are readily convertible to cash | Các khoản đầu tư ngắn hạn, có tính thanh khoản cao dễ dàng chuyển đổi thành tiền mặt';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_financial_investments IS 'Investments intended to be held for less than one year | Các khoản đầu tư tài chính dự định nắm giữ dưới một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.trading_securities IS 'Securities bought and held principally for selling in the near term | Chứng khoán mua và nắm giữ chủ yếu để bán trong thời gian ngắn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provision_for_decrease_in_value_of_trading_securities IS 'Allowance for potential loss in value of trading securities | Dự phòng cho khoản lỗ tiềm tàng về giá trị của chứng khoán kinh doanh';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_investments_held_to_maturity IS 'Debt securities the company intends to hold until maturity and are due within one year | Chứng khoán nợ mà công ty dự định nắm giữ đến ngày đáo hạn và có thời hạn dưới một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_receivables IS 'Amounts expected to be received within one year | Các khoản dự kiến sẽ nhận được trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_receivables_from_customers IS 'Amounts owed by customers that are due within one year | Các khoản khách hàng nợ đến hạn trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.prepayments_to_sellers_in_short_term IS 'Advance payments made to suppliers for goods or services to be received within one year | Thanh toán trước cho nhà cung cấp đối với hàng hóa hoặc dịch vụ sẽ nhận được trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_intercompany_receivables IS 'Amounts owed to the company by related entities within one year | Các khoản các thực thể liên quan nợ công ty trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.receivables_according_to_the_progress_of_construction_com IS 'Amounts receivable based on percentage of completion of construction contracts | Các khoản phải thu theo tiến độ hoàn thành hợp đồng xây dựng';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_loan_receivables IS 'Short-term loans made to others that are due within one year | Các khoản cho vay ngắn hạn đến hạn trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_short_term_receivables IS 'Other amounts due to the company within one year not elsewhere classified | Các khoản phải thu ngắn hạn khác không được phân loại ở nơi khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provision_for_uncollectible_short_term_receivables IS 'Allowance for doubtful short-term receivables | Dự phòng cho các khoản phải thu ngắn hạn khó đòi';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.shortage_of_assets_awaiting_resolution IS 'Shortages of assets that are pending investigation and resolution | Thiếu hụt tài sản đang chờ điều tra và giải quyết';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.inventories_total IS 'Total value of goods held for sale or in production | Tổng giá trị hàng hóa nắm giữ để bán hoặc trong sản xuất';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.inventories IS 'Raw materials, work in progress and finished goods | Nguyên liệu, sản phẩm dở dang và thành phẩm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provision_against_devaluation_of_goods_in_stock IS 'Allowance for potential loss in value of inventory | Dự phòng giảm giá hàng tồn kho';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_short_term_assets_total IS 'Total of other current assets not elsewhere classified | Tổng các tài sản ngắn hạn khác không được phân loại ở nơi khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_prepaid_expenses IS 'Expenses paid in advance that will be recognized within one year | Chi phí trả trước sẽ được ghi nhận trong vòng một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.deductible_vat IS 'Value added tax that can be deducted | Giá trị gia tăng được khấu trừ';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.taxes_and_other_revenues_to_the_state IS 'Taxes and other amounts payable to government authorities | Thuế và các khoản khác phải nộp nhà nước';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.purchase_and_resale_of_government_bonds IS 'Government bonds purchased for resale | Trái phiếu chính phủ mua để bán lại';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_short_term_assets IS 'Other current assets not elsewhere specified | Các tài sản ngắn hạn khác không được chỉ định ở nơi khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_assets IS 'Assets that provide value for more than one year | Tài sản cung cấp giá trị trong hơn một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_receivables IS 'Amounts expected to be received after one year | Các khoản dự kiến sẽ nhận được sau một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_receivables_from_customers IS 'Amounts owed by customers that are due after one year | Các khoản khách hàng nợ đến hạn sau một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.prepayments_to_suppliers_in_long_term IS 'Advance payments made to suppliers for goods or services to be received after one year | Thanh toán trước cho nhà cung cấp đối với hàng hóa hoặc dịch vụ sẽ nhận được sau một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.working_capital_provided_to_subordinate_units IS 'Capital provided to subsidiaries and affiliates | Vốn lưu động cung cấp cho các đơn vị trực thuộc';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_intercompany_receivables IS 'Amounts owed to the company by related entities after one year | Các khoản các thực thể liên quan nợ công ty sau một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.receivables_on_long_term_loans IS 'Long-term loans made to others | Các khoản cho vay dài hạn cho bên khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_long_term_receivables IS 'Other amounts due to the company after one year not elsewhere classified | Các khoản phải thu dài hạn khác không được phân loại ở nơi khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provision_for_doubtful_long_term_receivables IS 'Allowance for doubtful long-term receivables | Dự phòng cho các khoản phải thu dài hạn khó đòi';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.fixed_assets IS 'Long-term tangible and intangible assets used in operations | Tài sản hữu hình và vô hình dài hạn sử dụng trong hoạt động';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.tangible_fixed_assets IS 'Physical assets used in operations | Tài sản cố định hữu hình';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.tangible_fixed_assets_historical_costs IS 'Original acquisition cost of tangible fixed assets | Nguyên giá tài sản cố định hữu hình';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.tangible_fixed_assets_value_of_accumulated_depreciation IS 'Total depreciation accumulated on tangible fixed assets | Giá trị hao mòn lũy kế tài sản cố định hữu hình';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.finance_lease_fixed_asset IS 'Assets acquired under finance lease arrangements | Tài sản thuê tài chính';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.finance_lease_fixed_asset_historical_costs IS 'Original cost of finance leased assets | Nguyên giá tài sản thuê tài chính';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.finance_lease_fixed_asset_value_of_accumulated_depreciation IS 'Total depreciation accumulated on finance leased assets | Giá trị hao mòn lũy kế tài sản thuê tài chính';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.intangible_fixed_assets IS 'Non-physical assets with long-term value | Tài sản cố định vô hình';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.intangible_fixed_assets_historical_costs IS 'Original acquisition cost of intangible fixed assets | Nguyên giá tài sản cố định vô hình';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.intangible_fixed_assets_value_of_accumulated_depreciation IS 'Total amortization accumulated on intangible fixed assets | Giá trị hao mòn lũy kế tài sản cố định vô hình';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.investment_real_property IS 'Real estate held for investment purposes | Bất động sản đầu tư';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.investment_real_property_historical_costs IS 'Original acquisition cost of investment property | Nguyên giá bất động sản đầu tư';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.investment_real_property_value_of_accumulated_depreciation IS 'Total depreciation accumulated on investment property | Giá trị hao mòn lũy kế bất động sản đầu tư';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_unfinished_assets IS 'Assets under construction or development | Tài sản dở dang dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.cost_of_long_term_work_in_progress IS 'Costs incurred for long-term projects not yet completed | Chi phí cho các dự án dài hạn chưa hoàn thành';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.cost_of_construction_in_progress IS 'Costs incurred for construction projects not yet completed | Chi phí xây dựng dở dang';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_financial_investments IS 'Investments intended to be held for more than one year | Đầu tư tài chính dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.investments_in_subsidiaries IS 'Investments in companies where the parent has control | Đầu tư vào công ty con';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.investments_in_associated_companies_and_joint_ventures IS 'Investments in companies where the investor has significant influence | Đầu tư vào công ty liên kết và liên doanh';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.investments_in_other_units IS 'Other long-term equity investments | Đầu tư vào các đơn vị khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provisions_for_long_term_financial_investments IS 'Allowance for potential loss on long-term investments | Dự phòng giảm giá đầu tư tài chính dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_investments_held_to_maturity IS 'Debt securities the company intends to hold until maturity and are due after one year | Chứng khoán nợ mà công ty dự định nắm giữ đến ngày đáo hạn và có thời hạn trên một năm';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_long_term_assets_total IS 'Total of other non-current assets not elsewhere classified | Tổng các tài sản dài hạn khác không được phân loại ở nơi khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_prepaid_expenses IS 'Expenses paid in advance that will be recognized after one year | Chi phí trả trước dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.deferred_income_tax_assets IS 'Taxes paid in advance or tax benefits to be realized in future periods | Tài sản thuế thu nhập hoãn lại';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_equipment_supplies_and_spare_parts IS 'Long-term inventory of equipment and spare parts | Vật tư, phụ tùng thay thế dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_long_term_assets IS 'Other non-current assets not elsewhere specified | Tài sản dài hạn khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.total_assets IS 'Sum of all assets | Tổng tài sản';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.liabilities IS 'Total obligations owed to external parties including both short-term and long-term debts | Tổng các khoản nợ phải trả cho bên ngoài bao gồm nợ ngắn hạn và dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_debt IS 'Obligations due within one year | Nợ ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_supplier_payables IS 'Amounts owed to suppliers due within one year | Phải trả người bán ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_deferred_revenues IS 'Payments received in advance for services to be provided within one year | Doanh thu chưa thực hiện ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.taxes_and_other_payables_to_state IS 'Taxes and other amounts payable to government within one year | Thuế và các khoản phải nộp nhà nước ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.payables_to_employees IS 'Wages and benefits owed to employees | Phải trả người lao động';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_expenses_payable IS 'Accrued expenses to be paid within one year | Chi phí phải trả ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_intercompany_payables IS 'Amounts owed to related entities within one year | Phải trả nội bộ ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.payables_according_to_the_progress_of_construction_contract IS 'Amounts payable based on percentage of completion of construction contracts | Phải trả theo tiến độ hợp đồng xây dựng';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_unearned_revenue IS 'Payments received for services not yet performed | Doanh thu chưa thực hiện ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_short_term_payables IS 'Other current liabilities not elsewhere classified | Các khoản phải trả ngắn hạn khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.short_term_loans_and_finance_lease_liabilities IS 'Short-term borrowings and lease obligations | Vay ngắn hạn và nợ thuê tài chính ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provision_for_short_term_payables IS 'Allowance for uncertain short-term liabilities | Dự phòng phải trả ngắn hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.bonus_and_welfare_fund IS 'Reserves for employee bonuses and welfare | Quỹ khen thưởng, phúc lợi';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.price_stabilization_fund IS 'Reserve for price stabilization purposes | Quỹ bình ổn giá';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_liabilities IS 'Obligations due after one year | Nợ dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_supplier_payables IS 'Amounts owed to suppliers due after one year | Phải trả người bán dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_deferred_revenues IS 'Payments received in advance for services to be provided after one year | Doanh thu chưa thực hiện dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_expenses_payable IS 'Accrued expenses to be paid after one year | Chi phí phải trả dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.intercompany_payables_on_working_capital IS 'Amounts owed to related entities for working capital | Phải trả nội bộ về vốn kinh doanh';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_intercompany_payables IS 'Amounts owed to related entities after one year | Phải trả nội bộ dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_unearned_revenue IS 'Payments received for services to be performed after one year | Doanh thu chưa thực hiện dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_long_term_payables IS 'Other non-current liabilities not elsewhere classified | Các khoản phải trả dài hạn khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_loans_and_finance_lease_liabilities IS 'Long-term borrowings and lease obligations | Vay dài hạn và nợ thuê tài chính dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.convertible_bonds IS 'Bonds that can be converted into equity | Trái phiếu chuyển đổi';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.long_term_liabilities_preference_shares IS 'Preferred shares classified as liabilities | Cổ phiếu ưu đãi xếp vào nợ phải trả';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.deferred_income_tax IS 'Taxes payable in future periods | Thuế thu nhập hoãn lại phải trả';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.provision_for_long_term_payables IS 'Allowance for uncertain long-term liabilities | Dự phòng phải trả dài hạn';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.scientific_and_technological_development_fund IS 'Reserve for research and development activities | Quỹ phát triển khoa học và công nghệ';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.owner_equity_total IS 'Total owners equity | Tổng vốn chủ sở hữu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.owner_equity IS 'Owners claim on company assets | Vốn chủ sở hữu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.contributions_from_owners IS 'Capital contributed by owners | Vốn góp của chủ sở hữu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.ordinary_shares_with_voting_rights IS 'Common stock with voting privileges | Cổ phiếu phổ thông có quyền biểu quyết';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.owner_equity_preference_shares IS 'Preferred shares classified as equity | Cổ phiếu ưu đãi xếp vào vốn chủ sở hữu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.share_premium IS 'Amount received above par value of shares | Thặng dư vốn cổ phần';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.conversion_options_on_bond IS 'Value of conversion options on convertible bonds | Quyền chọn chuyển đổi trái phiếu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_capital_of_owners IS 'Other capital contributions from owners | Vốn khác của chủ sở hữu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.treasury_shares IS 'Company own shares repurchased | Cổ phiếu quỹ';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.differences_upon_asset_revaluation IS 'Gains/losses from asset revaluations | Chênh lệch đánh giá lại tài sản';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.exchange_differences IS 'Gains/losses from currency translation | Chênh lệch tỷ giá';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.development_investment_funds IS 'Reserves for development and investment | Quỹ đầu tư phát triển';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.enterprise_reorganization_assistance_fund IS 'Reserve for enterprise restructuring | Quỹ hỗ trợ sắp xếp doanh nghiệp';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.other_equity_fund IS 'Other equity reserves | Quỹ khác thuộc vốn chủ sở hữu';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.undistributed_post_tax_profits IS 'Retained earnings | Lợi nhuận sau thuế chưa phân phối';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.undistributed_post_tax_profits_accumulated_end_of_prv_period IS 'Retained earnings from prior periods | Lợi nhuận sau thuế chưa phân phối lũy kế đến cuối kỳ trước';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.undistributed_post_tax_profits_of_current_period IS 'Current period net income not yet distributed | Lợi nhuận sau thuế chưa phân phối kỳ hiện tại';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.capital_expenditure_fund IS 'Reserve for capital expenditures | Quỹ đầu tư phát triển';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.funding_and_other_funds IS 'Government grants and other funding | Nguồn kinh phí và quỹ khác';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.funding IS 'Government financial assistance | Nguồn kinh phí';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.funds_that_form_fixed_assets IS 'Funding used to acquire fixed assets | Nguồn vốn đầu tư XDCB';
# COMMENT ON COLUMN public.balance_sheets_at_end_of_period.total_capital IS 'Total liabilities and equity | Tổng nguồn vốn';
#     """
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
    undistributed_post_tax_profits_accumulated_end_of_prv_period: Retained earnings from prior periods | Lợi nhuận sau thuế chưa phân phối lũy kế đến cuối kỳ trước
    undistributed_post_tax_profits_of_current_period: Current period net income not yet distributed | Lợi nhuận sau thuế chưa phân phối kỳ hiện tại
    capital_expenditure_fund: Reserve for capital expenditures | Quỹ đầu tư phát triển
    funding_and_other_funds: Government grants and other funding | Nguồn kinh phí và quỹ khác
    funding: Government financial assistance | Nguồn kinh phí
    funds_that_form_fixed_assets: Funding used to acquire fixed assets | Nguồn vốn đầu tư XDCB
    total_capital: Total liabilities and equity | Tổng nguồn vốn
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
    # add_column_description()
    add_column_name_list()
    add_company_query()
    # add_ddl()
    # # add_balance_sheet_end_of_period_introduction()
    # # add_column_description()
    add_coalesce_for_total_doc()