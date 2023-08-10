# Read the list of adapters from the database and launch them
from datetime import datetime

from fetchers.adapters.confluence.confluence_adapter import ConfluenceAdapter
from fetchers.adapters.slack.slack_adapter import SlackAdapter
from utils import constants
from utils.database import unifyiq_config_db
from utils.file_utils import get_fetcher_output_path_from_config
from utils.log_util import get_logger

logger = get_logger(__name__)

def update_fetchers(source_config, current_date_hod):
    logger.info(f"Fetching data for {source_config.name} - {source_config.connector_type}")
    adapter = None
    if source_config.connector_type == constants.SLACK:
        logger.info("Initializing Slack Adapter")
        try:
            adapter = SlackAdapter(source_config, current_date_hod)
            logger.info("Initialized SlackAdapter")
        except Exception as e:
            logger.error("Error initializing Slack Adapter: {}".format(e))
    elif source_config.connector_type == constants.CONFLUENCE:
        try:
            adapter = ConfluenceAdapter(source_config, current_date_hod)
            logger.info("Initialized ConfluenceAdapter")
        except Exception as e:
            logger.error("Error initializing ConfluenceAdapter: {}".format(e))
    else:
        logger.error(f"Unknown connector type: {source_config.connector_type}")

    if adapter is not None:
        try:
            logger.info("Calling fetch on:{}".format(adapter))
            adapter.fetcher()
            logger.info(
                f"Done fetching data from {source_config.name} to {get_fetcher_output_path_from_config(source_config, current_date_hod)}")
        except Exception as e:
            logger.error("Error fetching: {}".format(e))
    else:
        logger.info("No adapter found, nothing to fetch")



if __name__ == '__main__':
    configs = unifyiq_config_db.get_fetcher_configs()
    current_date_hod = datetime.now().strftime("%Y-%m-%dT00-00-00")
    for config in configs:
        update_fetchers(config, current_date_hod)
