from flask import Flask,request,jsonify
from main_server.server_find import __getService
import logging

'''主服务框架'''

app = Flask(__name__)


#配置文件
class Config(object):
    DEBUG = True
app.config.from_object(Config)




@app.route('/vm',methods=['GET'])
def vm():
    """
    接受请求，调度虚拟机。使用第三方接入。
    :return:
    """
    return 'vm'


@app.route('/service/<string:name>',methods = ['GET'])
def find_service(name):
    """
    name:所请求子服务的名字
    接受请求，并发现服务
    :return:
    通过return 将请求重定向到指定的子服务上，具体子服务能否接到参数是个问题，需要把数据库端搭建起来，联调。
    目前先用重定向的方式继续开发，跑通之后，再具体修改细节。先测一下，再写，看怎么实现。
    重定向，不行，没有办法拿到请求的json数据，只能请求，返回IP地址，然后再次重发请求。然后做个缓存。
    0.1版本让web直接互联数据库端，0.2再迭代。
    最终由前端解决，这里只返回你要访问的服务的ip,端口就行。
    """
    try:
        print(name)
        service = __getService(name=name,host='192.168.29.129',port='8500',token=None)
        app.logger.info("remote_ip:{},user_agent:{}".format(request.remote_addr,request.user_agent.browser))

        # print(str(service[0]))
        #目前返回前端是json格式，也可以返回拼接好的格式。
        # print('http://' + str(service[0]) + ':' + str(service[1])+'/index')
        return  jsonify(service),200
    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)
        return  jsonify("service is busy please hold moment"),404





if __name__ == '__main__':
    print(app.url_map)
    handler = logging.FileHandler('E:\\logs\\flask_test.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s app:flask fun:%(funcName)s %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run()



'''目前主框架完成，虚拟机还没写。接下来数据库开发。'''