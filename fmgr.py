import os
import shutil
from typing import Callable

class FileListProvider:
    def subset(indices: list[int]) -> list[str]:
        pass


class FileSelection:
    def get_and_reset() -> list[str]:
        pass


class FileSystem:
    def copy(src: str, dest: str) -> None:
        pass

    def move(src: str, dest: str) -> None:
        pass

    def delete(path: str) -> None:
        pass


class StdFileSystem(FileSystem):
    def copy(src: str, dest: str) -> None:
        """Copy a file from src to dest"""
        if os.path.exists(src):
            shutil.copy2(src, dest)

    def move(src: str, dest: str) -> None:
        """Move a file from src to dest"""
        if os.path.exists(src):
            shutil.move(src, dest)

    def delete(path: str) -> None:
        """Delete a file"""
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


class UserInterface:
    def error(msg: str) -> None:
        pass


class ConsoleUI(UserInterface):
    def error(msg: str) -> None:
        print(msg)


class FileSelector(FileSelection):
    def __init__(self):
        self.selected_files = []
    
    def select_files_by_indices(self, indices: list[int], file_explorer: FileListProvider) -> list[str]:
        """Select files based on indices"""
        try:
            selected_indices = [int(i.strip()) for i in indices.split(',')]
            
            self.selected_files = file_explorer.subset(selected_indices)
            
            print("Selected files:")
            for file in self.selected_files:
                print(f" - {os.path.basename(file)}")
            
            return self.selected_files
        except ValueError:
            print("Invalid input. Please enter valid indices.")
            return []
        except Exception as e:
            print(f"Error selecting files: {e}")
            return []
 
    def get_and_reset(self) -> list[str]:
        """Return the list of currently selected files"""
        res = self.selected_files.copy()
        self.selected_files.clear()
        return res


class FileExplorer(FileListProvider):
    def __init__(self):
        self._set_current_path(os.path.expanduser('~'))

    def _set_current_path(self, path: str) -> None:
        """Set current path and update the contents of the current directory"""
        self.current_path = path
        self.current_directory_contents = os.listdir(self.current_path)

    def display_directory_contents(self) -> None:
        """Display contents of the current directory"""
        try:
            print(f"\nCurrent Directory: {self.current_path}")
            print("-" * 50)
            for index, element in enumerate(self.current_directory_contents):
                full_path = os.path.join(self.current_path, element)
                element_type = "📁 Folder" if os.path.isdir(full_path) else "📄 File"
                print(f"{index}. {element_type}: {element}")
        except PermissionError:
            print("Access denied to this directory.")
        except Exception as e:
            print(f"Error: {e}")

    def navigate(self, index: int) -> None:
        """Navigate to a subdirectory"""
        try:
            selected_element = self.current_directory_contents[index]
            full_path = os.path.join(self.current_path, selected_element)
            
            if os.path.isdir(full_path):
                self._set_current_path(full_path)
                self.display_directory_contents()
            else:
                print(f"Cannot open file {selected_element}")
        except Exception as e:
            print(f"Navigation error: {e}")

    def go_to_parent_directory(self) -> None:
        """Move to the parent directory"""
        self._set_current_path(os.path.dirname(self.current_path))
        self.display_directory_contents()

    def subset(self, indices: list[int]) -> list[str]:
        """Return a subset of the current directory contents"""
        selected_files = []
        for index in indices:
            if 0 <= index < len(self.current_directory_contents):
                full_path = os.path.join(self.current_path, self.current_directory_contents[index])
                selected_files.append(full_path)
        return selected_files


class FileManager:
    def __init__(self, file_provider: FileListProvider, fs: FileSystem, ui: UserInterface):
        self.file_provider = file_provider
        self.fs = fs
        self.ui = ui
        
    def _process_files(self, title: str, action: Callable[[str, str], None], destination: str=None) -> int:
        """Process files based on the action"""
        try:
            selected_files = self.file_provider.get_and_reset()
            for file in selected_files:
                action(file, destination)
            return len(selected_files)
        except Exception as e:
            self.ui.error(f"{title}: {e}")
            return 0
        
    def copy_files(self, destination) -> int:
        """Copy selected files"""
        return self._process_files("Copy", self.fs.copy, destination)

    def move_files(self, destination) -> int:
        """Move selected files"""
        return self._process_files("Move", self.fs.move, destination)

    def delete_files(self) -> int:
        """Delete selected files"""
        return self._process_files("Delete", action=lambda path, _ : self.fs.delete(path))


def main_menu():
    file_selector = FileSelector()
    file_manager = FileManager(file_selector, StdFileSystem(), ConsoleUI())
    file_explorer = FileExplorer()
    
    while True:
        print("\n--- File Explorer ---")
        print("1. Display Directory")
        print("2. Navigate")
        print("3. Go to Parent Directory")
        print("4. Select Files")
        print("5. Copy")
        print("6. Move")
        print("7. Delete")
        print("8. Quit")
        
        choice = input("Your choice: ")
        
        try:
            if choice == '1':
                file_explorer.display_directory_contents()
            
            elif choice == '2':
                index = int(input("Enter navigation index: "))
                file_explorer.navigate(index)
            
            elif choice == '3':
                file_explorer.go_to_parent_directory()
            
            elif choice == '4':
                file_explorer.display_directory_contents()
                indices = input("Enter file indices to select (comma-separated): ")
                file_selector.select_files_by_indices(indices, file_explorer)
            
            elif choice == '5':
                dest = input("Enter destination path for copying: ")
                count = file_manager.copy_files(dest)
                print(f"{count} file(s) copied")

            elif choice == '6':
                dest = input("Enter destination path for moving: ")
                count = file_manager.move_files(dest)
                print(f"{count} file(s) moved")
            
            elif choice == '7':
                count = file_manager.delete_files()
                print(f"{count} file(s)/folder(s) deleted")
            
            elif choice == '8':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice")
        
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main_menu()