import os


def cleanup_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)
