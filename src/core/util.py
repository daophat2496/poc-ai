def _build_numeric_code_maps(items):
    end_map = {}
    begin_map = {}

    for item in items:
        code_str = str(item.code).strip()

        # Skip codes with postfix letter
        if not code_str.isdigit():
            continue

        code_int = int(code_str)

        end_map[code_int] = int(item.amount_end_of_period or 0)
        begin_map[code_int] = int(item.amount_beginning_of_year or 0)

    return end_map, begin_map


def _check_total(values, total_code, low, high):
    """Check:
        total_code == sum(%100==0) == sum(%10==0 and %100!=0) == sum(%10!=0)
    """
    total_value = values.get(total_code)
    if total_value is None:
        return False

    # these code is not divisible by 10, but still sum of some other:
    # 221 = 222 + 223
    # 224 = 225 + 226
    # 227 = 228 + 229
    exclude_codes = [221, 224, 227]

    def in_range(c): return low < c < high

    sum_100 = sum(v for c, v in values.items() if in_range(c) and c % 100 == 0)
    sum_10  = sum(v for c, v in values.items() if in_range(c) and c % 10 == 0 and c % 100 != 0)
    sum_1   = sum(v for c, v in values.items() if in_range(c) and c % 10 != 0 and c not in exclude_codes)

    print(f">>>> check for code: {total_code}")
    print(f">>>>>>> total_value: {total_value}")
    print(f">>>>>>> sum_100: {sum_100}")
    print(f">>>>>>> sum_10: {sum_10}")
    print(f">>>>>>> sum_1: {sum_1}")


    return total_value == sum_100 == sum_10 == sum_1


def verify_balance_sheet_sums(items):
    end_map, begin_map = _build_numeric_code_maps(items)

    # END OF PERIOD
    end_270 = _check_total(end_map, 270, 0, 270)
    end_440 = _check_total(end_map, 440, 270, 440)

    # BEGINNING OF YEAR
    begin_270 = _check_total(begin_map, 270, 0, 270)
    begin_440 = _check_total(begin_map, 440, 270, 440)

    return end_270 and end_440 and begin_270 and begin_440