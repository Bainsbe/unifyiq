import json
from contextlib import contextmanager

from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, update
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fetchers.adapters.fetcher_configs import *
from utils import configs

metadata = MetaData()

fetchers_configs = Table('unifyiq_configs', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(45), nullable=False),
                         Column('connector_type', String(45), nullable=False),
                         Column('url_prefix', String(255), nullable=False),
                         # Not Supported, Uses global schedule in unifyiq.ini
                         Column('cron_expr', String(20), nullable=False),
                         Column('start_ts', Integer, nullable=False),
                         Column('config_json', String(2048), nullable=False),
                         Column('last_fetched_ts', Integer, nullable=False),
                         Column('is_enabled', Boolean, nullable=False))

engine = create_engine(configs.get_database_url())


@contextmanager
def session_scope():
    session = sessionmaker(bind=engine)()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_fetcher_configs():
    with session_scope() as session:
        return session.query(fetchers_configs).where(fetchers_configs.c.is_enabled == True).all()


def update_last_fetched_ts(config, last_fetched_ts):
    with session_scope() as session:
        stmt = update(fetchers_configs).where(fetchers_configs.c.id == config.id).values(
            last_fetched_ts=last_fetched_ts)
        session.execute(stmt)
        session.commit()


def add_fetcher_config(name, connector_type, url_prefix, cron_expr, start_ts, last_fetched_ts, is_enabled, config_json):
    with session_scope() as session:
        try:
            new = fetchers_configs.insert().values(name=name, connector_type=connector_type, url_prefix=url_prefix,
                                                   cron_expr=cron_expr, start_ts=start_ts,
                                                   last_fetched_ts=last_fetched_ts,
                                                   is_enabled=is_enabled, config_json=config_json)
            session.execute(new)
            session.commit()
            print('New fetcher configuration added successfully')
        except IndentationError as e:
            session.rollback()
            raise Exception(f'Error adding new fetcher configuration: {str(e)}')


def get_config(config_json, config_name):
    """Returns the value of the config_name from the config json string."""
    json_data = json.loads(config_json)
    return json_data[config_name]


def get_slack_app_token(config_json):
    """Returns the slack app token from config file `unifyiq.ini`."""
    return get_config(config_json, SLACK_APP_TOKEN)


def get_slack_bot_token(config_json):
    """Returns the slack bot token from config file `unifyiq.ini`."""
    return get_config(config_json, SLACK_BOT_TOKEN)


def get_slack_client_signature(config_json):
    """Returns the slack client signature from config file `unifyiq.ini`."""
    return get_config(config_json, SLACK_CLIENT_SIGNATURE)


def get_confluence_email_address(config_json):
    """Returns the confluence email address from config file `unifyiq.ini`."""
    return get_config(config_json, CONFLUENCE_EMAIL_ID)


def get_confluence_api_key(config_json):
    """Returns the confluence api key from config file `unifyiq.ini`."""
    return get_config(config_json, CONFLUENCE_API_KEY)


def get_confluence_site(config_json):
    """Returns the confluence site(organization) name from config file `unifyiq.ini`."""
    return config.get('Confluence', 'site')
