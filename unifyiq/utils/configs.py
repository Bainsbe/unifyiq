import configparser
from pathlib import Path

from utils.constants import SUPPORTED_STORAGE_TYPES

home_dir = str(Path.home())
SUPPORTED_DB_ENGINES = {'mysql': 'mysql+mysqlconnector'}


def reload_config():
    """Reloads the config file `unifyiq.ini`."""
    global config
    config = configparser.ConfigParser()
    config.read(f"{home_dir}/unifyiq.ini")


# Load the config file on import
reload_config()


def get_unifyiq_output_path():
    """Returns the output path from the config file `unifyiq.ini`."""
    return config.get('UnifyIQ', 'output_path')


def get_log_dir():
    """Returns the log dir from the config file `unifyiq.ini`."""
    return config.get('UnifyIQ', 'log_dir')


def get_admin_emails():
    """Returns the admin emails from the config file `unifyiq.ini`."""
    return config.get('UnifyIQ', 'admin_emails').split(',') if config.get('UnifyIQ', 'admin_emails') else []


def get_log_level():
    """Returns the log level from the config file `unifyiq.ini`."""
    return config.get('UnifyIQ', 'log_level', fallback='INFO')


def get_cron_schedule():
    """Returns the cron schedule from the config file `unifyiq.ini`."""
    return config.get('UnifyIQ', 'cron_schedule', fallback="0 0 * * *")


def get_storage_type():
    """Returns the storage type from the config file `unifyiq.ini`."""
    storage_type = config.get('UnifyIQ', 'storage_type')
    if storage_type not in SUPPORTED_STORAGE_TYPES:
        raise ValueError(f"Unsupported storage type {storage_type}")
    return storage_type


def get_database_url():
    """Constructs the database url from config file `unifyiq.ini` and returns it."""
    host = config.get('Database', 'host')
    port = config.getint('Database', 'port')
    username = config.get('Database', 'username')
    password = config.get('Database', 'password')
    name = config.get('Database', 'name')
    engine = config.get('Database', 'engine')
    if engine not in SUPPORTED_DB_ENGINES:
        raise ValueError(f"Unsupported engine {engine}")
    return f"{SUPPORTED_DB_ENGINES[engine]}://{username}:{password}@{host}:{port}/{name}"


def get_milvus_uri():
    """Constructs the milvus uri from config file `unifyiq.ini` and returns it."""
    host = config.get('Milvus', 'host')
    port = config.getint('Milvus', 'port')
    return f"{host}:{port}"


def delete_index_always():
    return config.getboolean('Milvus', 'delete_index_always')


def get_embedding_model():
    """Returns the embedding model name from config file `unifyiq.ini`."""
    return config.get('Embeddings', 'model', fallback='multi-qa-mpnet-base-dot-v1')


def get_embedding_dimension():
    """Returns the embedding dimension from config file `unifyiq.ini`."""
    return config.getint('Embeddings', 'dimension', fallback=768)


def get_open_ai_api_key():
    """Returns the openai api key from config file `unifyiq.ini`."""
    return config.get('LLM', 'open_ai_api_key')


def get_slack_app_token():
    """Returns the slack app token from config file `unifyiq.ini`."""
    return config.get('Slackbot', 'app_token')


def get_slack_bot_token():
    """Returns the slack bot token from config file `unifyiq.ini`."""
    return config.get('Slackbot', 'bot_token')


def get_slack_client_signature():
    """Returns the slack client signature from config file `unifyiq.ini`."""
    return config.get('Slackbot', 'client_signature')


def get_confluence_email_address():
    """Returns the confluence email address from config file `unifyiq.ini`."""
    return config.get('Confluence', 'email_address')


def get_confluence_api_key():
    """Returns the confluence api key from config file `unifyiq.ini`."""
    return config.get('Confluence', 'api_key')


def get_confluence_site():
    """Returns the confluence site(organization) name from config file `unifyiq.ini`."""
    return config.get('Confluence', 'site')


def get_security_key():
    """Returns the security key from config file `unifyiq.ini`."""
    return config.get('Security', 'security_key')


def get_storage_encryption_key():
    """Returns the encryption key from config file `unifyiq.ini`."""
    return config.get('Security', 'storage_encryption_key')
