from abc import ABC

from utils.storage.base_storage import BaseStorage


class LocalFileSystemStorage(BaseStorage, ABC):
    def __init__(self):
        super().__init__()
        self.write_files = {}

    def write_line(self, full_path, data):
        if full_path not in self.write_files:
            self.write_files[full_path] = open(full_path, 'w')  # Open the file in text mode for writing
        encrypted_data = self.security_utils.encrypt(data)
        self.write_files[full_path].write(encrypted_data + '\n')  # Append a newline character

    def read_file(self, full_path):
        lines = []
        with open(full_path, 'r') as file:
            for line in file:  # Iterates over the lines of the file
                line = line.strip()
                if line == '':
                    continue  # Skip empty lines
                try:
                    lines.append(self.security_utils.decrypt(line))  # Decrypt line and append it to the list
                except ValueError as e:  # Catch the specific error caused by invalid lines
                    print(f'Failed to decrypt line "{line}": {str(e)}')
        return lines  # Return the list of decrypted lines

    def close_all_write_files(self):
        for file in self.write_files.values():
            file.close()
        self.write_files.clear()
