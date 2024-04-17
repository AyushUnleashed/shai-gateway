import os
from pydantic import FilePath, DirectoryPath

def get_all_pose_names(directory_path: DirectoryPath) -> list[FilePath]:
    # Check if the directory exists
    if not os.path.exists(directory_path):
        return None

    # Get a list of all files in the directory
    files = os.listdir(directory_path)

    # Filter the list to include only image files (you can customize this filter)
    image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    return image_files
    