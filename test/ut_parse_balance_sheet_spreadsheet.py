import os
from pathlib import Path
from typing import Dict

from src.core.balance_sheet import parse_balance_sheet_spreadsheet   # ← change import

FILE_PATH = "C:\\Users\\Phat Dao\\Downloads\\POC AI\\NOS\\DN - BẢNG CÂN ĐỐI KẾ TOÁN (2).xls"

def test_parse_spreadsheet():
    file_path = Path(FILE_PATH)

    if not file_path.exists():
        raise FileNotFoundError(f"Test file not found: {file_path}")

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    result = parse_balance_sheet_spreadsheet(file_bytes)

    print("Parsed spreadsheet metrics:")
    for code, value in result.items():
        print(f"{code}: {value}")

    assert isinstance(result, dict)
    assert len(result) > 0


if __name__ == "__main__":
    test_parse_spreadsheet()