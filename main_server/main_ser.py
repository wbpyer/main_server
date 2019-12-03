import logging
import requests
from flask import Flask,request,jsonify
from main_server.server_find import __getService
from flask_cors import CORS
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


'''主服务框架'''

app = Flask(__name__)


#配置文件
class Config(object):
    DEBUG = False
app.config.from_object(Config)

CORS(app)  # 允许跨站访问
SERECT_KEY = 'fdjsklafjkldsja'  #密匙 ，权限那里给的。
Ser = Serializer(SERECT_KEY)



@app.route('/vm/login',methods=['POST'])
def vm_login():
    """
    接受前端请求虚拟机服务。
    接受用户的信息，以及token,对token做一个验证，然后合法才能继续下一步，才能发送给毕工。

    :return:
    """

    #todo api 1,用来登录虚拟机的接口，接受前端请求


    data = request.form
    token = data.get('token')
    user_name = data.get('user_name')
    user_id = data.get('user_id')

    try:

        payload = Ser.loads(token)

        payload = {'user_name': user_name, 'user_id': user_id, 'payload': payload}
        resp = requests.post("127.4.1.1:6000", json=payload)

        res = {'status': 200, "data": resp.text}

        return jsonify(res), 200

    except Exception as e:

        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        d = {'status': 404,  "data": "验证未通过，请重新登陆"}
        return jsonify(d),404




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
        service = __getService(name=name,host='192.168.29.129',port='8500',token=None)
        app.logger.info("remote_ip:{},user_agent:{}".format(request.remote_addr,request.user_agent.browser))


        res  = {'status': 200, "data":service }
        print(res)
        return  jsonify(res),200

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)
        res = {'status': 404, "data": "无法获取服务地址"}
        return  jsonify(res),404



if __name__ == '__main__':

    print(app.url_map)
    handler = logging.FileHandler('E:\\logs\\main_server.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s app:flask fun:%(funcName)s %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run('0.0.0.0',5002)








