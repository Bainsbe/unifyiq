import configparser
from pathlib import Path

home_dir = str(Path.home())
config = configparser.ConfigParser()
out = config.read(f"{home_dir}/unifyiq.ini")
SUPPORTED_DB_ENGINES = {'mysql': 'mysql+mysqlconnector'}


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
