def get_strings_from_bpmn(bpmn_path: str) -> list[str]:
    string_list: list[str] = []

    with open(bpmn_path, "r", encoding="utf-8") as file:
        string_list = file.readlines()

    return string_list
