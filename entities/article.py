from sqlalchemy import Column, String, create_engine, INT, VARCHAR, TEXT, MetaData, Table, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import time
import json

# 创建对象的基类:
Base = declarative_base()


class ArticleEntity(Base):
    __tablename__ = 'article'
    meta = MetaData()

    table = Table(
        __tablename__, meta,
        Column('id', Integer, primary_key=True),
        Column('create_time', Integer, default=time.time()),
        Column('update_time', Integer),
        Column('title', VARCHAR(20), nullable=False),
        Column('content', TEXT, nullable=True)
    )

    id = Column(Integer, primary_key=True)
    create_time = Column(Integer, default=time.time())
    update_time = Column(Integer)
    title = Column(VARCHAR(20), nullable=False)
    content = Column(TEXT, nullable=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


