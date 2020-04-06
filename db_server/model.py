from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
import sqlalchemy


Base = declarative_base()
class Manage(Base):

    """一人一库管理表，记录所有的库信息"""
    __tablename__ = "manage"
    id = Column(Integer, primary_key=True)
    dbname = Column(String(64), nullable=False)
    department_id = Column(Integer, nullable=True)

    department = Column(String(64), nullable=False)  #那个部门必须有
    family = Column(String(64), nullable=False)   # 那个层次必须有，第几项目部，或者是公司。
    name = Column(String(64), nullable=False)
    business = Column(String(128), nullable=True)

    any1 = Column(String(128), nullable=True)
    any2 = Column(String(128), nullable=True)
    any3 = Column(String(128), nullable=True)
    any4 = Column(String(128), nullable=True)
    any5 = Column(String(128), nullable=True)

    #一个人可能对着多个业务。


class All_Texts(Base):
    '''虚拟机端我的办公模板库'''
    __tablename__ = 'all_texts'

    id = Column(Integer, primary_key=True)
    textname = Column(String(64), nullable=True)  # 模板名，和业务名字是一样的，都是成套走的。
    path = Column(String(200), nullable=False, unique=True)
    level = Column(String(60),nullable=False)  # 项目部还是公司还是工区
    department = Column(String(60),nullable=False)  # 部门
    business = Column(String(60),nullable=False)  # 业务
    any1 = Column(String(60), nullable=True)
    any2 = Column(String(60), nullable=True)
    any3 = Column(String(60), nullable=True)
    any4 = Column(String(60), nullable=True)
    any5 = Column(String(60), nullable=True)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Model_base(Base):
    '''模板库模板'''
    __tablename__ = 'model_base'

    id = Column(Integer, primary_key=True)
    textname = Column(String(64), nullable=False)  # 模板名，和业务名字是一样的，都是成套走的。
    path = Column(String(200), nullable=False, unique=True)
    level = Column(String(60),nullable=True)  # 项目部还是公司还是工区
    department = Column(String(60),nullable=False)  # 部门
    business = Column(String(60),nullable=True)  # 业务
    file_id = Column(String(60), nullable=True)
    any1 = Column(String(60), nullable=True)
    any2 = Column(String(60), nullable=True)
    any3 = Column(String(60), nullable=True)
    any4 = Column(String(60), nullable=True)
    any5 = Column(String(60), nullable=True)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)


if __name__ == "__main__":
    host = '172.16.240.1'
    user = 'root'
    password = '123456'
    port = 3306
    database = "manage_table"
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)
    # srcfile = "C:\\Users\\Admin\\Desktop\\资料PDF\\机器学习(算法篇).pdf"
    # print(change_filename(srcfile))

    Base.metadata.create_all(engine)
