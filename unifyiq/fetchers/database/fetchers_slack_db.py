from contextlib import contextmanager

from sqlalchemy import Table, Column, String, MetaData, PrimaryKeyConstraint, Boolean, update, and_, text, bindparam
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker

from utils import configs

metadata = MetaData()

fetchers_slack_channel_members = Table('fetchers_slack_channel_members', metadata,
                                       Column('channel_id', String(45), nullable=False),
                                       Column('member_id', String(45), nullable=False),
                                       Column('is_active', Boolean, nullable=False),
                                       PrimaryKeyConstraint('channel_id', 'member_id'))

fetchers_slack_channel_info = Table('fetchers_slack_channel_info', metadata,
                                    Column('channel_id', String(45), primary_key=True),
                                    Column('name', String(80), nullable=False),
                                    Column('topic', String(256), nullable=False),
                                    Column('purpose', String(256), nullable=False),
                                    Column('is_archived', Boolean, nullable=False),
                                    Column('is_private', Boolean, nullable=False),
                                    Column('is_channel', Boolean, nullable=False),
                                    Column('is_group', Boolean, nullable=False),
                                    Column('is_im', Boolean, nullable=False),
                                    Column('is_mpim', Boolean, nullable=False))

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


def get_current_channel_info():
    """
    Get active current channel info from database
    :return:
    """
    with session_scope() as session:
        channel_info = {}
        curr_channel_info = session.query(fetchers_slack_channel_info).all()
        for c in curr_channel_info:
            channel_info[c.channel_id] = {"channel_id": c.channel_id,
                                          "name": c.name,
                                          "topic": c.topic,
                                          "purpose": c.purpose,
                                          "is_archived": c.is_archived,
                                          "is_private": c.is_private,
                                          "is_channel": c.is_channel,
                                          "is_group": c.is_group,
                                          "is_im": c.is_im,
                                          "is_mpim": c.is_mpim}
        return channel_info


def insert_channel_info_to_db(data):
    """
    Insert channel info into database
    :param data: List of dicts with channel_id, name, topic, purpose, is_archived, is_private, is_channel, is_group, is_im, is_mpim
    :return:
    """
    with session_scope() as session:
        count = 0
        insert_statement = insert(fetchers_slack_channel_info).values(channel_id=":channel_id",
                                                                      name=":name",
                                                                      topic=":topic",
                                                                      purpose=":purpose",
                                                                      is_archived=":is_archived",
                                                                      is_private=":is_private",
                                                                      is_channel=":is_channel",
                                                                      is_group=":is_group",
                                                                      is_im=":is_im",
                                                                      is_mpim=":is_mpim")
        for d in data:
            session.execute(insert_statement, {"channel_id": d['channel_id'],
                                               "name": d['name'],
                                               "topic": d['topic'],
                                               "purpose": d['purpose'],
                                               "is_archived": d['is_archived'],
                                               "is_private": d['is_private'],
                                               "is_channel": d['is_channel'],
                                               "is_group": d['is_group'],
                                               "is_im": d['is_im'],
                                               "is_mpim": d['is_mpim']})
            count += 1
            if (count % 1000) == 0:
                session.commit()
        session.commit()


def update_channel_info_to_db(data):
    """
    Update channel info in database
    :param data: List of dicts with channel_id, name, topic, purpose, is_archived, is_private, is_channel, is_group, is_im, is_mpim
    :return:
    """
    with session_scope() as session:
        count = 0
        update_statement = (
            update(fetchers_slack_channel_info)
            .where(text("channel_id = :channel_id"))
            .values(name=":name",
                    topic=":topic",
                    purpose=":purpose",
                    is_archived=":is_archived",
                    is_private=":is_private",
                    is_channel=":is_channel",
                    is_group=":is_group",
                    is_im=":is_im",
                    is_mpim=":is_mpim"))
        for d in data:
            session.execute(update_statement, {"channel_id": d['channel_id'],
                                               "name": d['name'],
                                               "topic": d['topic'],
                                               "purpose": d['purpose'],
                                               "is_archived": d['is_archived'],
                                               "is_private": d['is_private'],
                                               "is_channel": d['is_channel'],
                                               "is_group": d['is_group'],
                                               "is_im": d['is_im'],
                                               "is_mpim": d['is_mpim']})
            count += 1
            if (count % 1000) == 0:
                session.commit()
        session.commit()


def get_current_channel_membership():
    """
    Get active current channel membership from database
    :return: Dict with (channel_id, member_id) -> False as key -> value
    """
    with session_scope() as session:
        membership = {}
        curr_memberships = session.query(fetchers_slack_channel_members).where(
            fetchers_slack_channel_members.c.is_active == True).all()
        for m in curr_memberships:
            membership[(m.channel_id, m.member_id)] = False
        return membership


def insert_channel_membership(data):
    """
    Insert channel membership into the database
    :param data: List of dicts with channel_id and member_id
    :return:
    """
    with session_scope() as session:
        count = 0
        insert_statement = insert(fetchers_slack_channel_members).values(channel_id=bindparam('channel_id'),
                                                                         member_id=bindparam('member_id'),
                                                                         is_active=True)
        for d in data:
            session.execute(insert_statement, {"channel_id": d['channel_id'], "member_id": d['member_id']})
            count += 1
            if (count % 1000) == 0:
                session.commit()
        session.commit()


def delete_channel_membership(data):
    """
    Delete channel membership from the database by marking is_active as False
    :param data: List of dicts with channel_id and member_id
    :return:
    """
    with session_scope() as session:
        count = 0
        update_statement = (
            update(fetchers_slack_channel_members)
            .where(and_(fetchers_slack_channel_members.c.channel_id == bindparam('b_channel_id'),
                        fetchers_slack_channel_members.c.member_id == bindparam('b_member_id')))
            .values(is_active=False)
        )
        for d in data:
            session.execute(update_statement, {"b_channel_id": d['channel_id'], "b_member_id": d['member_id']})
            count += 1
            if (count % 1000) == 0:
                session.commit()
        session.commit()
