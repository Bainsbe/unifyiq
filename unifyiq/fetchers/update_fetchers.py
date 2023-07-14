# Read the list of adapters from the database and launch them
from datetime import datetime

from fetchers.adapters.slack.slack_adapter import SlackAdapter
from utils import constants
from utils.database import unifyiq_config_db
from utils.file_utils import get_fetcher_output_path_from_config


def update_fetchers(source_config, current_date_hod):
    print(f"Fetching data for {source_config.name} - {source_config.connector_type}")
    if source_config.connector_type == constants.SLACK:
        adapter = SlackAdapter(source_config, current_date_hod)
        adapter.fetcher()
    print(f"Done fetching data from {source_config.name} to {get_fetcher_output_path_from_config(source_config, current_date_hod)}")


if __name__ == '__main__':
    configs = unifyiq_config_db.get_fetcher_configs()
    current_date_hod = datetime.now().strftime("%Y-%m-%dT00-00-00")
    for config in configs:
        update_fetchers(config, current_date_hod)
