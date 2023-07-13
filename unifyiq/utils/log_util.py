import logging
import os.path
from logging.handlers import TimedRotatingFileHandler

from utils.configs import get_log_dir, get_log_level


def get_logger(name):
    log_dir = get_log_dir()
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger(name)
    logger.setLevel(get_log_level())
    handler = TimedRotatingFileHandler(log_dir + '/app.log', when='midnight', backupCount=180)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
