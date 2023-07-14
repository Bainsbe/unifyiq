import datetime
import time

from croniter import croniter

from core.update_core import init_vector_store, update_index
from fetchers.update_fetchers import update_fetchers
from utils.configs import get_cron_schedule
from utils.database import unifyiq_config_db


def run_application(version):
    configs = unifyiq_config_db.get_fetcher_configs()
    current_date_hod = version.strftime("%Y-%m-%dT%H-%M-00")
    vector_store = init_vector_store()
    for config in configs:
        update_fetchers(config, current_date_hod)
        update_index(vector_store, config, current_date_hod)


cron_expression = get_cron_schedule()
cron = croniter(cron_expression)

# Infinite loop to continuously check if it's time to run the application
while True:
    next_run = cron.get_next(datetime.datetime)
    wait_seconds = (next_run - datetime.datetime.now()).total_seconds()
    print("Next run: ", next_run, " Sleeping for ", wait_seconds, " seconds")
    time.sleep(wait_seconds)
    run_application(next_run)
