import os


def create_new_bpmn(bpmn_path: str) -> str:
    folder_path: str = os.path.dirname(bpmn_path)
    file_path: str = os.path.join(folder_path, "new.bpmn")
    return file_path
