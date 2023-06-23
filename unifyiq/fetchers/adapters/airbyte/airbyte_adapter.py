import json
import os
from abc import abstractmethod

from utils.constants import AIRBYTE
from fetchers.adapters.base_adapter import BaseAdapter
from utils.file_utils import get_jsonl_files, get_files_glob


class AirbyteAdapter(BaseAdapter):
    @abstractmethod
    def __init__(self, config, version):
        super().__init__(config, version)

    def fetch_data(self):
        src_files = get_files_glob(self.config.src_path, '_airbyte_raw_*.jsonl')
        tmp_path = self.config.dest_path + "/" + AIRBYTE + "/" + self.config.name + "/" + self.version
        for file in src_files:
            new_name = tmp_path + "/" + file.name
            os.renames(file, new_name)
        # in case we need to rerun the fetcher
        src_files = get_jsonl_files(tmp_path)
        for file in src_files:
            self.parse_jsonl(file)
        self.close_files()

    @abstractmethod
    def parse_jsonl(self, jsonl_file):
        pass


def get_airbyte_data(json_line):
    data = json.loads(json_line)
    # Assuming all other sources will have this
    return data.get('_airbyte_data')
