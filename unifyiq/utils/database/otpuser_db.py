from contextlib import contextmanager

from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from utils import configs

metadata = MetaData()

user_otp = Table('user_otps', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('email', String(255), nullable=False),
                 Column('otp', String(6), nullable=False),
                 Column('created_at', TIMESTAMP, nullable=False, server_default=func.now()),
                 Column('is_verified', Boolean, nullable=False))

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


def get_user(email):
    with session_scope() as session:
        user = session.query(user_otp).filter(user_otp.c.email == email).first()
        if user != None:
            return {
                'id': user.id,
                'email': user.email,
                'otp': user.otp,
                'created_at': user.created_at,
                'is_verified': user.is_verified
            }
        return user


def add_user_otp(email, otp, is_verified):
    with session_scope() as session:
        try:
            new = user_otp.insert().values(email=email, otp=otp, is_verified=is_verified)
            session.execute(new)
            session.commit()
            print('New fetcher configuration added successfully')
        except IndentationError as e:
            session.rollback()
            raise Exception(f'Error adding new fetcher configuration: {str(e)}')


def update_user_otp(email, otp, now):
    with session_scope() as session:
        try:
            # update = update(user_otp).where(user_otp.c.email == email).values(otp=otp)
            session.query(user_otp).filter(user_otp.c.email == email).update({'otp': otp, 'created_at': now})
            session.commit()
            print('New fetcher configuration added successfully')
        except IndentationError as e:
            session.rollback()
            raise Exception(f'Error adding new fetcher configuration: {str(e)}')


def update_user_verified(email, is_verified):
    with session_scope() as session:
        try:
            # update = update(user_otp).where(user_otp.c.email == email).values(is_verified=is_verified)
            session.query(user_otp).filter(user_otp.c.email == email).update({'is_verified': is_verified})
            session.commit()
            print('New fetcher configuration added successfully')
        except IndentationError as e:
            session.rollback()
            raise Exception(f'Error adding new fetcher configuration: {str(e)}')
