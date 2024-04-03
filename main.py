import re

from BPMN_Incrimenter import BPMN_Incrimenter
from utils.create_new_bpmn import create_new_bpmn
from utils.get_strings_from_bpmn import get_strings_from_bpmn
from utils.rewrite_new_bpmn import rewrite_new_bpmn
from utils.validate_input import validate_input

if __name__ == "__main__":
    bpmn_path: str = input("Введите путь до файла bpmn:\n")
    string_list: list[str] = get_strings_from_bpmn(bpmn_path)

    user_input: str = input("С какого пункта начать? Например 5. или 5.1 или 4.2.5\n")

    match: re.Match[str] = validate_input(user_input)
    incrimenter = BPMN_Incrimenter(match)
    incrimenter.incriment_strings(string_list)
    new_file_path: str = create_new_bpmn(bpmn_path)
    rewrite_new_bpmn(new_file_path, string_list)
