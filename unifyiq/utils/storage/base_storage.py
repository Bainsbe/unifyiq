from utils.security_utils import SecurityUtils


class BaseStorage:
    def __init__(self) -> None:
        self.security_utils = SecurityUtils()

    def write_line(self, file_name, data):
        raise NotImplementedError

    def read_file(self, file_name):
        raise NotImplementedError

    def close_all_write_files(self):
        raise NotImplementedError
