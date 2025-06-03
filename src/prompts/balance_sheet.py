PROMPT_COMPANY_NAME = """What is the company name?
If the company name appears in this page, *IMPORTANT* return only the name, DO NOT translate it, DO NOT add any explanation.
Otherwise, ONLY return "No". DO NOT add any explanation.

Example:
Input: [image]
Output: Công ty Cổ phần Xây Dựng Coteccons

Input: [image]
Output: Kosy Joint Stock Company

Input: [image]
Output: No"""

PROMPT_STOCK_CODE = """What is the stock code?
If the stock code appears in this page, *IMPORTANT* return only the stock code, DO NOT translate it, DO NOT add any explanation.
Otherwise, ONLY return "No". DO NOT add any explanation.

Example:
Input: [image]
Output: CTD

Input: [image]
Output: TTE

Input: [image]
Output: No"""

PROMPT_IS_BALANCE_SHEET_FIRST = """This is a Yes/No question. Does this page contain a balance sheet or part of a balance sheet?
Look for these key indicators:
- A table, or a table-like text box, or lists of items with financial data organized in rows and columns
- There could be a title is named as a balance sheet (Balance sheet, or bảng cân đối, ...)
- Codes in range 100-440 (may include letters like 311a, 312b)
- Financial section headers: ASSETS, LIABILITIES, CAPITAL, EQUITY, etc
- Column headers like "End of period", "Beginning of year", or similar date references
- Item names typical of balance sheets (Cash, Inventories, Fixed assets, etc.)
A balance sheet may be split across multiple pages, so this could be any section.
*IMPORTANT*: Respond with only "Yes" or "No", DO NOT add any explanation.

Example:
Input: [images]
Output: Yes

Input: [images]
Output: No"""

PROMPT_IS_BALANCE_SHEET_CONT = """This is a Yes/No question. You are given 2 images. The FIRST image contains a confirmed balance sheet.
Does the SECOND image contain a balance sheet, or contain a part of a balance sheet, it may continue balance sheet in the first image, or contain related balance sheet content?
The second image should have:
- A table, or a table-like text box, or lists of items with financial data organized in rows and columns
- There could be a title is named as a balance sheet (Balance sheet, or bảng cân đối, ...)
- Similar structure and layout as the first image
- Financial codes continuing the sequence from the first image (range 100-440)
- Financial section headers (LIABILITIES, CAPITAL, EQUITY, etc.)
- Same column headers for dates/periods as the first image
- Financial data in the same format and currency
Even if the section names are different (e.g., first image shows ASSETS, second shows CAPITAL), it's still part of the same balance sheet if the structure matches.
*IMPORTANT*: Respond with only "Yes" or "No", DO NOT add any explanation.

Example:
Input: [images]
Output: Yes

Input: [images]
Output: No"""

PROMPT_BALANCE_SHEET = """You are a financial data extractor.
Analyze ALL provided images of financial statements and extract all:
    - DATE OF BALANCE SHEET (period_end_date) in the Balance Sheet. CRITICAL: Pay careful attention to date format interpretation:
        * If format appears to be DD/MM/YYYY or DD-MM-YYYY (day first), interpret accordingly (e.g., "30/06/2024" = June 30, 2024)
        * If format appears to be MM/DD/YYYY or MM-DD-YYYY (month first), interpret accordingly (e.g., "06/30/2024" = June 30, 2024)  
        * If format appears to be YYYY/MM/DD or YYYY-MM-DD (year first), interpret accordingly (e.g., "2024/06/30" = June 30, 2024)
        * Look for context clues like document language, company location, or other dates in the document to determine the likely format
        * When in doubt about DD/MM vs MM/DD, consider that dates like "30/06/2024" can only be DD/MM format (since there's no 30th month)
        * Return the date in YYYY-MM-DD format regardless of input format
    - Currency: The currency unit used in this balance sheet, convert is to formal unit (VND, USD, etc.)
    - "Balance Sheet" items found across ALL provided images. Combine data from all images into a single comprehensive list.
In detail, each "Balance Sheet" item should include:
- The code of each balance sheet item: 
  * Look for the code in a dedicated "Code" or "Code No." column
  * Extract 3-digit numbers (100-440) with optional trailing letters (format: [0-9]{3}[a-z]*)
  * DO NOT extract numbers from item name prefixes like "1.", "I.", "A.", etc.
  * Code position examples:
    - If table shows "311 | 1. Short-term trade payables" → code is "311"
    - If table shows "1. Short-term trade payables | 311" → code is "311" 
    - If item shows "421a Accumulated profit" → code is "421a"
    - If item shows "A. CURRENT ASSETS" with code "100" in separate column → code is "100"
- The name of the item (keep the language as is in the image)
- The amount at the end of the reporting period
- The amount at the beginning of the year
IMPORTANT: Include ALL items including subtotals and grand totals (like TOTAL ASSETS, TOTAL LIABILITIES, TOTAL CAPITAL, etc.) Even if an item appears to be a summary or total or footer, include it in the extraction.
Return only the structured JSON list of items, without any extra explanation or markdown."""