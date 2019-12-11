"""向consul 添加注册测试，地址。"""
# import json
# import requests
from consulate import Consul
# from random import randint
#
consul = Consul(host='172.16.13.1', port=8500)
#
consul.agent.service.register(name='db', service_id='db', address='172.16.13.1', port=5002, tags=["db"],
                                               interval='5s', httpcheck="http://172.16.13.1:5002/health/check")
# b = json.dumps(None)
# print(b)
# print(json.loads(b))


# l = [1,2,3]
# print(l[0:20])
# l ="    "
# s = ""
# print(len(""))



# import base64
# import  jwt
# SECRET_KEY = '+)dno%=uwq*8rv4^u-^9-2s!gf=!wl_75iqqj56wyr&!s4yolg'
# d = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ilx1OGZkMFx1N2VmNFx1NTQ5Nlx1NTU2MVx1NTQyNyIsInNpdGUiOiJodHRwczovL29wcy1jb2ZmZWUuY24ifQ.YA_cMfqLOSZm0jkhVxLoKYx7xzR8IFUla1bNa_riBmU'
# print(jwt.decode(d,SECRET_KEY,algorithms=['HS256']))

