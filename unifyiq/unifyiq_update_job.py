import datetime
import sys
import time

from croniter import croniter

from core.update_core import init_vector_store, update_index
from fetchers.update_fetchers import update_fetchers
from utils.configs import get_cron_schedule, reload_config, get_env
from utils.database import unifyiq_config_db
from utils.log_util import get_logger

logger = get_logger(__name__)


def run_application(version):
    try:
        logger.info("Getting fetcher config")
        source_configs = unifyiq_config_db.get_fetcher_configs()
        reload_config()
        current_date_hod = version.strftime("%Y-%m-%dT%H-%M-00")
        logger.info("Initializing vector store for non dev env")
        if get_env() != "dev":
            vector_store = init_vector_store()
        for source_config in source_configs:
            logger.info("Fetching for:" + source_config.connector_type)
            update_fetchers(source_config, current_date_hod)
            logger.info("Updating index for:" + source_config.connector_type)
            if get_env() != "dev":
                update_index(vector_store, source_config, current_date_hod)
    except Exception as e:
        logger.error("Error updating index: {}".format(e))


cron_expression = get_cron_schedule()
cron = croniter(cron_expression)


def start_cron():
    # Infinite loop to continuously check if it's time to run the application
    while True:
        next_run = cron.get_next(datetime.datetime)
        wait_seconds = (next_run - datetime.datetime.now()).total_seconds()
        print("Next run: ", next_run, " Sleeping for ", wait_seconds, " seconds")
        time.sleep(wait_seconds)
        run_application(next_run)


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) > 1 and arguments[1] == "test":
        run_application(cron.get_prev(datetime.datetime))
    else:
        start_cron()
