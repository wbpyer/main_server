import sqlalchemy
import json
from flask import Flask,request,jsonify
from db_server.utils import delete_fdfs
from sqlalchemy.orm import sessionmaker,relationship
from db_server.table import User_excel,Vm_last_status,Base,Status,Date_name,Work_name
from sqlalchemy_utils import database_exists,create_database



app = Flask(__name__)

#这里由两种传参方式，json，还是直接restful
host = '192.168.29.129'
user = 'root'
password = ''
port = 3306



@app.route("/mysql/create",methods=['POST'])
def create_db():
    """
    创建数据库的接口，并可以直接完成表的迁移，这个是给人事用。

    :return:
    """

    data = request.form
    user_id = data.get("id")
    user_name = data.get("name")
    user_role = data.get("role")
    user_work_id = data.get("work_id")
    database = str(user_id) + user_name + str(user_work_id) + user_role

    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    if database_exists(engine.url):
        print(engine.url)

        Base.metadata.drop_all(engine)
        return "数据库存在，清楚成功"

    else:
        create_database(engine.url)
        Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    s = Status(status_name ="草")
    s1 = Status(status_name="报")
    s2 = Status(status_name="副")
    s3 = Status(status_name="垃")
    d1 = Date_name(date_name = "日")
    d2 = Date_name(date_name = "周")
    d3 =Date_name(date_name = "月")
    d4 =Date_name(date_name = "年")
    w1 = Work_name(work_name = "人")
    w2 = Work_name(work_name = "机")
    w3 = Work_name(work_name = "物")
    w4 = Work_name(work_name = "法")

    try :
        session.add_all([s,s1,s2,s3,d1,d2,d3,d4,w1,w2,w3,w4])
        session.commit()
        return "ok",200
    except Exception as e:
        session.rollback()
        print(e,"记录日志")
        return "not ok",404








@app.route("/mysql/excel",methods=['POST'])   # 要拼接一个库名，你不拼，没有办法发请求，对接口，传参方式。
def excel_list():
    '''
    该方法，主要用来去查询文件列表，该用户名下的所有文件列表。
    给客户展示用的，
    同时还要做分组展示返回给前端。现在开发完善这个功能。分组返回数据。

    :param
    :return: 该用户库中所有excel的文件名
    '''

    data = request.form
    user_id = data.get("id")
    user_name = data.get("name")
    user_role = data.get("role")
    user_work_id = data.get("work_id")
    database = str(user_id) + user_name + str(user_work_id) + user_role

    print(database)


    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user,password,host,port,database)
    engine = sqlalchemy.create_engine(conn_str,echo=True)



    #所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()



    books = session.query(User_excel).all()

    d = {str(book.created_date):book.filename for book in books}
    print(d)
    return json.dumps(d)

@app.route("/db/<string:db_name>/excel/delete",methods=['POST'])
def excel_delete(db_name):
    """
    对接虚拟机的垃操作。数据库端做出的一些列反应。
    :param db_name:
    :return:
    """
    data = request.json


    print(data)
    print(db_name)


    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    #下面的参数都是传参数，也就是放在requests里传进来的，filename,path,status,date,work,由虚拟机传过来，user,role,depart登陆之后，这个用户的信息，要有一个token，一直跟到虚拟机，
    #再由虚拟机跟过来。否则，这个是完全解耦合的，你查不到权限库。


    filename = data.get("file_name")
    filepath = data.get("path")
    user_id = data.get("user_id")
    user_name =data.get("user_name")
    role = data.get("role")
    role_id = data.get("role_id")
    department_id = data.get("department_id")
    department = data.get("department")
    status_id = 4


    date_id = data.get("date_id")
    if date_id == "日":
        date_id = 1
    elif date_id =="周":
        date_id = 2
    elif date_id == "月":
        date_id =3
    elif date_id == "年":
        date_id =4

    work_id = data.get("work_id")
    if work_id == "人":
        work_id = 1
    elif work_id =="机":
        work_id = 2
    elif work_id == "物":
        work_id =3
    elif work_id == "法":
        work_id =4
    # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空


    name = session.query(User_excel).filter(User_excel.filename == filename).all()

    if name:
        for i in name:
            print(i.path)
            delete_fdfs(i.path)
            i.path = filepath
            i.status_id = 4
            i.deleted = 1

            try:
                session.add(i)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e, "记录日志")
    else:
        if all([department,department_id]):

            excel = User_excel(filename=filename,path=filepath,deleted = 1,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       department_id=department_id,
                        department = department,
                       status_id=status_id,date_id=date_id,work_id=work_id)
        else:
            excel = User_excel(filename=filename,path=filepath,deleted = 1,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       status_id=status_id,date_id=date_id,work_id=work_id)
        try:
            session.add(excel)
            session.commit()
            return "ok",200
        except Exception as e:
            session.rollback()
            print(e,"记录日志")
            return "not ok",404

@app.route("/db/<string:db_name>/excel/add",methods=['POST'])
def excel_add(db_name):
    """
    目前还没有 完成这个功能，但是我的思路是绝对无敌的。先放下，现在开始开发虚拟机端。
    这个的基础功能实现了，但是添加记录时候的所有，都应该是请求传进来的，不是固定的，所以，这个先放一放，不急。
    考虑到，fdfs冗余问题，这里也要加个FDFS去客户端里面删除东西。
    :param db_name:
    :return:
    """
    data = request.json


    print(data)
    print(db_name)


    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    #下面的参数都是传参数，也就是放在requests里传进来的，filename,path,status,date,work,由虚拟机传过来，user,role,depart登陆之后，这个用户的信息，要有一个token，一直跟到虚拟机，
    #再由虚拟机跟过来。否则，这个是完全解耦合的，你查不到权限库。


    filename = data.get("file_name")
    filepath = data.get("path")
    user_id = data.get("user_id")
    user_name =data.get("user_name")
    role = data.get("role")
    role_id = data.get("role_id")
    department_id = data.get("department_id")
    department = data.get("department")
    status_id = data.get("status_id")
    if status_id == "草":
        status_id = 1
    elif status_id =="报":
        status_id = 2
    elif status_id == "副":
        status_id =3
    elif status_id == "垃":
        status_id =4


    date_id = data.get("date_id")
    if date_id == "日":
        date_id = 1
    elif date_id =="周":
        date_id = 2
    elif date_id == "月":
        date_id =3
    elif date_id == "年":
        date_id =4

    work_id = data.get("work_id")
    if work_id == "人":
        work_id = 1
    elif work_id =="机":
        work_id = 2
    elif work_id == "物":
        work_id =3
    elif work_id == "法":
        work_id =4
    # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空


    name = session.query(User_excel).filter(User_excel.filename == filename).all()

    if name:
        for i in name:
            print(i.path)
            delete_fdfs(i.path)
            i.path = filepath
            try:
                session.add(i)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e, "记录日志")
    else:
        if all([department,department_id]):

            excel = User_excel(filename=filename,path=filepath,deleted = 0,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       department_id=department_id,
                        department = department,
                       status_id=status_id,date_id=date_id,work_id=work_id)
        else:
            excel = User_excel(filename=filename,path=filepath,deleted = 0,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       status_id=status_id,date_id=date_id,work_id=work_id)
        try:
            session.add(excel)
            session.commit()
            return "ok",200
        except Exception as e:
            session.rollback()
            print(e,"记录日志")
            return "not ok",404


@app.route("/db/<string:db_name>/excel/add/leader",methods=['POST'])
def excel_add_leader(db_name):
    """
    上报功能时候，替领导添加数据，但是有一点，不能更新，而是新建，
    因为上报上来的，删不删，得领导自己决定，
    考虑到，fdfs冗余问题，这里也要加个FDFS去客户端里面删除东西。
    :param db_name:
    :return:
    """
    data = request.json
    print(data)
    print(db_name)
    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    #下面的参数都是传参数，也就是放在requests里传进来的，filename,path,status,date,work,由虚拟机传过来，user,role,depart登陆之后，这个用户的信息，要有一个token，一直跟到虚拟机，
    #再由虚拟机跟过来。否则，这个是完全解耦合的，你查不到权限库。


    filename = data.get("file_name")
    filepath = data.get("path")
    user_id = data.get("user_id")
    user_name =data.get("user_name")   #这里能体现出是谁报送上来的。
    role = data.get("role")
    role_id = data.get("role_id")
    department_id = data.get("department_id")
    department = data.get("department")
    status_id = 1  # 报上去的，在领导那里，体现的只能是草里面。


    date_id = data.get("date_id")
    if date_id == "日":
        date_id = 1
    elif date_id =="周":
        date_id = 2
    elif date_id == "月":
        date_id =3
    elif date_id == "年":
        date_id =4

    work_id = data.get("work_id")
    if work_id == "人":
        work_id = 1
    elif work_id =="机":
        work_id = 2
    elif work_id == "物":
        work_id =3
    elif work_id == "法":
        work_id =4

    # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空



    if all([department,department_id]):

        excel = User_excel(filename=filename,path=filepath,deleted = 0,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       department_id=department_id,
                        department = department,
                       status_id=status_id,date_id=date_id,work_id=work_id)


    else:
        excel = User_excel(filename=filename,path=filepath,deleted = 0,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       status_id=status_id,date_id=date_id,work_id=work_id)
    try:
        session.add(excel)
        session.commit()
        return "ok",200
    except Exception as e:
        session.rollback()
        print(e,"记录日志")
        return "not ok",404





@app.route("/mysql/<string:db_name>/excel/find",methods=['POST'])
def vm_latest_find(db_name):
    # data = request.json
    #
    # role = data.get("role")
    # user_name = data.get('user_name')
    # user_id = data.get('user_id')
    # job_id = data.get("job_id")
    # db_name = str(user_id) + user_name + str(job_id) + role
    print(db_name)

    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    """这里是固定的逻辑，就是查这张表中，最后一次记录里的地址返回来就行。"""
    v = session.query(Vm_last_status).order_by(Vm_last_status.id).limit(1).one()
    # print(session.query(User).filter(User.username != 'budong').order_by(User.username).all())

    print(v.filename)
    if json.dumps(v):
        return json.dumps(v.filename)
    else:
        return json.dumps(None)  # null





@app.route("/db/<string:db_name>/vm_latest/add",methods=['POST'])
def vm_latest_add(db_name):
    """
    目前还没有 完成这个功能，但是我的思路是绝对无敌的。先放下，现在开始开发虚拟机端。
    这个的基础功能实现了，但是添加记录时候的所有，都应该是请求传进来的，不是固定的，所以，这个先放一放，不急。
    :param db_name:
    :return:
    """
    data = request.json


    print(data)
    print(db_name)


    database = db_name
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
    Session = sessionmaker(bind=engine)
    session = Session()
    #下面的参数都是传参数，也就是放在requests里传进来的，filename,path,status,date,work,由虚拟机传过来，user,role,depart登陆之后，这个用户的信息，要有一个token，一直跟到虚拟机，
    #再由虚拟机跟过来。否则，这个是完全解耦合的，你查不到权限库。


    filename = data.get("file_name")
    filepath = data.get("path")
    user_id = data.get("user_id")
    user_name =data.get("user_name")
    role = data.get("role")
    role_id = data.get("role_id")
    department_id = data.get("department_id")
    department = data.get("department")


    if all([department,department_id]):

        vml = Vm_last_status(filename=filename,path=filepath,deleted = 0,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       department_id=department_id,
                        department = department,
                       )
    else:
        vml = Vm_last_status(filename=filename,path=filepath,deleted = 0,
                       user_id=user_id,user_name = user_name,role=role,
                       role_id= role_id,
                       )




    try:
        session.add(vml)
        session.commit()
        return "ok",200
    except Exception as e:
        session.rollback()
        print(e,"记录日志")
        return "not ok",404




if __name__ == '__main__':
    print(app.url_map)
    app.run()









