import sqlalchemy
import json
from flask import Flask,request,jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from db_server.table import User_excel,Vm_last_status


app = Flask(__name__)

#这里由两种传参方式，json，还是直接restful
host = '192.168.29.129'
user = 'root'
password = ''
port = 3306



@app.route("/mysql/<string:db_name>/excel",methods=['GET'])
def excel_list(db_name):
    '''
    该方法，主要用来去查询文件列表，该用户名下的所有文件列表。
    初

    :param db_name: 库名
    :return: 该用户库中所有excel的文件名
    '''


    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user,password,host,port,database)
    engine = sqlalchemy.create_engine(conn_str,echo=True)


    #所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()



    books = session.query(User_excel).all()

    d = {str(book.created_date):book.filename for book in books}
    print(d)
    return json.dumps(d)



@app.route("/mysql/<string:db_name>/excel/add",methods=['GET'])
def excel_add(db_name):
    """
    目前还没有 完成这个功能，但是我的思路是绝对无敌的。先放下，现在开始开发虚拟机端。
    这个的基础功能实现了，但是添加记录时候的所有，都应该是请求传进来的，不是固定的，所以，这个先放一放，不急。
    :param db_name:
    :return:
    """
    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    #下面的参数都是传参数，也就是放在requests里传进来的，filename,path,status,date,work,由虚拟机传过来，user,role,depart登陆之后，这个用户的信息，要有一个token，一直跟到虚拟机，
    #再由虚拟机跟过来。否则，这个是完全解耦合的，你查不到权限库。
    excel = User_excel(filename="传奇",path="123fdsajkljl321",deleted = 0,user_id=2,role_id=3,depart_id=2,status_id=2,date_id=3,work_id=4)



    try:
        session.add(excel)
        session.commit()
        return "ok",200
    except Exception as e:
        session.rollback()
        print(e,"记录日志")
        return "not ok",404

@app.route("/mysql/<string:db_name>/excel/find",methods=['GET'])
def vm_latest_find(db_name):


    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    """这里是固定的逻辑，就是查这张表中，最后一次记录里的地址返回来就行。"""
    books = session.query(Vm_last_status).order_by(Vm_last_status.id)
    # print(session.query(User).filter(User.username != 'budong').order_by(User.username).all())
    d = {str(book.created_date): book.filename for book in books}
    print(d)
    return json.dumps(d)








if __name__ == '__main__':
    print(app.url_map)
    app.run()









