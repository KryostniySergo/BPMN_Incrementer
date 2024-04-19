import re

from BPMN_Incrimenter import BPMN_Incrimenter
from utils.create_new_bpmn import create_new_bpmn
from utils.get_strings_from_bpmn import get_strings_from_bpmn
from utils.rewrite_new_bpmn import rewrite_new_bpmn
from utils.validate_input import validate_input


def do_one() -> None:
    user_input: str = input("С какого пункта начать? Например 5. или 5.1 или 4.2.5\n")
    match: re.Match[str] = validate_input(user_input)
    BPMN_Incrimenter(match).incriment_strings(string_list)
    new_file_path: str = create_new_bpmn(bpmn_path)
    rewrite_new_bpmn(new_file_path, string_list)


def do_range() -> None:
    start = int(input("С какого пункта начать? Например 5 или 8\n"))
    end = int(input("До кокого пункта? Например 5 или 8\n"))

    while end >= start:
        match: re.Match[str] = validate_input(f"{end}.")
        BPMN_Incrimenter(match).incriment_strings(string_list)
        end -= 1

    new_file_path: str = create_new_bpmn(bpmn_path)
    rewrite_new_bpmn(new_file_path, string_list)


if __name__ == "__main__":
    bpmn_path: str = input("Введите путь до файла bpmn:\n")
    string_list: list[str] = get_strings_from_bpmn(bpmn_path)

    match input("Как вы хотите обработать bpmn? 1: Определенный пункт 2: Диапозон\n"):
        case "1":
            do_one()
        case "2":
            do_range()
