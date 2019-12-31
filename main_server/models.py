import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker






Base = declarative_base()
class Ip_table(Base):

    """一人一库管理表，记录所有的库信息"""
    __tablename__ = "ip_tbl"
    id = Column(Integer, primary_key=True)
    ip = Column(String(64), nullable=False)
    status = Column(Integer, nullable=False)
    role = Column(String(64), nullable=False)


if __name__ == '__main__':
    host = '172.16.13.1'
    user = 'root'
    password = '123456'
    port = 3306

    database = 'manage_table'
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()
    # Base.metadata.create_all(engine)

    s1 = Ip_table(ip='172.16.14.1',role='安全员',status = 0)
    s2 = Ip_table(ip='172.16.14.2', role='安全管理员', status=0)
    s3 = Ip_table(ip='172.16.14.3', role='安全巡查员', status=0)
    s4 = Ip_table(ip='172.16.14.4', role='巡查员', status=0)
    s5 = Ip_table(ip='172.16.14.5', role='', status=0)
    s6 = Ip_table(ip='172.16.14.6', role='', status=0)
    s7 = Ip_table(ip='172.16.14.7', role='', status=0)
    s8 = Ip_table(ip='172.16.14.8', role='', status=0)
    s9 = Ip_table(ip='172.16.14.9', role='', status=0)
    s10 = Ip_table(ip='172.16.14.10', role='', status=0)
    s11 = Ip_table(ip='172.16.14.11', role='', status=0)
    s12 = Ip_table(ip='172.16.14.12', role='', status=0)
    try:

        session.add_all([ s1, s2, s3, s4,s5,s6,s7,s8,s9,s10,s11,s12])
        session.commit()
    except Exception as e:
        session.rollback()
        print(e, "记录日志")
