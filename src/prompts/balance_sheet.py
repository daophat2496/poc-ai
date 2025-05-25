PROMPT_COMPANY_NAME = """What is the company name? If the company name appears in this page, return only the full legal name. Otherwise, ONLY return "No". """

PROMPT_STOCK_CODE = """What is the stock code? If the stock code appears in this page, return only the stock code. Otherwise, ONLY return "No". """

PROMPT_IS_BALANCE_SHEET_FIRST = """
Is this page contain a main Balance sheet (not additional information for balance sheet)?

If there is a table, check its title carefully — is it titled as a balance sheet (a balance sheet may contains showing Assets, Capital, Liabilities, Equity)?

A balance sheet can contain:
- A table or a table-like text box
- A title is named as a balance sheet (a balance sheet may contains showing Assets, Capital, Liabilities, Equity)?
- Row header, Column header, Title, Item name, or Property values match the Balance Sheet (e.g., ASSETS, LIABILITIES, CAPITAL, or EQUITY), it may just contain some properties in a typical balance sheet (because another half is in the first image already), or the properties name may difference from the typical one
- Table can contains: name of item, code, explaination / note, 2 amounts for end of period and beginning of year
- The code of each balance sheet item. Value range: 100-440 (Optional: following by a letter). For example: 100, 311, 411a

Respond with only "Yes" or "No".
"""

PROMPT_IS_BALANCE_SHEET_CONT = """
You are given 2 images, check the SECOND image whether it contains a balance sheet or not?
If it is a clear "Yes" answer, do not look at the first image.
If it is "No" answer in the first place or you are not sure, you can use the first image as a reference. The first image IS a balance sheet. 

A balance sheet can contain:
- A table or a table-like text box (with same number of columns and data type of columns with the first image)
- Row header, Column header, Title, Item name, or Property values match the Balance Sheet (e.g., ASSETS, LIABILITIES, CAPITAL, or EQUITY), it may just contain some properties in a typical balance sheet (because another half is in the first image already), or the properties name may difference from the typical one
- Table can contains: name of item / resource, code, explaination / note, 2 amounts for end of period and beginning of year
- The code of each balance sheet item. Value range: 100-440 (Optional: following by a letter). For example: 100, 311, 411a

Respond with only "Yes" or "No".
"""

PROMPT_BALANCE_SHEET = """
You are a financial data extractor.
Analyze the provided image of a financial statement and extract all:
    - DATE OF BALANCE SHEET (period_end_date) in the Balance Sheet. Carefully check the date format (it could be in dd/mm/yyyy, yyyy/mm/dd, dd-mm-yyyy, yyyy-mm-dd, ...)
    - Currency The currency unit used in this balance sheet
    - "Balance Sheet" items found on this page.

In detail, each "Balance Sheet" item should include:
- The code of each balance sheet item. Value range: 100-440 (Optional: following by a letter). For example: 100, 311, 411a
- The name of the item (Convert to snaake_case with all lower case letters, remove any prefix (A. | 1. | I. | a. |...) and remove any postfix (. | ! | (*) | ...) and remove all special character)
- The amount at the end of the reporting period

Return only the structured JSON list of items, without any extra explanation or markdown.

If no balance sheet items are present, return an empty list.
"""

# PROMPT_BALANCE_SHEET = """
# You are a financial data extractor.
# Analyze the provided image of a financial statement and extract all:
#     - DATE OF BALANCE SHEET (period_end_date) in the Balance Sheet. Carefully check the date format (it could be in dd/mm/yyyy, yyyy/mm/dd, dd-mm-yyyy, yyyy-mm-dd, ...)
#     - Currency The currency unit used in this balance sheet
#     - "Balance Sheet" items found on this page.

# In detail, each "Balance Sheet" item should include:
# - The code of each balance sheet item. Value range: 100-440 (Optional: following by a letter). For example: 100, 311, 411a
# - The name of the item (Convert to snaake_case with all lower case letters, remove any prefix (A. | 1. | I. | a. |...) and remove any postfix (. | ! | (*) | ...) and remove all special character)
# - The amount at the end of the reporting period
# - The amount at the beginning of the year

# Return only the structured JSON list of items, without any extra explanation or markdown.

# If no balance sheet items are present, return an empty list.
# """