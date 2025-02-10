import os
class FileOperation:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        try:
            if not os.path.exists(self.file_name):
                with open(self.file_name, 'x'):
                    pass  # File creation is silent
        except Exception as e:
            raise Exception(f"Error creating file: {e}")

    def write_file(self, content: str) -> None:
        with open(self.file_name, 'a') as file:
            file.write(content.replace('\n', '') + '\n')

    def read_file(self) -> str:
        if not self.file_name:
            return "No file selected."
        try:
            with open(self.file_name, 'r') as file:
                content = file.read()
                return content if content else "The file is empty."
        except FileNotFoundError:
            return f"File '{self.file_name}' does not exist."

    def clear_file_content(self) -> str:
        if not self.file_name:
            return "No file selected."
        try:
            with open(self.file_name, 'r+') as file:
                content = file.read()
                if content:
                    file.truncate(0)
                    return "File contents cleared."
                else:
                    return "File is already empty."
        except FileNotFoundError:
            return f"File '{self.file_name}' does not exist."

    def update_file_content(self, line_number: int, new_content: str) -> str:
        if not self.file_name:
            return "No file selected."
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
            if not lines:
                return "File is empty."
            lines[line_number - 1] = new_content + '\n'
            with open(self.file_name, 'w') as file:
                file.writelines(lines)
            return f"Line {line_number} updated."
        except (IndexError, ValueError):
            return "Invalid line number."
        except FileNotFoundError:
            return f"File '{self.file_name}' does not exist."

    def delete_file(self) -> str:
        if not self.file_name:
            return "No file selected."
        try:
            os.remove(self.file_name)
            self.file_name = None
            return "File deleted."
        except FileNotFoundError:
            return f"File '{self.file_name}' does not exist."