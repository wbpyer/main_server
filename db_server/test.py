import sqlalchemy
import json
from flask import Flask,request,jsonify

from sqlalchemy.orm import sessionmaker,relationship
from db_server.table import User_excel,Vm_last_status,Base
from sqlalchemy_utils import database_exists,create_database




host = '192.168.29.129'
user = 'root'
password = ''
port = 3306
database = '761bili0012安全员'

conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
engine = sqlalchemy.create_engine(conn_str, echo=True)
filename = "11.18.txt"

Session = sessionmaker(bind=engine)
session = Session()


name = session.query(User_excel).filter(User_excel.filename =="11.1800000.txt" ).all()
print(name)
if name:
    for i in name:
        print(i.path)
        i.path = "我被更改了"
        try:
            session.add(i)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e, "记录日志")

# for i in name:
#     print(i)
