from pathlib import Path

FILEPATH = Path(__file__).with_name("todos.txt")


def _ensure_file_exists(filepath: Path) -> None:
    if not filepath.exists():
        filepath.write_text("", encoding="utf-8")


def get_todos(filepath=FILEPATH):
    """
    Return a list of todos (each line includes a trailing newline).
    Creates the file if it does not exist.
    """
    filepath = Path(filepath)
    _ensure_file_exists(filepath)

    with open(filepath, "r", encoding="utf-8") as file:
        return file.readlines()


def write_todos(todos_arg, filepath=FILEPATH):
    """
    Overwrite the todos file with the list of lines provided.
    """
    filepath = Path(filepath)
    _ensure_file_exists(filepath)

    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(todos_arg)