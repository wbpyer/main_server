import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
class Ip_table(Base):

    """一人一库管理表，记录所有的库信息,目前满足部了这个需求，这个需要加字段，因为接下来，有各种需求。4个字段肯定不够。"""
    __tablename__ = "ip_tbl_new"
    id = Column(Integer, primary_key=True)
    ip = Column(String(64), nullable=False)
    status = Column(Integer, nullable=False)
    role = Column(String(64), nullable=True)
    business = Column(String(64), nullable=True) #业务字段
    any1 = Column(String(64), nullable=True)
    any2 = Column(String(64), nullable=True)
    any3 = Column(String(64), nullable=True)
    any4 = Column(String(64), nullable=True)



if __name__ == '__main__':
    host = '172.16.240.1'
    user = 'root'
    password = '123456'
    port = 3306

    database = 'manage_table'
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()


    Base.metadata.create_all(engine) #建库
    # Base.metadata.drop_all(engine)  #删除库


    s1 = Ip_table(ip='172.16.240.101',status = 0)
    s2 = Ip_table(ip='172.16.240.102',  status=0)
    s3 = Ip_table(ip='172.16.240.103',  status=0)
    s4 = Ip_table(ip='172.16.240.104', status=0)
    s5 = Ip_table(ip='172.16.240.105', status=0)
    s6 = Ip_table(ip='172.16.240.106',  status=0)
    s7 = Ip_table(ip='172.16.240.107', status=0)
    s8 = Ip_table(ip='172.16.240.108', status=0)
    s9 = Ip_table(ip='172.16.240.109', status=0)
    s10 = Ip_table(ip='172.16.240.110',  status=0)
    s11 = Ip_table(ip='172.16.240.111',  status=0)
    s12 = Ip_table(ip='172.16.240.112',  status=0)



    try:

        session.add_all([ s1, s2, s3, s4,s5,s6,s7,s8,s9,s10,s11,s12])
        session.commit()
    except Exception as e:
        session.rollback()
        print(e, "记录日志")
