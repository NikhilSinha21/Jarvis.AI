import os
import re
import shutil
from features.jarvis_voice import JarvisVoice

class FileManager:
    _base_path = os.path.join(os.getcwd(), "Jarvis_Managed_Files")
    
    def __init__(self):
        os.makedirs(self._base_path, exist_ok=True)
        self._current_path = self._base_path

    def _get_full_path(self, item_name):
        return os.path.join(self._current_path, item_name)

    def process_command(self, command: str):
        command_lower = command.lower().replace(" dot ", ".").strip()
        
        create_match = re.search(r'create a (folder|file) (?:named )?(.+)', command_lower)
        delete_match = re.search(r'delete (?:the )?(.+)', command_lower)
        rename_match = re.search(r'rename (.+) to (.+)', command_lower)
        move_match = re.search(r'move (.+) to (.+)', command_lower)
        list_match = re.search(r'list files|show files', command_lower)
        change_dir_match = re.search(r'go to (.+)|change directory to (.+)', command_lower)
        read_file_match = re.search(r'read file(?: named)? (.+)', command_lower)
        edit_file_match = re.search(r'edit file (.+) line (\d+) to (.+)', command_lower)
        append_file_match = re.search(r'append to file (.+) with (.+)', command_lower)

        if create_match:
            item_type = create_match.group(1).strip()
            item_name = create_match.group(2).strip()
            if item_type == "folder":
                self.create_folder(item_name)
            elif item_type == "file":
                self.create_file(item_name)
                
        elif delete_match:
            item_name = delete_match.group(1).strip()
            self.delete_item(item_name)
            
        elif rename_match:
            old_name = rename_match.group(1).strip()
            new_name = rename_match.group(2).strip()
            self.rename_item(old_name, new_name)
            
        elif move_match:
            source_name = move_match.group(1).strip()
            destination_name = move_match.group(2).strip()
            self.move_item(source_name, destination_name)

        elif read_file_match:
            file_name = read_file_match.group(1).strip()
            self.read_file(file_name)

        elif edit_file_match:
            file_name = edit_file_match.group(1).strip()
            line_number = int(edit_file_match.group(2).strip())
            new_content = edit_file_match.group(3).strip()
            self.edit_file_line(file_name, line_number, new_content)

        elif append_file_match:
            file_name = append_file_match.group(1).strip()
            content = append_file_match.group(2).strip()
            self.append_to_file(file_name, content)

        elif list_match:
            self.list_items()

        elif change_dir_match:
            path = next(group for group in change_dir_match.groups() if group is not None).strip()
            self.change_directory(path)
            
        else:
            JarvisVoice.speak("I'm sorry, I couldn't understand that file management command.")

    def create_folder(self, folder_name: str):
        full_path = self._get_full_path(folder_name)
        try:
            os.makedirs(full_path, exist_ok=False)
            output = f"Folder '{folder_name}' created successfully."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
        except FileExistsError:
            output = f"Folder '{folder_name}' already exists."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
        except OSError as e:
            output = f"Error creating folder '{folder_name}': {e}"
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")

    def create_file(self, file_name: str):
        full_path = self._get_full_path(file_name)
        try:
            with open(full_path, 'w') as f:
                f.write('')
            output = f"File '{file_name}' created successfully."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
        except FileExistsError:
            output = f"File '{file_name}' already exists."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
        except OSError as e:
            output = f"Error creating file '{file_name}': {e}"
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")

    def delete_item(self, item_name: str):
        full_path = self._get_full_path(item_name)
        if not os.path.exists(full_path):
            output = f"Item '{item_name}' does not exist."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
            return
        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
                output = f"File '{item_name}' deleted successfully."
                JarvisVoice.speak(output)
                print(f"[File Manager] {output}")
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
                output = f"Folder '{item_name}' and its contents deleted successfully."
                JarvisVoice.speak(output)
                print(f"[File Manager] {output}")
        except OSError as e:
            output = f"Error deleting '{item_name}': {e}"
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")

    def rename_item(self, old_name: str, new_name: str):
        old_path = self._get_full_path(old_name)
        new_path = self._get_full_path(new_name)
        if not os.path.exists(old_path):
            JarvisVoice.speak(f"I cannot find an item named '{old_name}'.")
            return
        if os.path.exists(new_path):
            JarvisVoice.speak(f"An item named '{new_name}' already exists.")
            return
        try:
            os.rename(old_path, new_path)
            JarvisVoice.speak(f"Renamed '{old_name}' to '{new_name}'.")
            print(f"[File Manager] Renamed '{old_name}' to '{new_name}'.")
        except OSError as e:
            JarvisVoice.speak(f"Error renaming '{old_name}': {e}")
            print(f"[File Manager] Error renaming '{old_name}': {e}")

    def move_item(self, source_name: str, destination_name: str):
        source_path = self._get_full_path(source_name)
        destination_path = self._get_full_path(destination_name)
        if not os.path.exists(source_path):
            JarvisVoice.speak(f"I cannot find an item named '{source_name}'.")
            return
        if not os.path.exists(destination_path) or not os.path.isdir(destination_path):
            JarvisVoice.speak(f"The destination '{destination_name}' is not a valid folder.")
            return
        try:
            shutil.move(source_path, destination_path)
            JarvisVoice.speak(f"Moved '{source_name}' to '{destination_name}'.")
            print(f"[File Manager] Moved '{source_name}' to '{destination_path}'.")
        except shutil.Error as e:
            JarvisVoice.speak(f"Error moving '{source_name}': {e}")
            print(f"[File Manager] Error moving '{source_name}': {e}")

    def list_items(self):
        try:
            contents = os.listdir(self._current_path)
            if not contents:
                JarvisVoice.speak("The folder is empty.")
                return
            JarvisVoice.speak("Here are the contents of the current folder.")
            for item in contents:
                JarvisVoice.speak(item)
                print(f"[File Manager] - {item}")
        except OSError as e:
            JarvisVoice.speak(f"Error listing files: {e}")
            print(f"[File Manager] Error listing files: {e}")

    def change_directory(self, path: str):
        if path == "parent" or path == "up":
            if self._current_path == self._base_path:
                JarvisVoice.speak("You are already in the base directory.")
            else:
                self._current_path = os.path.dirname(self._current_path)
                JarvisVoice.speak(f"Moved up to '{os.path.basename(self._current_path)}'.")
                print(f"[File Manager] Current directory is '{self._current_path}'.")
            return

        new_path = self._get_full_path(path)
        if os.path.isdir(new_path):
            self._current_path = new_path
            JarvisVoice.speak(f"Changed directory to '{path}'.")
            print(f"[File Manager] Current directory is '{self._current_path}'.")
        else:
            JarvisVoice.speak(f"Cannot find a directory named '{path}'.")
    
    def _read_file_lines(self, file_path):
        """Helper to read file lines safely."""
        if not os.path.exists(file_path):
            JarvisVoice.speak(f"Error: The file '{os.path.basename(file_path)}' does not exist.")
            return None
        if not os.path.isfile(file_path):
            JarvisVoice.speak(f"Error: '{os.path.basename(file_path)}' is not a file.")
            return None
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            return lines
        except Exception as e:
            JarvisVoice.speak(f"An error occurred while reading the file: {e}")
            return None

    def read_file(self, file_name: str):
        full_path = self._get_full_path(file_name)
        lines = self._read_file_lines(full_path)
        if lines is not None:
            JarvisVoice.speak(f"Reading file '{file_name}':")
            for i, line in enumerate(lines, 1):
                JarvisVoice.speak(f"Line {i}: {line.strip()}")
                print(f"[File Manager] Line {i}: {line.strip()}")

    def edit_file_line(self, file_name: str, line_number: int, new_content: str):
        full_path = self._get_full_path(file_name)
        lines = self._read_file_lines(full_path)
        if lines is None:
            return

        if not 1 <= line_number <= len(lines):
            JarvisVoice.speak(f"Error: Line {line_number} is out of range. The file has {len(lines)} lines.")
            return

        lines[line_number - 1] = new_content + "\n"
        
        try:
            with open(full_path, 'w') as f:
                f.writelines(lines)
            output = f"Successfully updated line {line_number} in '{file_name}'."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
        except Exception as e:
            output = f"Error writing to file '{file_name}': {e}"
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
    
    def append_to_file(self, file_name: str, content: str):
        full_path = self._get_full_path(file_name)
        if not os.path.exists(full_path):
            JarvisVoice.speak(f"Error: The file '{file_name}' does not exist. Creating it now.")
            self.create_file(file_name)
        if not os.path.isfile(full_path):
            JarvisVoice.speak(f"Error: '{file_name}' is not a file. Cannot append content.")
            return

        try:
            with open(full_path, 'a') as f:
                f.write(content + "\n")
            output = f"Successfully appended content to '{file_name}'."
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
        except Exception as e:
            output = f"Error appending to file '{file_name}': {e}"
            JarvisVoice.speak(output)
            print(f"[File Manager] {output}")
