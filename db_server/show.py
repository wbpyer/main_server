from flask import Blueprint
import sqlalchemy
from flask import Flask,request,jsonify,current_app
from sqlalchemy.orm import sessionmaker,relationship
from models import User_excel,Vm_last_status,Status,Base
from sqlalchemy_utils import database_exists,create_database
from model import Manage,All_Texts,Model_base

mysql = Blueprint('mysql',__name__)
host = '172.16.13.1'
user = 'root'
password = '123456'
port = 3306



"""
此页面内容和前端交互
"""
def deletd_manage_busi(session,database:str,busi:str):
    """
    删除所选中的业务配置。一次只能删除一条，不能删除多条。
    :param session:
    :param database:
    :param depart:
    :param username:
    :param busi:
    :return:
    """

    record = session.query(Manage).filter(Manage.dbname == database).filter(Manage.business == busi).limit(1).one()

    try:

        session.delete(record)
        session.commit()

    except Exception as e:
        session.rollback()
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        print(e, "记录日志")



def insert_manage_table(session,database:str,department,level,username,busi:str):
    """

    :param session:  连接
    :param database:  数据库名
    :param depart:
    :param username: name
    :param busi:  业务
    :return:
    """


    # Base.metadata.create_all(engine)

    mange = Manage(dbname =database ,department = department ,level=level, name = username, business = busi)

    try:
        session.add(mange)
        session.commit()

    except Exception as e:
        session.rollback()
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
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



@mysql.route("/mysql/business",methods=['POST'])
def change_business():
    """
    调整业务接口，部门长给人员配置业务的时候，就走这个接口，每次配置，都走一次这个业务接口。
    拿到name，用库名去查，怕用name有重复，然后拿到这条记录，后去库里面更新business字段，目前设计的是这个字段，是一个str
    #todo 接口4   部门长配置用户业务接口
    这个接口需要还张敏调试
    这里每次走这个接口，都需要去对比，已有表里的和不在表里的有什么不同，从而对这张表做出相应的变更。
    每次更改接口，都需要把更改后的这个人的最终业务列表传送到这个接口里面，然后我再后面做处理。
    :return:
    """

    try:

        data = request.form
        user_id = data.get("user_id")
        user_name = data.get("username")
        user_role = data.get("work")  # todo 这里变成了部门了，这个地方变成了传部门,我这里不用改，只需要张敏改就行。
        user_job_id = data.get("numVal")
        user_department_id = data.get("department_id")  # 这个字段可查，可不查
        user_business = data.get("business")  #这就是一个list,这里面有几个，就往里面写入几个记录，这样工区才能查询的到。
        user_department = data.get("department")  # 什么部门
        user_level = data.get("level")  # 那个项目部，或者公司



        for i in  [user_id,user_name,user_role,user_job_id,user_department_id]:
            if i.isspace() or len(i) == 0:
                res = {'status': 409, "data": "数据格式不合法，请重新请求"}
                return jsonify(res),409



        dbname = str(user_id) + ":" +user_name +":" + str(user_job_id) +":" + user_role


        madatabase = "manage_table"
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, madatabase)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        if user_business:
            records = session.query(Manage).filter(Manage.dbname == dbname).all()
            if records:
                #如果之前有记录

                 temp = [r.business for r in records]
                 ret = list(set(temp) ^ set(user_business))  #差集
                 if ret:
                     #证明确实有不一样的地方，否则的话什么都不做，证明没有任何改变。
                     if len(temp) > len(user_business):

                         for i in ret:
                             deletd_manage_busi(session, dbname, busi=i)


                         #权限有删除

                     elif len(temp) < len(user_business):
                         for i in ret:
                             insert_manage_table(session, dbname, user_department, user_level,user_name, busi=i)


                     #权限有增加

            else:

                #如果之前没有，就为每一给重新添加记录。
                for busi in user_business:
                    #每一个业务里面都会对应着一条记录，就是为了工区报的时候用的。
                    insert_manage_table(session, dbname, user_department, user_level, user_name, busi=busi)





    except Exception as e:
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        print(e)




@mysql.route("/mysql/create",methods=['POST'])
def create_db():
    """
    创建数据库的接口，并可以直接完成表的迁移，同时初始化，默认数据。这个是给人事用。建库在这里建，但是还是需要
    一些其他的业务口的。这个口径还是要有的。先建库，建完库之后，每次变动，就调一次变动的接口。
    #todo 接口1   人事添加用户接口
    :return:
    """

    try:

        data = request.form
        user_id = data.get("user_id")
        user_name = data.get("username")
        user_role = data.get("work")  # todo 这里变成了部门了，这个地方变成了传部门,我这里不用改，只需要张敏改就行。
        user_job_id = data.get("numVal")
        user_department_id = data.get("department_id")




        for i in  [user_id,user_name,user_role,user_job_id,user_department_id]:
            if i.isspace() or len(i) == 0:
                res = {'status': 404, "data": "数据格式不合法，请重新请求"}
                return jsonify(res),404



        database = str(user_id) + ":" +user_name +":" + str(user_job_id) +":" + user_role

        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        if database_exists(engine.url):
            print(engine.url)

            # Base.metadata.drop_all(engine)
            return jsonify("数据库已经存在，"),200

        else:
            create_database(engine.url)
            Base.metadata.create_all(engine)


        Session = sessionmaker(bind=engine)
        session = Session()


        # s = Status(status_name ="草")
        s1 = Status(status_name="我的办公桌")
        s2 = Status(status_name="报")
        s3 = Status(status_name="回收站")
        s4 = Status(status_name = "收")
        s5 = Status(status_name = "发")

        # d1 = Date_name(date_name = "日")
        # d2 = Date_name(date_name = "周")
        # d3 = Date_name(date_name = "旬")
        # d4 =Date_name(date_name = "月")
        # d5 =Date_name(date_name = "季")
        # d6 = Date_name(date_name = "半")
        # d7 = Date_name(date_name = "年")
        #
        # w1 = Work_name(work_name = "人")
        # w2 = Work_name(work_name = "机")
        # w3 = Work_name(work_name = "物")
        # w4 = Work_name(work_name = "法")

        try :
            # session.add_all([s,s1,s2,s3,s4,d1,d2,d3,d4,d5,d6,d7,w1,w2,w3,w4])
            session.add_all([ s1, s2, s3, s4, s5])
            session.commit()
            res = {'status': 200, "data": "ok"}
            return jsonify(res),200
        except Exception as e:
            session.rollback()
            print(e,"记录日志")
            res = {'status': 404, "data": "not ok"}
            return jsonify(res),404

    except Exception as e:
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        print(e)



@mysql.route("/mysql/findbusi",methods = ['POST'])
def find_busi():
    """
    寻找接口，找到部门对应要报送的人
    :return: 一个列表，根据查询条件，返回一个列表。
    """
    try:

        data = request.json
        # business = data.get("business")  # 暂时不用业务
        department = data.get("department")
        family = data.get("family")


        madatabase = "manage_table"
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, madatabase)
        engine = sqlalchemy.create_engine(conn_str, echo=True)


        Session = sessionmaker(bind=engine)
        session = Session()

        records = session.query(Manage).filter(Manage.department == department).filter(Manage.family == family).all()

        try:
            if records:
                res = [i.dbname for i in records]

                return jsonify(res), 200

            else:
                return None,200

        except Exception as e:
            return jsonify(e),404



    except Exception as e:
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        print(e)





@mysql.route("/mysql/excel",methods=['POST'])
def excel_list():
    '''
    分页展示功能已完成。
    #todo 接口2 ，展示用户所有文件列表 ,变成给部门领导的展示，


    :param
    :return: 该用户库中所有excel的文件名
    '''

    data = request.form
    # level_3 = data.get("level_3")
    user_name = data.get("name")
    level = data.get("level")
    # level_2 = data.get("level_2")
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



    if level == "收":
        level = 4
    elif level =="报":
        level = 2
    elif level == "发":
        level = 5
    # elif level_1 == "垃":
    #     level_1 = 4
    # elif level_1 == "收":
    #     level_1 = 5


    # if level_2 == "日":
    #     level_2 = 1
    # elif level_2 == "周":
    #     level_2 = 2
    # elif level_2 == "旬":
    #     level_2 = 3
    # elif level_2 == "月":
    #     level_2 = 4
    # elif level_2 == "季":
    #     level_2 = 5
    # elif level_2 == "半":
    #     level_2 = 6
    # elif level_2 == "年":
    #     level_2 = 7
    #
    #
    # if level_1 == "人":
    #     level_1 = 1
    # elif level_1 == "机":
    #     level_1 = 2
    # elif level_1 == "物":
    #     level_1 = 3
    # elif level_1 == "法":
    #     level_1 = 4



    # todo 前端要什么，就给他查什么。
    try:
        database = find_db(user_name)

        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        start = (page - 1) * size


        # exceles = session.query(User_excel).filter(User_excel.work_id == level_1). \
        # filter(User_excel.date_id == level_2).filter(User_excel.status_id == level_3) \
        # .order_by(User_excel.created_date.desc()).all()

        exceles = session.query(User_excel).filter(User_excel.status_id == level).filter(User_excel.deleted == 0) \
            .order_by(User_excel.created_date.desc()).all()

        count = len(exceles)  # 总条数

        exceles = exceles[start:start + size]   # 记录不够也不会抛出错误。



        json_list = []
        for i in exceles:
            json_dict = {}
            json_dict["id"] = i.id


            filepath = "http://172.16.13.1:8080/"+ i.path
            json_dict["filepath"] = filepath
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
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        return jsonify({'status': 404, "data": None}),404



@mysql.route("/mysql/excel/show",methods=['POST'])
def excel_show():
    """
    用来展示具体的文件接口
    这里我有思路了，挂上NGINX 然后直接去打开地址，就等于是阅览。需要微软的控件访问

    #todo api4
    :return:
    """
    try:
        data = request.form
        filename = data.get("filename")
        id = data.get("id")
        user_name = data.get("name")




        database = find_db(user_name)
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        file = session.query(User_excel).filter(User_excel.filename == filename).filter(User_excel.id == id ).limit(1).one()
        path = "http://" +  file.fgroup + "/" +   file.path
        res = {'status': 200, "data": path}

        return jsonify(res), 200
    #todo 这里需要拼接路径，前面是固定的ip地址,运维安排，。但是前面的组号，需要在文件入库的时候单独放入一个字段里面，然后在这里拿出来拼接。


    except Exception as e:
        print(e)
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        return jsonify({'status': 404, "data": None}),404


@mysql.route("/mysql/find_initpath",methods=['POST'])
def mysql_conn():
    """
    查询初始化的报表。
    :param business: 业务
    :param department: 部门
    :param level:  所属
    :return:  路径地址
    """
    try:
        data = request.json
        business = data.get("role")
        department = data.get("department")
        level = data.get("level")

        database = "manage_table"
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)


        Session = sessionmaker(bind=engine)
        session = Session()
        name = session.query(All_Texts).filter(All_Texts.level == level).filter(
            All_Texts.business == business).filter(All_Texts.department == department).all()

        if name:
            for i in name:
                # print(i.path)
                return jsonify(i.path),200

        else:
            return None,200



    except Exception as e:
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        print(e)



@mysql.route("/mysql/model",methods=['POST'])
def model_list():
    '''
    模板加载器接口1
    #todo 模板加载器接口1 ，展示所有模板列表，按照部门展示，。


    :param
    :return: 该用户库中所有excel的文件名
    '''

    data = request.form

    department = data.get("department")

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



    # todo 前端要什么，就给他查什么。
    try:
        database = "manage_table"

        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        start = (page - 1) * size


        # exceles = session.query(User_excel).filter(User_excel.work_id == level_1). \
        # filter(User_excel.date_id == level_2).filter(User_excel.status_id == level_3) \
        # .order_by(User_excel.created_date.desc()).all()

        modeles = session.query(Model_base).filter(Model_base.department == department).order_by(Model_base.file_id.desc()).all()

        count = len(modeles)  # 总条数

        # exceles = modeles[start:start + size]   # 记录不够也不会抛出错误。



        json_list = []
        for i in modeles:
            json_dict = {}
            json_dict["id"] = i.id


            filepath = "http://172.16.13.1:8080/"+ i.path
            json_dict["filepath"] = filepath
            json_dict["filename"] = i.textname



            json_list.append(json_dict)


        res = {'status': 200,
               "total": len(modeles),"size":size,
               "page":page,
               "count":count,
               "data": json_list}
        return jsonify(res), 200


    except Exception as e:
        print(e,"记录日志")
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
                                 request.user_agent.browser)
        return jsonify({'status': 404, "data": None}),404





@mysql.route("/mysql/model/show",methods=['POST'])
def model_show():
    """
    #todo api4 用来下载具体文件的接口
    :return:
    """
    try:
        data = request.form
        filename = data.get("filename")
        id = data.get("id")


        database = "manage_table"
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        file = session.query(Model_base).filter(Model_base.textname == filename).filter(Model_base.id == id ).limit(1).one()
        path = "http://" +  file.fgroup + "/" +   file.path
        res = {'status': 200, "data": path}

        return jsonify(res), 200
    #todo 这里需要拼接路径，前面是固定的ip地址,运维安排，。但是前面的组号，需要在文件入库的时候单独放入一个字段里面，然后在这里拿出来拼接。


    except Exception as e:
        print(e)
        current_app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        return jsonify({'status': 404, "data": None}),404


















