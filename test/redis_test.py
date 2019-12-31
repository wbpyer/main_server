import os
import socket
import re

'ESTABLISH'

addrs = socket.getaddrinfo(socket.gethostname(), None)
ip = [item[4][0] for item in addrs if ':' not in item[4][0]][0]
print(ip)
output = os.popen("netstat -ano | findstr {0}:3389".format(ip))
a = str(output.read())
c = 'TCP    172.16.11.5:3389       0.0.0.0:0              LISTENING       17776'
if a:
    ab = re.compile('ESTABLISH')
    lis = re.findall(ab , a)
    print(lis)
    if lis:
        print("guaduan ")
else:
    print("挂断")
# print(a)
# new = a.split("      ")[-2]
# print(new)

# a = os.system("netstat -ano | findstr 172.16.14.1:3390 | findstr EST" )
# print(a)

# db = redis.Redis('172.16.13.1',6379,2)
# #
#
# print(db.hgetall("安全管理员"))

# print(db.set(2,"343243fdsafdksla;jfkds;akj.xilg"))
# print(db.get(1))
#
#
# import jwt
# SECRET_KEY = '+)dno%=uwq*8rv4^u-^9-2s!gf=!wl_75iqqj56wyr&!s4yolg'
# data =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsZWFkZXJfaWQiOjE3LCJsZWFkZXJfbmFtZSI6InByb2plY3RKb2IiLCJsZWFkZXJfcm9sZSI6Ilx1OTg3OVx1NzZlZVx1OTBlOFx1NWI4OVx1NTE2OFx1N2JhMVx1NzQwNlx1NTQ1OCIsImxlYWRlcl9qb2JfaWQiOiI0Iiwicm9sZSI6Ilx1NTIwNlx1NTMwNVx1OTYxZlx1NGYwZDFcdTViODlcdTUxNjhcdTdiYTFcdTc0MDZcdTU0NTgiLCJyb2xlX2lkIjoxNiwiam9iX2lkIjoiMSIsImRlcGFydG1lbnRfaWQiOjIyLCJkZXBhcnRtZW50IjoiXHU0ZTEzXHU0ZTFhXHU1MjA2XHU1MzA1XHU5NjFmXHU0ZjBkMSJ9.wpZmgNWK0CttWWRPdxNTKOzRUfFaZwcunxWfpHhZh-8"
# data2 =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsZWFkZXJfaWQiOjQyLCJsZWFkZXJfbmFtZSI6ImRlbW8iLCJsZWFkZXJfcm9sZSI6Ilx1NTIwNlx1NTMwNVx1OTYxZlx1NGYwZDJcdTViODlcdTUxNjhcdTdiYTFcdTc0MDZcdTU0NTgiLCJsZWFkZXJfam9iX2lkIjoiMiIsInJvbGUiOiJcdTUyMDZcdTUzMDVcdTk2MWZcdTRmMGQxXHU1Yjg5XHU1MTY4XHU3YmExXHU3NDA2XHU1NDU4Iiwicm9sZV9pZCI6MTYsImpvYl9pZCI6IjEiLCJkZXBhcnRtZW50X2lkIjo0NSwiZGVwYXJ0bWVudCI6Ilx1NGUxM1x1NGUxYVx1NTIwNlx1NTMwNVx1OTYxZlx1NGYwZDEifQ.7R4g1Xngf7kwtoZF9mBu1dRlTPNsXmgSFobafQA4Exo"
# data2 = jwt.decode(data2, SECRET_KEY, algorithms=['HS256'])
# print(data2)

# import base64
# a = "{0}|3389|worker|pass@2019".format('172.16.13.1').encode()
#
# a1 = base64.b64encode(a).decode()
# print(a)
# print(a1)

