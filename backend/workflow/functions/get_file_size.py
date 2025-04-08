import os


def get_file_size_label(value: int | None = None):
    if value is None:
        return None
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if value < 1024:
            return f'{value:.1f} {unit}'
        value /= 1024
    return None


def get_file_size(file_path: str):
    try:
        return os.path.getsize(file_path)
    except Exception:
        return None


def get_file_size_label_by_path(file_path: str):
    return get_file_size_label(get_file_size(file_path))
