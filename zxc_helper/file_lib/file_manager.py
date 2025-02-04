import os
from typing import List, Optional

class FileManager:
    def __init__(self, root_folder: str):
        """
        Initialize the FileManager with a root folder.
        """
        self.root_folder = root_folder

    def get_all_files_and_subfolders(self) -> List[str]:
        """
        Get all files and subfolders in the root folder.
        Returns a list of absolute paths.
        """
        all_paths = []
        for root, dirs, files in os.walk(self.root_folder):
            for dir_name in dirs:
                all_paths.append(os.path.join(root, dir_name))
            for file_name in files:
                all_paths.append(os.path.join(root, file_name))
        return all_paths

    def delete_all_files_in_folder(self, folder_path: Optional[str] = None) -> None:
        """
        Delete all files in the specified folder (or root folder if not specified).
        """
        if folder_path is None:
            folder_path = self.root_folder

        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

    def search_files_by_keyword(self, keyword: str) -> List[str]:
        """
        Search for files in the root folder whose names contain the keyword.
        Returns a list of absolute paths.
        """
        matching_files = []
        for root, dirs, files in os.walk(self.root_folder):
            for file_name in files:
                if keyword.lower() in file_name.lower():
                    matching_files.append(os.path.join(root, file_name))
        return matching_files

    def search_files_by_extension(self, extension: str) -> List[str]:
        """
        Search for files in the root folder with the specified extension.
        Returns a list of absolute paths.
        """
        matching_files = []
        for root, dirs, files in os.walk(self.root_folder):
            for file_name in files:
                if file_name.lower().endswith(extension.lower()):
                    matching_files.append(os.path.join(root, file_name))
        return matching_files

# Example usage:
if __name__ == "__main__":
    # Initialize the FileManager with a root folder
    root_folder = "example_folder"
    file_manager = FileManager(root_folder)

    # Create example folder and files for testing
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
        with open(os.path.join(root_folder, "test1.txt"), "w") as f:
            f.write("This is a test file.")
        with open(os.path.join(root_folder, "test2.docx"), "w") as f:
            f.write("This is another test file.")
        os.makedirs(os.path.join(root_folder, "subfolder"))
        with open(os.path.join(root_folder, "subfolder", "test3.txt"), "w") as f:
            f.write("This is a test file in a subfolder.")

    # Get all files and subfolders
    print("All files and subfolders:")
    for path in file_manager.get_all_files_and_subfolders():
        print(path)

    # Search files by keyword
    print("\nFiles containing 'test':")
    for path in file_manager.search_files_by_keyword("test"):
        print(path)

    # Search files by extension
    print("\nFiles with '.txt' extension:")
    for path in file_manager.search_files_by_extension(".txt"):
        print(path)

    # Delete all files in the root folder
    print("\nDeleting all files in the root folder...")
    file_manager.delete_all_files_in_folder()

    # Verify deletion
    print("\nRemaining files and subfolders:")
    for path in file_manager.get_all_files_and_subfolders():
        print(path)