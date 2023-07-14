import json
from abc import ABCMeta, abstractmethod

from jsonschema import validate, ValidationError

from utils.database.unifyiq_config_db import update_last_fetched_ts
from utils.file_utils import get_fetcher_output_path_from_config
from utils.log_util import get_logger
from utils.time_utils import get_prev_cron_ts

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


def get_end_ts_from_cron_expr(last_fetched_ts, cron_expr):
    """
    Returns the timestamp in seconds for the end of the current fetch window. It will be max of the following:
    1. The timestamp for previous execution of the cron job + 1 second
    2. The timestamp for the last fetch + 1 second
    For the first run window will be a lot bigger than the subsequent windows as it has to start from beginning of time.
    # TODO: Handle if big window size is a problem.
    """
    prev_exp_run = get_prev_cron_ts(cron_expr) + 1
    return max(last_fetched_ts + 1, prev_exp_run)


class BaseAdapter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, source_config, version, logger=get_logger(__name__)):
        self.source_config = source_config
        self.version = version
        self.logger = logger
        if source_config.last_fetched_ts > 0:
            self.start_ts = source_config.last_fetched_ts
        else:
            self.start_ts = source_config.start_ts
        self.end_ts = get_end_ts_from_cron_expr(source_config.last_fetched_ts, source_config.cron_expr)
        self.output_path = get_fetcher_output_path_from_config(source_config, version)
        self.output_files = {}

    @abstractmethod
    def fetch_and_save_raw_data(self):
        pass

    @abstractmethod
    def load_metadata_from_db(self):
        """
        Load metadata from the database to determine the current state.
        """
        pass

    @abstractmethod
    def save_metadata_to_db(self):
        """
        Save metadata to the database with the updated state after the current fetch.
        """
        pass

    def fetcher(self):
        self.load_metadata_from_db()
        self.fetch_and_save_raw_data()
        self.save_metadata_to_db()
        self.close_files()
        update_last_fetched_ts(self.source_config, self.end_ts)

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
