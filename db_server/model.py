

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text


Base = declarative_base()
class Manage(Base):

    """一人一库管理表，记录所有的库信息"""
    __tablename__ = "manage"
    id = Column(Integer, primary_key=True)
    dbname = Column(String(64), nullable=False)
    depart_id = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)



