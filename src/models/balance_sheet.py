from pydantic import BaseModel, Field
from typing import List
from datetime import date

class BalanceSheetItem(BaseModel):
    """Represents a single line item in a balance sheet."""
    code: str = Field(
        ...,
        description="The code of each balance sheet item. Value range: 100-440 (Optional: following by a letter). For example: 100, 311, 411a"
    )
    name: str = Field(
        ...,
        description="Name of the balance sheet item. Convert to snake_case with all lower case letters, remove any prefix (A. | 1. | I. | a. |...) and remove any postfix (. | ! | (*) | ...) and remove all special character"
    )
    amount_end_of_period: int = Field(
        ...,
        description="Amount at the end of the current reporting period."
    )
    # amount_beginning_of_year: int = Field(
    #     ...,
    #     description="Amount at the beginning of the year."
    # )

class BalanceSheet(BaseModel):
    """Represents a list of balance sheet items and associated metadata."""
    period_end_date: date = Field(
        ...,
        description="The end date of the reporting period for this balance sheet."
    )
    currency: str = Field(
        ...,
        description="The currency unit used in this balance sheet."
    )
    balance_sheet_items: List[BalanceSheetItem]