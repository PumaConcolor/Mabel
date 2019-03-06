import os
from abc import ABC
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


starred = Table(
    'starred',
    Base.metadata,
    Column('file_id', String(36), ForeignKey('files.id')),
    Column('user_id', String(36), ForeignKey('users.id'))
)


files_tags = Table(
    'files_tags',
    Base.metadata,
    Column('file_id', String(36), ForeignKey('files.id')),
    Column('tag_id', String(36), ForeignKey('tags.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True)
    username = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    files = relationship('File', secondary=starred)

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class File(Base):
    __tablename__ = 'files'

    id = Column(String(36), primary_key=True)
    path = Column(Text, nullable=False)

    tags = relationship('Tag', secondary=files_tags)

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String(36), primary_key=True)
    description = Column(String(64), unique=True, nullable=False)
    category = Column(String(64), nullable=False)

    files = relationship('File', secondary=files_tags)

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class DatabaseConnector(ABC):

    def __init__(self, path):
        engine = create_engine(path)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._db = Session()

    def db(self):
        return self._db


class SQLiteConnetor(DatabaseConnector):

    def __init__(self, path):
        path = 'sqlite:///' + os.path.join(path, 'index.db')
        super().__init__(path)
