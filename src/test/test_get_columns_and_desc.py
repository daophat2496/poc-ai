from src.database2.database_helpers import get_column_name_and_description

res = get_column_name_and_description("balance_sheets_at_end_of_period")
res_str = "\n".join(
    f"{i[0]}: {i[1]}"
    for i in res if i[1]
)
print(res_str)