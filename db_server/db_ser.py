import sqlalchemy
import logging
from consulate import Consul
from flask import Flask,request,jsonify
from utils import delete_fdfs
from sqlalchemy.orm import sessionmaker,relationship
from models import User_excel,Vm_last_status
from show import mysql
from flask_cors import CORS
from health_check import health

app = Flask(__name__)
app.register_blueprint(mysql)
app.register_blueprint(health)
CORS(app)



#这里由两种传参方式，json，还是直接restful
host = '172.16.13.1'
user = 'root'
password = '123456'
port = 3306
consul = Consul(host='172.16.13.1', port=8500)   # 服务发现集群consul连接器。

"""

此页面内容只和虚拟机通信。

"""

@app.route("/db/<string:db_name>/excel/delete",methods=['POST'])
def excel_delete(db_name):
    """
    对接虚拟机的垃圾操作。数据库端做出的一些列反应。包括假删除
    :param db_name:
    :return:
    """
    try:
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
        file_ip = data.get('file_ip')
        user_id = data.get("user_id")
        user_name =data.get("user_name")
        role = data.get("role")
        role_id = data.get("role_id")
        department_id = data.get("department_id")
        department = data.get("department")
        status_id = data.get("status_id")


        if status_id == "我的办公桌":
            status_id = 1
        elif status_id =="报":
            status_id = 2
        elif status_id == "回收站":
            status_id =3
        elif status_id == "收":
            status_id =4

        elif status_id == "发":
            status_id = 5

        # date_id = data.get("date_id")
        # if date_id == "日":
        #     date_id = 1
        # elif date_id =="周":
        #     date_id = 2
        # elif date_id == "旬":
        #     date_id =3
        # elif date_id == "月":
        #     date_id =4
        # elif date_id == "季":
        #     date_id = 5
        # elif date_id == "半":
        #     date_id = 6
        # elif date_id == "年":
        #     date_id = 7



        # work_id = data.get("work_id")
        # if work_id == "人":
        #     work_id = 1
        # elif work_id =="机":
        #     work_id = 2
        # elif work_id == "物":
        #     work_id =3
        # elif work_id == "法":
        #     work_id =4



        # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空

        #查询条件更加精准化，理论上，一定会有重名文件，因为是多级目录，所以一定要精准，这样就没问题了
        # name = session.query(User_excel).filter(User_excel.filename == filename).filter(User_excel.work_id == work_id).filter(User_excel.date_id ==
        #     date_id).all()


        name = session.query(User_excel).filter(User_excel.filename == filename).filter(User_excel.status_id == status_id).all()


        if name:
            for i in name:
                print(i.path)
                delete_fdfs(i.path)
                i.path = filepath
                # i.status_id = 4
                i.deleted = 1

                try:
                    session.add(i)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(e, "记录日志")

            return "ok",200


        else:
            if all([department,department_id]):

                excel = User_excel(filename=filename,path=filepath,deleted = 1,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup=file_ip,
                           department_id=department_id,
                            department = department,
                           status_id=status_id)
            else:
                excel = User_excel(filename=filename,path=filepath,deleted = 1,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup = file_ip,
                           status_id=status_id)


            try:
                session.add(excel)
                session.commit()
                return "ok",200
            except Exception as e:
                session.rollback()
                print(e,"记录日志")
                return "not ok",404

    except Exception as e:
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)









@app.route("/db/<string:db_name>/excel/add",methods=['POST'])
def excel_add(db_name):
    """
    excel添加功能，向mysql中添加新的数据。
    :param db_name:
    :return:
    """
    try:

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
        file_ip = data.get('file_ip')
        user_id = data.get("user_id")
        user_name =data.get("user_name")
        role = data.get("role")  #这里面现在是业务
        role_id = data.get("role_id")
        department_id = data.get("department_id")
        department = data.get("department")
        status_id = data.get("status_id")

        if status_id == "我的办公桌":
            status_id = 1
        elif status_id =="报":
            status_id = 2
        elif status_id == "回收站":
            status_id =3
        elif status_id == "收":
            status_id =4

        elif status_id == "发":
            status_id = 5


        # date_id = data.get("date_id")
        # if date_id == "日":
        #     date_id = 1
        # elif date_id =="周":
        #     date_id = 2
        # elif date_id == "旬":
        #     date_id =3
        # elif date_id == "月":
        #     date_id =4
        # elif date_id == "季":
        #     date_id =5
        # elif date_id == "半":
        #     date_id =6
        # elif date_id == "年":
        #     date_id =7
        #
        # work_id = data.get("work_id")
        # if work_id == "人":
        #     work_id = 1
        # elif work_id =="机":
        #     work_id = 2
        # elif work_id == "物":
        #     work_id =3
        # elif work_id == "法":
        #     work_id =4
        # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空


        # file = session.query(User_excel).filter(User_excel.filename == filename).filter(User_excel.status_id == status_id).filter(User_excel.date_id == date_id)\
        #     .filter(User_excel.work_id == work_id).all()
        file = session.query(User_excel).filter(User_excel.filename == filename).filter(
            User_excel.status_id == status_id).filter(User_excel.role == role).all()

        # todo 4.2做一个防止重复的查询，如果有重复的就更新路径，没有就新增，但是查询时候还要根据业务查一下。


        if file:
            for i in file:
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
                           role_id= role_id,fgroup=file_ip,
                           department_id=department_id,
                            department = department,
                           status_id=status_id)
            else:
                excel = User_excel(filename=filename,path=filepath,deleted = 0,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup=file_ip,
                           status_id=status_id)

            try:
                session.add(excel)
                session.commit()
                return "ok",200
            except Exception as e:
                session.rollback()
                print(e,"记录日志")
                return "not ok",404



    except Exception as e:
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)
        print("记录日志",e)




@app.route("/db/<string:db_name>/excel/add/lower",methods=['POST'])
def excel_add_lower(db_name):
    """
    下发功能时候，替下属添加数据，但是有一点，不能更新，而是新建，
    因为下发的，删不删，得自己决定，

    :param db_name:
    :return:
    """
    try:

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
        file_ip = data.get('file_ip')
        user_id = data.get("user_id")
        user_name =data.get("user_name")   #这里能体现出是谁发下来的。
        role = data.get("role")
        role_id = data.get("role_id")
        department_id = data.get("department_id")
        department = data.get("department")
        status_id = 5  # 下发的，在手下那里，体现的只能是发里面。


        # date_id = data.get("date_id")
        # if date_id == "日":
        #     date_id = 1
        # elif date_id =="周":
        #     date_id = 2
        # elif date_id == "旬":
        #     date_id =3
        # elif date_id == "月":
        #     date_id =4
        # elif date_id == "季":
        #     date_id =5
        # elif date_id == "半":
        #     date_id =6
        # elif date_id == "年":
        #     date_id =7
        #
        # work_id = data.get("work_id")
        # if work_id == "人":
        #     work_id = 1
        # elif work_id =="机":
        #     work_id = 2
        # elif work_id == "物":
        #     work_id =3
        # elif work_id == "法":
        #     work_id =4

        # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空



        if all([department,department_id]):

            excel = User_excel(filename=filename,path=filepath,deleted = 0,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup = file_ip,
                           department_id=department_id,
                            department = department,
                           status_id=status_id)


        else:
            excel = User_excel(filename=filename,path=filepath,deleted = 0,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup = file_ip,
                           status_id=status_id)
        try:
            session.add(excel)
            session.commit()
            return "ok",200
        except Exception as e:
            session.rollback()
            print(e,"记录日志")
            return "not ok",404

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)





@app.route("/db/<string:db_name>/excel/add/leader",methods=['POST'])
def excel_add_leader(db_name):
    """
    上报功能时候，替领导添加数据，但是有一点，不能更新，而是新建，
    因为上报上来的，删不删，得领导自己决定，

    :param db_name:
    :return:
    """
    try:

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
        file_ip = data.get('file_ip')
        user_id = data.get("user_id")
        user_name =data.get("user_name")   #这里能体现出是谁报送上来的。
        role = data.get("role")
        role_id = data.get("role_id")
        department_id = data.get("department_id")
        department = data.get("department")
        status_id = 4  # 报上去的，在领导那里，体现的只能是收里面。


        # date_id = data.get("date_id")
        # if date_id == "日":
        #     date_id = 1
        # elif date_id =="周":
        #     date_id = 2
        # elif date_id == "旬":
        #     date_id =3
        # elif date_id == "月":
        #     date_id =4
        # elif date_id == "季":
        #     date_id =5
        # elif date_id == "半":
        #     date_id =6
        # elif date_id == "年":
        #     date_id =7
        #
        # work_id = data.get("work_id")
        # if work_id == "人":
        #     work_id = 1
        # elif work_id =="机":
        #     work_id = 2
        # elif work_id == "物":
        #     work_id =3
        # elif work_id == "法":
        #     work_id =4

        # file_type_id = data.get("file_type_id")  0.1暂时先不考虑。先放空



        if all([department,department_id]):

            excel = User_excel(filename=filename,path=filepath,deleted = 0,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup = file_ip,
                           department_id=department_id,
                            department = department,
                           status_id=status_id)


        else:
            excel = User_excel(filename=filename,path=filepath,deleted = 0,
                           user_id=user_id,user_name = user_name,role=role,
                           role_id= role_id,fgroup = file_ip,
                           status_id=status_id)
        try:
            session.add(excel)
            session.commit()
            return "ok",200
        except Exception as e:
            session.rollback()
            print(e,"记录日志")
            return "not ok",404

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)






@app.route("/mysql/<string:db_name>/excel/find",methods=['POST'])
def vm_latest_find(db_name):
    """
    根据业务查找最后一次虚拟机状态，所有人逻辑都是固定的
    :param db_name:
    :return:
    """
    data = request.json
    # todo 这里要通过业务来查询。
    business = data.get("role") # 业务名。
    # user_name = data.get('user_name')
    # user_id = data.get('user_id')
    # job_id = data.get("job_id")
    # db_name = str(user_id) + user_name + str(job_id) + role

    try:

        print(db_name)

        database = db_name
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
        Session = sessionmaker(bind=engine)
        session = Session()
        """这里是固定的逻辑，就是查这张表中，最后一次记录里的地址返回来就行。这张表里面有一个业务字段，我看现在有
        个read字段是空闲的，所以就用这个字段就行。下面是具体的查询逻辑。"""

        if session.query(Vm_last_status).filter(Vm_last_status.role == business).all():
            v = session.query(Vm_last_status).filter(Vm_last_status.role == business).order_by(Vm_last_status.id.desc()).limit(1).one()

            print(v.id)

            filepath = v.path
            print(filepath)
            return jsonify(filepath)
        else:
            return jsonify(None)

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)





@app.route("/mysql/<string:db_name>/excel/find/submit",methods=['POST'])
def vm_latest_find_submit(db_name):
    """
    查找下级报送给上级的文件路径。为初始化工作区做准备。
    这个接口没用，因为是用Redis实时收发
    :param db_name:
    :return:
    """
    try:

        data = request.json

        # role = data.get("role")
        user_name = data.get('user_name')
        user_id = data.get('user_id')
        # job_id = data.get("job_id")
        # db_name = str(user_id) + user_name + str(job_id) + role
        print(db_name)

        database = db_name
        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

        # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
        Session = sessionmaker(bind=engine)
        session = Session()


        files = session.query(User_excel).filter(User_excel.user_name != user_name).all()

        d = [(file.filename,file.path)  for file in files ]

        return jsonify(d)

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)




@app.route("/db/<string:db_name>/vm_latest/add",methods=['POST'])
def vm_latest_add(db_name):
    """

    对接虚拟机的最后一次状态保存功能，请求到这里后，数据库端就会完成保存。
    这里没有什么业务逻辑，也不考虑冗余 。存好就行。
    :param db_name:
    :return:
    """
    try:

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

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)




@app.route("/db/excel/movename",methods=['POST'])
def move():
    """
    解决文件改名之后，造成的数据库文件冗余问题。
    :return:
    """

    try:

        data = request.json

        name = data.get("filename")
        db = data.get("dbname")
        status_id = data.get("status")
        # work_id = data.get("work")
        # date_id = data.get("date")


        if status_id == "我的办公桌":
            status_id = 1
        elif status_id =="报":
            status_id = 2
        elif status_id == "回收站":
            status_id =3
        elif status_id == "收":
            status_id =4
        elif status_id == "发":
            status_id = 5



        # if date_id == "日":
        #     date_id = 1
        # elif date_id =="周":
        #     date_id = 2
        # elif date_id == "旬":
        #     date_id =3
        # elif date_id == "月":
        #     date_id =4
        # elif date_id == "季":
        #     date_id =5
        # elif date_id == "半":
        #     date_id =6
        # elif date_id == "年":
        #     date_id =7
        #
        #
        # if work_id == "人":
        #     work_id = 1
        # elif work_id =="机":
        #     work_id = 2
        # elif work_id == "物":
        #     work_id =3
        # elif work_id == "法":
        #     work_id =4


        conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
        engine = sqlalchemy.create_engine(conn_str, echo=True)

            # 所有的都是这个模型，所以可以提前写好，应为可以复用，大量复用。
        Session = sessionmaker(bind=engine)
        session = Session()


        # file = session.query(User_excel).filter(User_excel.filename == name).\
        #         filter(User_excel.status_id == status_id).filter(User_excel.date_id == date_id)\
        #         .filter(User_excel.work_id == work_id).all()


        file = session.query(User_excel).filter(User_excel.filename == name). \
            filter(User_excel.status_id == status_id).all()





        for i in file:
            delete_fdfs(i.path)
            session.delete(i)
            session.commit()

        return "file is deleted",200





    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        return "delete error",404




if __name__ == '__main__':


    print(app.url_map)
    # try:
    #     consul.agent.service.register(name='db', service_id='db', address='172.16.13.1', port=5002, tags=["db"],
    #                                            interval='5s', httpcheck="http://172.16.13.1:5002/health/check")
    #
    # except Exception as e:
    #     print("服务没有注册成功:{0}".format(e))
    #     app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ", e, request.remote_addr,
    #                      request.user_agent.browser)
    #上面是注册服务发现，向consul注册服务。

    # handler = logging.FileHandler('/var/logs/db_server.log', encoding='UTF-8')
    # handler.setLevel(logging.DEBUG)
    # logging_format = logging.Formatter("%(asctime)s app:flask fun:%(funcName)s %(levelname)s %(message)s")
    # handler.setFormatter(logging_format)
    # app.logger.addHandler(handler)

    app.run('0.0.0.0',5001)













