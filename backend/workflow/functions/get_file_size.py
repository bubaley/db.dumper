import os


def get_file_size(file_path: str):
    try:
        file_size = os.path.getsize(file_path)
        for unit in ['B', 'K', 'M', 'G', 'T']:
            if file_size < 1024:
                return f'{file_size:.1f}{unit}'
            file_size /= 1024
    except FileNotFoundError:
        return 'Invalid'
