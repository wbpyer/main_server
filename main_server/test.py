"""向consul 添加注册测试，地址。"""
import json
import requests
from consulate import Consul
from random import randint

consul = Consul(host='192.168.29.129', port=8500)

consul.agent.service.register(name='db', service_id='db', address='127.0.0.1', port=4325, tags=["test2"],
                                           interval='5s', httpcheck="http://191.0.0.1:9654/")

b = json.dumps(None)
print(b)
print(json.loads(b))








