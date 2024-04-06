def rewrite_new_bpmn(new_bpmn_path: str, raw_strings: list[str]) -> None:
    with open(new_bpmn_path, "w") as file:
        file.writelines(raw_strings)
