import os
import shutil

SCREENSHOTS_DIRECTORY = "/mnt/c/Users/antho/OneDrive/Pictures/Screenshots"

def get_newest_screenshot() -> str:
    files = [f for f in os.listdir(SCREENSHOTS_DIRECTORY) if f.endswith('.png')]
    if not files:
        return None
    newest_file = max(files, key=lambda f: os.path.getctime(os.path.join(SCREENSHOTS_DIRECTORY, f)))
    return newest_file

def list_categories() -> str:
    categories = ""
    for category in os.listdir(SCREENSHOTS_DIRECTORY):
        category_path = os.path.join(SCREENSHOTS_DIRECTORY, category)
        if os.path.isdir(category_path):
            categories += f"{category}\n"
    return categories

def create_directory(directory_name: str) -> None:
    new_directory_path = os.path.join(SCREENSHOTS_DIRECTORY, directory_name)
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

def rename_and_move_screenshot(filename: str, new_name: str) -> None:
    source_path = os.path.join(SCREENSHOTS_DIRECTORY, filename)
    destination_path = os.path.join(SCREENSHOTS_DIRECTORY, new_name)
    shutil.move(source_path, destination_path)