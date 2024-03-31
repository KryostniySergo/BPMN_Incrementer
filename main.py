import os
import re


def strings_from_bpmn(bpmn_path: str) -> list[str]:
    raw_lines: list[str] = []

    with open(bpmn_path, "r", encoding="utf-8") as file:
        raw_lines = file.readlines()

    return raw_lines


def matches_strings(lines: list[str]) -> list[str]:
    pattern = r"name=\"((\d{1,2})\.?(\d{1,2})?\.?(\d{1,2})?)"

    matches: list[str] = []
    for line in lines:
        match: re.Match[str] | None = re.search(pattern, line)
        if match:
            matches.append(match.string)

    return matches


def sort_string_list(bpmn_path: str) -> list[str]:
    raw_lines = strings_from_bpmn(bpmn_path)

    raw_pattern = r"name=\"((\d{1,2})\.?(\d{1,2})?\.?(\d{1,2})?)"

    raw_matches: list[re.Match] = []
    for line in raw_lines:
        match: re.Match[str] | None = re.search(raw_pattern, line)
        if match:
            # raw_matches.append(match.group(0))
            raw_matches.append(match)

    # Можно убрать
    sorted_matches: list[re.Match] = sorted(raw_matches, key=lambda x: int(x.group(2)))
    sorted_strings: list[str] = []
    [sorted_strings.append(string.group(0)) for string in sorted_matches]
    return sorted_strings


def choose_pattern(template: re.Match) -> str:
    first_number: str = template.group(2)
    second_number: str = template.group(3)
    last_number: str = template.group(4)

    if last_number:
        return r"(" + first_number + r"\." + second_number + r"\.?(\d{1,2})?)"
    elif second_number:
        return r"[^\.](" + first_number + r"\.?(\d{1,2})?)"
    else:
        return r"[^\.]((" + first_number + r")\.)"


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


def incriment_strings(sorted_string: list[str], template: re.Match) -> None:
    pattern: str = choose_pattern(template)

    for i in range(len(sorted_string)):
        match: re.Match | None = re.search(pattern, sorted_string[i])
        if match is None:
            continue
        if retry_or_continue(template, match):
            continue

        replacment_str: str = choose_replacment_str(template, match)

        sorted_string[i] = sorted_string[i].replace(
            f'name="{match.group(1)}',
            replacment_str,
        )


def create_new_bpmn(bpmn_path: str, incremented_strings: list[str]) -> None:
    folder_path = os.path.dirname(bpmn_path)
    file_name = os.path.join(folder_path, "new.bpmn")
    with open(file_name, "w") as file:
        file.writelines(incremented_strings)


if __name__ == "__main__":
    bpmn_path = (
        "G:\\BPNM_UPDATE\\diagram.bpmn"  # input("Введите путь до файла bpmn:\n")
    )
    raw_lines: list[str] = strings_from_bpmn(bpmn_path)
    matches: list[str] = matches_strings(raw_lines)
    # sorted_string: list[str] = sort_string_list(bpmn_path)

    start_point: str = (
        "5."  # input("С какого пункта начать? Например 5. или 5.1 или 4.2.5\n")
    )
    pattern = r"((\d{1,2})\.(\d{1,2})?\.?(\d{1,2})?)"

    template: re.Match[str] | None = re.search(pattern, start_point)

    if template is None:
        raise Exception("Кал")

    # Full string => 4.1.2
    # 0-> 4.1.2 | 1-> 4.1.2 | 2-> 4 | 3-> 1 | 4-> 2
    incriment_strings(matches, template)

    # TODO -> КАК ТО НАУЧИТСЯ ЗАМЕНЯТЬ СТРОКИ

    # for replaced_str in matches:
    #     for line in raw_lines:

    create_new_bpmn(bpmn_path, matches)
