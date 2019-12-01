from flask import Blueprint
import sqlalchemy
import json
from flask import Flask,request,jsonify
from sqlalchemy.orm import sessionmaker,relationship
from db_server.models import User_excel,Vm_last_status,Status,Date_name,Work_name,Base
from sqlalchemy_utils import database_exists,create_database
from db_server.manager.model import Manage

mysql = Blueprint('mysql',__name__)



host = '192.168.29.129'
user = 'root'
password = ''
port = 3306





def insert_manage_table(database:str,depart,username):
    """
    向库管理表注入信息，每次有新的库的要录入信息去管理。
    :param database:
    :param depart:
    :return:
    """



    madatabase = "manage_table"
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, madatabase)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()
    # Base.metadata.create_all(engine)
    #
    mange = Manage(dbname =database ,depart_id = depart , name = username)

    try:
        session.add(mange)
        session.commit()

    except Exception as e:
        session.rollback()
        print(e, "记录日志")


def find_db(username):
    """
    查找用户的库名
    :param username:
    :return:
    """


    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, "manage_table")
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    db = session.query(Manage).filter(Manage.name == username).limit(1).one()

    return db.dbname



@mysql.route("/mysql/create",methods=['POST'])
def create_db():
    """
    创建数据库的接口，并可以直接完成表的迁移，同时初始化，默认数据。这个是给人事用。
    #todo 接口1   人事添加用户接口
    :return:
    """

    data = request.form
    user_id = data.get("id")
    user_name = data.get("name")
    user_role = data.get("role")  # 这里和以前的角色内容一样，只不过名字变成了岗位
    user_job_id = data.get("job_id")
    user_department_id = data.get("user_department_id")
    database = str(user_id) + ":" +user_name +":" + str(user_job_id) +":" + user_role

    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    if database_exists(engine.url):
        print(engine.url)

        # Base.metadata.drop_all(engine)
        return "数据库已经存在，"

    else:
        create_database(engine.url)
        Base.metadata.create_all(engine)
        insert_manage_table(database,user_department_id,user_name)

    Session = sessionmaker(bind=engine)
    session = Session()

    s = Status(status_name ="草")
    s1 = Status(status_name="报")
    s2 = Status(status_name="副")
    s3 = Status(status_name="垃")
    s4 = Status(status_name = "收")

    d1 = Date_name(date_name = "日")
    d2 = Date_name(date_name = "周")
    d3 = Date_name(date_name = "旬")
    d4 =Date_name(date_name = "月")
    d5 =Date_name(date_name = "季")
    d6 = Date_name(date_name = "半")
    d7 = Date_name(date_name = "年")

    w1 = Work_name(work_name = "人")
    w2 = Work_name(work_name = "机")
    w3 = Work_name(work_name = "物")
    w4 = Work_name(work_name = "法")

    try :
        session.add_all([s,s1,s2,s3,s4,d1,d2,d3,d4,d5,d6,d7,w1,w2,w3,w4])
        session.commit()
        return "ok",200
    except Exception as e:
        session.rollback()
        print(e,"记录日志")
        return "not ok",404



@mysql.route("/mysql/finename",methods = ['POST'])
def find_name():
    """
    第一次请求，找到他部门下的所有员工姓名，列出来。这个是动态的，但是先不用这个接口，前端意思是写死的。
    # todo 3 暂未启用。以后再说。
    :return:
    """
    data = request.form
    user_department_id = data.get("id")

    madatabase = "manage_table"
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, madatabase)
    engine = sqlalchemy.create_engine(conn_str, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    peoples = session.query(Manage).filter(Manage.id == user_department_id).all()
    try:

        d = {i:peo.name for i,peo in  enumerate(peoples)}
    except Exception as e:
        return jsonify(None),404

    return jsonify(d),200




@mysql.route("/mysql/excel/",methods=['POST'])
def excel_list():
    '''
    分页展示功能已完成。
    #todo 接口2 ，展示用户所有文件列表 ,变成给部门领导的展示，


    :param
    :return: 该用户库中所有excel的文件名
    '''

    data = request.form
    level_3 = data.get("level_3")
    user_name = data.get("name")
    level_1 = data.get("level_1")
    level_2 = data.get("level_2")
    try:
        page = int(data.get("page",1))
        page = page if page > 0 else 1
    except:
        page = 1

    try :
        size = int(data.get("size",20))
        size = size if size > 0 and size < 101 else 20
    except:
        size = 20



    if level_3 == "草":
        level_3 = 1
    elif level_3 =="报":
        level_3 = 2
    elif level_3 == "副":
        level_3 = 3
    elif level_3 == "垃":
        level_3 = 4
    elif level_3 == "收":
        level_3 = 5


    if level_2 == "日":
        level_2 = 1
    elif level_2 == "周":
        level_2 = 2
    elif level_2 == "旬":
        level_2 = 3
    elif level_2 == "月":
        level_2 = 4
    elif level_2 == "季":
        level_2 = 5
    elif level_2 == "半":
        level_2 = 6
    elif level_2 == "年":
        level_2 = 7


    if level_1 == "人":
        level_1 = 1
    elif level_1 == "机":
        level_1 = 2
    elif level_1 == "物":
        level_1 = 3
    elif level_1 == "法":
        level_1 = 4



    # todo 前端要什么，就给他查什么。
    try:
        database = find_db(user_name)

        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        start = (page - 1) * size


        exceles = session.query(User_excel).filter(User_excel.work_id == level_1). \
        filter(User_excel.date_id == level_2).filter(User_excel.status_id == level_3) \
        .order_by(User_excel.created_date.desc()).all()

        count = len(exceles)  # 总条数

        exceles = exceles[start:start + size]   # 记录不够也不会抛出错误。



        json_list = []
        for i in exceles:
            json_dict = {}
            json_dict["id"] = i.id
            json_dict["filename"] = i.filename
            json_dict["created_date"] = i.created_date
            json_list.append(json_dict)


        res = {'status': 200,
               "total": len(exceles),"size":size,
               "page":page,
               "count":count,
               "data": json_list}
        return jsonify(res), 200


    except Exception as e:
        print(e,"记录日志")
        return jsonify({'status': 404, "data": None}),404








@mysql.route("/mysql/excel/show",methods=['POST'])
def excel_show():
    """
    用来展示具体的文件接口
    这里我有思路了，挂上NGINX 然后直接去打开地址，就等于是阅览。
    #todo api4
    :return:
    """
    data = request.form
    filename = data.get("filename")
    id = data.get("id")
    user_name = data.get("name")

    try:
        database = find_db(user_name)
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        file = session.query(User_excel).filter(User_excel.filename == filename).filter(User_excel.id == id ).limit(1).one()
        path = "http://"+ file.fgroup  +  file.path
        res = {'status': 200, "data": path}

        return jsonify(res), 200
    #todo 这里需要拼接路径，前面是固定的ip地址,运维安排，。但是前面的组号，需要在文件入库的时候单独放入一个字段里面，然后在这里拿出来拼接。


    except Exception as e:
        return jsonify({'status': 404, "data": None}),404

















