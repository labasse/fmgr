import os
import shutil

""" File Manager Console Application 
    Generated with Claude 3.5 Haiku
    With 2 prompts : 
        Génère un programme console python qui permet d'explorer les fichiers, 
        en sélectionner pour copier, déplacer et supprimer les fichiers sélectionnés. 
        Une classe "métier" regroupe les fonctions de sélection, copie, déplacement 
        et suppression.

        Deux rectifications : il faudrait passer le code et l'interface en anglais 
        et sortir la sélection de la classe "métier"
"""


class FileSelector:
    def __init__(self):
        self.selected_files = []
    
    def select_files_by_indices(self, indices, file_explorer):
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

    def get_selected_files(self):
        """Return the list of currently selected files"""
        return self.selected_files

    def clear_selection(self):
        """Clear the current file selection"""
        self.selected_files.clear()


class FileExplorer:
    def __init__(self):
        self._set_current_path(os.path.expanduser('~'))

    def _set_current_path(self, path):
        """Set current path and update the contents of the current directory"""
        self.current_path = path
        self.current_directory_contents = os.listdir(self.current_path)

    def display_directory_contents(self):
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

    def navigate(self, index):
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

    def go_to_parent_directory(self):
        """Move to the parent directory"""
        self._set_current_path(os.path.dirname(self.current_path))
        self.display_directory_contents()

    def subset(self, indices):
        """Return a subset of the current directory contents"""
        for index in indices:
            if 0 <= index < len(self.current_directory_contents):
                full_path = os.path.join(self.current_path, self.current_directory_contents[index])
                self.selected_files.append(full_path)
        return self.selected_files


class FileManager:
    def __init__(self):
        self.file_selector = FileSelector()

    def copy_files(self, destination):
        """Copy selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.exists(file):
                    shutil.copy2(file, destination)
            print(f"{len(selected_files)} file(s) copied")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Copy error: {e}")

    def move_files(self, destination):
        """Move selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.exists(file):
                    shutil.move(file, destination)
            print(f"{len(selected_files)} file(s) moved")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Move error: {e}")

    def delete_files(self):
        """Delete selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.isfile(file):
                    os.remove(file)
                elif os.path.isdir(file):
                    shutil.rmtree(file)
            print(f"{len(selected_files)} file(s)/folder(s) deleted")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Delete error: {e}")


def main_menu():
    file_manager = FileManager()
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
                file_manager.file_selector.select_files_by_indices(indices, file_explorer)
            
            elif choice == '5':
                dest = input("Enter destination path for copying: ")
                file_manager.copy_files(dest)
            
            elif choice == '6':
                dest = input("Enter destination path for moving: ")
                file_manager.move_files(dest)
            
            elif choice == '7':
                file_manager.delete_files()
            
            elif choice == '8':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice")
        
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main_menu()