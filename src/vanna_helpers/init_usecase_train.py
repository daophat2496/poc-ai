from src.vanna_helpers.init_vanna import get_vanna

def add_usecase1():
    vn = get_vanna()
    question = "Tổng tiền mặt và tương đương tiền mặt của công ty TDS tại 31/03/2025?"
    sql = """
SELECT cash_and_cash_equivalents
FROM public.balance_sheets_at_end_of_period
WHERE (LOWER(stock_code) = LOWER('TDS') OR LOWER(company_name) LIKE '%' || LOWER('TDS') || '%')
    AND period_end_date = '2025-03-31';
"""

    vn.train(question=question, sql=sql)

def add_usecase3():
    vn = get_vanna()
    question = "Kết quả làm ăn của công ty TDS như thế nào tại 31/03/2025?"
    sql = """
SELECT *
FROM public.balance_sheets_at_end_of_period
WHERE (LOWER(stock_code) = LOWER('TDS') OR LOWER(company_name) LIKE '%' || LOWER('TDS') || '%')
    AND period_end_date = '2025-03-31';
;
"""

def add_usecase5():
    vn = get_vanna()
    question = "Tình hình nợ của các công ty tại ngày 31/03/2025"
    sql = """
SELECT company_name, stock_code, liabilities
FROM public.balance_sheets_at_end_of_period
WHERE period_end_date = '2025-03-31'
ORDER BY liabilities DESC
;
"""

def add_usecase2():
    vn = get_vanna()
    question = "công ty nào có bảng cân đối kế toán khả quan nhất vào ngày 31/03/2025?"
    sql = """
SELECT company_name, stock_code, total_assets, liabilities, owner_equity_total
FROM public.balance_sheets_at_end_of_period
WHERE period_end_date = '2025-03-31'
ORDER BY (total_assets - liabilities + owner_equity_total) DESC
LIMIT 1
;
"""

    vn.train(question=question, sql=sql)

def add_usecase3():
    vn = get_vanna()
    question = "Kết quả làm ăn của công ty TDS như thế nào tại 31/03/2025?"
    sql = """
SELECT *
FROM public.balance_sheets_at_end_of_period
WHERE (LOWER(stock_code) = LOWER('TDS') OR LOWER(company_name) LIKE '%' || LOWER('TDS') || '%')
    AND period_end_date = '2025-03-31';
;
"""

    vn.train(question=question, sql=sql)

def add_usecase4():
    vn = get_vanna()
    question = "Công ty nào có tài sản an toàn nhất vào cuối năm 2024?"
    sql = """
SELECT company_name, stock_code, cash_and_cash_equivalents, period_end_date
FROM public.balance_sheets_at_end_of_period
WHERE EXTRACT(YEAR FROM period_end_date) = 2024
ORDER BY cash_and_cash_equivalents DESC
LIMIT 1
;
"""

    vn.train(question=question, sql=sql)

def add_usecase5():
    vn = get_vanna()
    question = "So sánh nợ của các công ty tại ngày 31/03/2025"
    sql = """
SELECT company_name, stock_code, liabilities
FROM public.balance_sheets_at_end_of_period
WHERE period_end_date = '2025-03-31'
ORDER BY liabilities DESC
;
"""

    vn.train(question=question, sql=sql)

def add_usecase6():
    vn = get_vanna()
    question = "Tỷ lệ khả năng thanh toán hiện hành (tài sản ngắn hạn / nợ ngắn hạn) của công ty CTD tại thời điểm 31/03/2025 là bao nhiêu?"
    sql = """
SELECT short_term_assets / short_term_debt AS current_ratio
FROM public.balance_sheets_at_end_of_period
WHERE (LOWER(stock_code) = LOWER('CTD') OR LOWER(company_name) LIKE '%' || LOWER('CTD') || '%')
    AND period_end_date = '2025-03-31'
;
"""

    vn.train(question=question, sql=sql)

if __name__ == "__main__":
    add_usecase3()