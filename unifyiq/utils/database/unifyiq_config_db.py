from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import configs

metadata = MetaData()

fetchers_configs = Table('unifyiq_configs', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(45), nullable=False),
                         Column('connector_platform', String(45), nullable=False),
                         Column('connector_type', String(45), nullable=False),
                         Column('src_storage_type', String(45), nullable=False),
                         Column('src_path', String(255), nullable=False),
                         Column('dest_storage_type', String(45), nullable=False),
                         Column('dest_path', String(255), nullable=False),
                         Column('url_prefix', String(255), nullable=False),
                         Column('cron_expr', String(2048), nullable=False),
                         Column('last_fetched_ts', Integer, nullable=False),
                         Column('is_enabled', Boolean, nullable=False))

engine = create_engine(configs.get_database_url())
Session = sessionmaker(bind=engine)
session = Session()


def get_fetcher_configs():
    return session.query(fetchers_configs).where(fetchers_configs.c.is_enabled == True).all()
