
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text
from sqlalchemy.orm import sessionmaker,relationship



"""数据库端，所有一人一库表的定义，都放在这里，方便复用，
分离出来不和主模块冲突"""



Base = declarative_base()
class User_excel(Base):
    '''用户文件表'''
    __tablename__ = 'user_excel'

    id = Column(Integer, primary_key=True)
    filename = Column(String(64), nullable=False)
    path = Column(String(200), nullable=False, unique=True)
    fgroup = Column(String(60),nullable=False)  # 用来放文件的分组，后加字段
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    deleted = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String(20),nullable=False)
    role = Column(String(20), nullable=False)
    role_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=True)
    department = Column(String(20),nullable=True)
    read = Column(Integer, nullable=True)
    any = Column(String(20), nullable=True)
    status_id = Column(Integer, ForeignKey("status.id"))
    status = relationship("Status",back_populates= "exceles")
    date_id = Column(Integer, ForeignKey("date_name.id"))
    date = relationship("Date_name", back_populates="exceles")

    # 外键关系
    work_id = Column(Integer, ForeignKey("work_name.id"))
    work =  relationship("Work_name", back_populates="exceles")


    # file_type = Column(Integer,ForeignKey("file_type.id"),nullable=True)


    # def __repr__(self):
    #     return "{}id={} name{} ".format(self.__class__.__name__,self.id,
    #                                          self.filename)




class Vm_last_status(Base):
    '''用户最后一次状态表'''
    __tablename__ = 'vm_latest_status'

    id = Column(Integer, primary_key=True)
    filename = Column(String(64), nullable=False)
    path = Column(String(256), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    deleted = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String(20),nullable=False)
    role = Column(String(20), nullable=True)
    role_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=True)
    department = Column(String(20),nullable=True)
    read = Column(Integer, nullable=True)
    leader = Column(String(20), nullable=True)
    # status_id
    # date_id
    # work_id


class Status(Base):
    '''
    状态表，草， 报，拉
    '''
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    status_name = Column(String(5), nullable=False)
    # 下面这个不是字段，是为了方便查询，反向查询，比如某一个状态下有多少个表，就可以利用这个区查询。
    exceles = relationship("User_excel", back_populates="status")



class Date_name(Base):
    """
    日期类型表, 日，周，月
    """
    __tablename__ = "date_name"
    id = Column(Integer, primary_key=True)
    date_name = Column(String(5), nullable=False)
    exceles = relationship("User_excel", back_populates="date")


class Work_name(Base):
    """
    工作类型表, 人，机，物，法
    """
    __tablename__ = "work_name"
    id = Column(Integer, primary_key=True)
    work_name = Column(String(5), nullable=False)

    exceles = relationship("User_excel", back_populates="work")



# class File_type(Base):
#     """
#     文件类型表
#
#     """
#     __tablename__= "file_type"
#
#     id = Column(Integer, primary_key=True)
#     file_type = Column(String(5), nullable=False)
#
#     # exceles = relationship("User_excel", back_populates="work")
#
#





