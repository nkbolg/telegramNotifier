from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import db_name

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    Id = Column(Integer, primary_key=True)
    username = Column(String)
    telegram_id = Column(Integer)


eng = create_engine(db_name, connect_args={'check_same_thread': False}, echo=False)
Base.metadata.bind = eng
Base.metadata.create_all()
Session = sessionmaker(bind=eng)


def add_user(username, user_id):
    assert isinstance(username, str)
    assert isinstance(user_id, int)
    ses = Session()
    if ses.query(User).filter(User.username == username).count() == 0:
        ses.add(User(username=username, telegram_id=user_id))
        ses.commit()


def get_user(username):
    assert isinstance(username, str)
    ses = Session()
    return ses.query(User).filter(User.username == username).first()
