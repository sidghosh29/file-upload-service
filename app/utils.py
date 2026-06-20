import uuid
from pathlib import Path
import shutil


def generate_storage_filename(filename: str) -> str:
    file_uuid = str(uuid.uuid4())
    file_extension = "".join(Path(filename).suffixes)
    return f"{file_uuid}{file_extension}"


def empty_folder(folder_path: str | Path):
    path = Path(folder_path)

    # Safety check: Ensure the directory actually exists
    if not path.exists():
        print(f"The directory {path} does not exist.")
        return

    # Iterate through everything inside the folder
    for item in path.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()  # Deletes files or symlinks
            elif item.is_dir():
                shutil.rmtree(item)  # Deletes subfolders and their contents
        except Exception as e:
            print(f"Failed to delete {item}. Reason: {e}")


def quick_empty_folder(folder_path: str | Path):
    path = Path(folder_path)
    if path.exists():
        shutil.rmtree(path)  # Blows away the entire directory
    path.mkdir(parents=True, exist_ok=True)  # Recreates it fresh
