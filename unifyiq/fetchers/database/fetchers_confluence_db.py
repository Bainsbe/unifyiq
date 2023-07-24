from contextlib import contextmanager

from sqlalchemy import Table, Column, String, MetaData, update, Integer, and_, bindparam
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker

from utils import configs

metadata = MetaData()

fetchers_confluence_page_info = Table('fetchers_confluence_page_info', metadata,
                                      Column('page_id', String(45), primary_key=True),
                                      Column('space_key', String(80), nullable=False),
                                      Column('topic', String(512), nullable=False),
                                      Column('author_email', String(80), nullable=False),
                                      Column('last_modified_time', Integer, nullable=False),
                                      Column('status', String(10), nullable=False))

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


def get_page_id(space_key, page_id):
    return f"{space_key}-{page_id}"


def get_current_page_info():
    """
    Get active current page info from database
    :return:
    """
    with session_scope() as session:
        page_info = {}
        curr_page_info = session.query(fetchers_confluence_page_info).all()
        for c in curr_page_info:
            page_info[get_page_id(c.space_key, c.page_id)] = {"page_id": c.page_id,
                                                              "space_key": c.space_key,
                                                              "topic": c.topic,
                                                              "author_email": c.author_email,
                                                              "last_modified_time": c.last_modified_time,
                                                              "status": c.status}
        return page_info


def insert_page_info_to_db(data):
    """
    Insert page info into database
    :param data: List of dicts with page_id, space_key, topic, author_email, last_modified_time, status
    :return:
    """
    with session_scope() as session:
        count = 0
        insert_statement = insert(fetchers_confluence_page_info).values(
            page_id=":page_id",
            space_key=":space_key",
            topic=":topic",
            author_email=":author_email",
            last_modified_time=":last_modified_time",
            status=":status"
        )
        for d in data:
            session.execute(insert_statement, {"page_id": d['page_id'],
                                               "space_key": d['space_key'],
                                               "topic": d['topic'],
                                               "author_email": d['author_email'],
                                               "last_modified_time": d['last_modified_time'],
                                               "status": d['status']})
            count += 1
            if (count % 1000) == 0:
                session.commit()
        session.commit()


def update_page_info_to_db(data):
    """
    Update page info in database
    :param data: List of dicts with page_id, space_key, topic, author_email, last_modified_time, status
    :return:
    """
    with session_scope() as session:
        count = 0
        update_statement = (
            update(fetchers_confluence_page_info)
            .where(and_(fetchers_confluence_page_info.c.page_id == bindparam('b_page_id'),
                        fetchers_confluence_page_info.c.space_key == bindparam('b_space_key')))
            .values(
                topic=":topic",
                author_email=":author_email",
                last_modified_time=":last_modified_time",
                status=":status"
            ))
        for d in data:
            session.execute(update_statement, {"b_page_id": d['page_id'],
                                               "b_space_key": d['space_key'],
                                               "topic": d['topic'],
                                               "author_email": d['author_email'],
                                               "last_modified_time": d['last_modified_time'],
                                               "status": d['status']})
        count += 1
        if (count % 1000) == 0:
            session.commit()
        session.commit()
