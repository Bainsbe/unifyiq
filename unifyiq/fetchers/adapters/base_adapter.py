import json
from abc import ABCMeta, abstractmethod

from jsonschema import validate, ValidationError

from utils.file_utils import get_fetcher_output_path_from_config

ID = "id"
PARENT_ID = "parent_id"
TEXT = "text"
URL = "url"
USER = "user"
GROUP = "group"
CREATED_AT = "created_at"
LAST_UPDATED_AT = "last_updated_at"

schema = {
    "type": "object",
    "properties": {
        ID: {"type": "string"},
        PARENT_ID: {"type": "string"},
        TEXT: {"type": "string"},
        URL: {"type": "string"},
        USER: {"type": "string"},
        GROUP: {"type": "string"},
        CREATED_AT: {"type": "integer"},
        LAST_UPDATED_AT: {"type": "integer"}
    },
    "required": [ID, PARENT_ID, TEXT, URL, USER, GROUP, CREATED_AT, LAST_UPDATED_AT]
}


class BaseAdapter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, config, version):
        self.config = config
        self.version = version
        self.output_path = get_fetcher_output_path_from_config(config, version)
        self.output_files = {}

    @abstractmethod
    def fetch_data(self):
        pass

    def validate_and_write_json(self, json_data, file_name):
        if file_name not in self.output_files:
            self.output_files[file_name] = open(f"{self.output_path}/{file_name}.jsonl", 'w')
        try:
            validate(json_data, schema)
        except ValidationError as e:
            raise f"Validation error: {e}"
        else:
            self.output_files[file_name].write(json.dumps(json_data) + "\n")

    def close_files(self):
        for file in self.output_files.values():
            file.close()

    def set_required_values_in_json(self, json_data, id_str, parent_id, text, url, user, group, created_at,
                                    last_updated_at):
        json_data[ID] = id_str
        json_data[PARENT_ID] = parent_id
        json_data[TEXT] = text
        json_data[URL] = url
        json_data[USER] = user
        json_data[GROUP] = group
        json_data[CREATED_AT] = created_at
        json_data[LAST_UPDATED_AT] = last_updated_at
