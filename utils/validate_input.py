import re


def validate_input(input_str: str) -> re.Match:
    pattern = r"((\d{1,2})\.(\d{1,2})?\.?(\d{1,2})?)"

    match: re.Match[str] | None = re.search(pattern, input_str)

    if match is None:
        raise Exception(
            "Ваше значение не подходит шаблону!\nВведите корректные даные. Например 5. или 5.1 или 4.2.5 "
        )

    return match
