import os


def remove_local_file(path: str):
    try:
        os.remove(path)
        return True
    except (FileNotFoundError, FileExistsError):
        return False
