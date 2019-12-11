import logging
import requests
import  jwt
from flask import Flask,request,jsonify
from server_find import __getService
from flask_cors import CORS





'''主服务框架'''

app = Flask(__name__)


#配置文件
class Config(object):
    DEBUG = False
app.config.from_object(Config)
CORS(app)  # 允许跨站访问
SECRET_KEY = '+)dno%=uwq*8rv4^u-^9-2s!gf=!wl_75iqqj56wyr&!s4yolg'



@app.route('/vm/login',methods=['POST'])
def vm_login():
    """
    接受前端请求虚拟机服务。
    接受用户的信息，以及token,对token做一个验证，然后合法才能继续下一步，才能发送给毕工。

    :return:
    """

    #todo api 1,用来登录虚拟机的接口，接受前端请求


    data = request.form

    print(data)

    user_name = data.get('user_name')
    user_id = data.get('user_id')
    data = data.get('token')
    try:

        data = jwt.decode(data, SECRET_KEY, algorithms=['HS256'])
        print(data)

    except Exception as e:
        res = {'status': 404, "data": "口令不合法，非法登录"}
        return jsonify(res)




    leader_id = data.get("leader_id")
    leader_name=data.get("leader_name")
    leader_role=data.get("leader_role")
    leader_job_id = data.get("leader_job_id")
    role = data.get("role")
    role_id=data.get("role_id")
    job_id = data.get("job_id")
    department_id = data.get("department_id")
    department = data.get("department")

    for i in [user_name,user_id,role,role_id,job_id,department_id,department]:
        if not isinstance(i,int):

            if i.isspace() or len(i) == 0:
                res = {'status': 404, "data": "数据格式不合法，请重新请求"}
                return jsonify(res)



    try:


        payload = {'user_name': user_name,
                   'user_id': user_id,

                   "payload":
                       {"leader_id":leader_id,
                   "department":department,"department_id":department_id,"job_id":job_id,
                   "role_id":role_id,"role":role,"leader_job_id":leader_job_id,
                   "leader_name":leader_name,"leader_role":leader_role}
                   }

        print(111111)
        resp = requests.post("http://172.16.11.5:5006/dispatcher", json=payload)  #访问毕工服务地址
        print(resp.text)

        if resp.text:

            res = {'status': 200, "data": resp.text}
            return jsonify(res)
        else:
            res = {'status': 404,  "data": "没有可用的虚拟机"}
            return jsonify(res)


    except Exception as e:

        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        d = {'status': 406,  "data": "验证未通过，请重新登陆"}
        return jsonify(d)






@app.route('/service/<string:name>',methods = ['GET','POST'])
def find_service(name):
    """
    name:所请求子服务的名字
    接受请求，并发现服务
    根据不同的名字，可以访问不同的服务，也就是做到了，绝对动态，不需要改变主服务的一行代码
    有了新的功能模块，挂上来就能直接用。
    :return:

    最终由前端解决，这里只返回你要访问的服务的ip,端口就行。
    """
    try:
        data = request.form
        print(data)

        print(name)
        service = __getService(name=name,host='172.16.13.1',port='8500',token=None)
        app.logger.info("remote_ip:{},user_agent:{}".format(request.remote_addr,request.user_agent.browser))


        res  = {'status': 200, "data":service }
        print(res)
        return  jsonify(res)

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)
        res = {'status': 404, "data": "无法获取服务地址"}
        return  jsonify(res)



if __name__ == '__main__':

    print(app.url_map)
    handler = logging.FileHandler('/var/logs/flask_main.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s app:flask fun:%(funcName)s %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run()








