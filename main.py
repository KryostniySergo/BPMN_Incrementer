import os
import re


def strings_from_bpmn(bpmn_path: str) -> list[str]:
    string_list: list[str] = []

    with open(bpmn_path, "r", encoding="utf-8") as file:
        string_list = file.readlines()

    return string_list


def choose_pattern(template: re.Match) -> str:
    first_number: str = template.group(2)
    second_number: str = template.group(3)
    last_number: str = template.group(4)

    if last_number:
        return r"name=\"(" + first_number + r"\." + second_number + r"\.?(\d{1,2})?)"
    elif second_number:
        return r"name=\"(" + first_number + r"\.?(\d{1,2})?)"
    else:
        return r"name=\"((" + first_number + r")\.)"


def choose_replacment_str(template: re.Match, match: re.Match) -> str:
    first_number: str = template.group(2)
    second_number: str = template.group(3)
    last_number: str = template.group(4)

    if last_number:
        return f'name="{first_number}.{second_number}.{int(match.group(2)) + 1}'
    elif second_number:
        return f'name="{first_number}.{int(match.group(2)) + 1}'
    else:
        return f'name="{int(match.group(2)) + 1}.'


def retry_or_continue(template: re.Match, match: re.Match) -> bool:
    first_number: str = template.group(2)
    second_number: str = template.group(3)
    last_number: str = template.group(4)

    if last_number and int(last_number) > int(match.group(2)):
        return True
    elif second_number and int(second_number) > int(match.group(2)):
        return True
    elif (
        not last_number
        and not second_number
        and int(first_number) < int(match.group(2))
    ):
        return True

    return False


def incriment_strings(string_list: list[str], template: re.Match) -> None:
    # Full string => 4.1.2
    # 0-> 4.1.2 | 1-> 4.1.2 | 2-> 4 | 3-> 1 | 4-> 2
    pattern: str = choose_pattern(template)

    for i in range(len(string_list)):
        match: re.Match | None = re.search(pattern, string_list[i])
        if match is None:
            continue
        if retry_or_continue(template, match):
            continue

        replacment_str: str = choose_replacment_str(template, match)

        string_list[i] = string_list[i].replace(
            f'name="{match.group(1)}',
            replacment_str,
        )


def validate_input(input_str: str) -> re.Match:
    pattern = r"((\d{1,2})\.(\d{1,2})?\.?(\d{1,2})?)"

    match: re.Match[str] | None = re.search(pattern, input_str)

    if match is None:
        raise Exception(
            "Ваше значение не подходит шаблону!\nВведите корректные даные. Например 5. или 5.1 или 4.2.5 "
        )

    return match


def create_new_bpmn(bpmn_path: str) -> str:
    folder_path: str = os.path.dirname(bpmn_path)
    file_path: str = os.path.join(folder_path, "new.bpmn")
    return file_path


def rewrite_new_bpmn(new_bpmn_path: str, raw_strings: list[str]) -> None:
    with open(new_bpmn_path, "w") as file:
        file.writelines(raw_strings)


if __name__ == "__main__":
    bpmn_path: str = input("Введите путь до файла bpmn:\n")
    string_list: list[str] = strings_from_bpmn(bpmn_path)

    input_str: str = input("С какого пункта начать? Например 5. или 5.1 или 4.2.5\n")

    match: re.Match[str] = validate_input(input_str)

    incriment_strings(string_list, match)
    new_file_path: str = create_new_bpmn(bpmn_path)
    rewrite_new_bpmn(new_file_path, string_list)
