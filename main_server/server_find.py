import json
import requests
from random import randint




def __getService(name,host,port,token):  # 负债均衡获取服务实例
    url = 'http://' + host + ':' + port + '/v1/catalog/service/' + name  # 获取 相应服务下的DataCenter
    dataCenterResp = requests.get(url)
    if dataCenterResp.status_code != 200:
        raise Exception('can not connect to consul ')
    listData = json.loads(dataCenterResp.text)
    dcset = set()  # DataCenter 集合 初始化
    for service in listData:
        dcset.add(service.get('Datacenter'))
    serviceList = []  # 服务列表 初始化
    for dc in dcset:
        if token:
            url = 'http://' + host + ':' + port + '/v1/health/service/' + name + '?dc=' + dc + '&token=' + token
        else:
            url = 'http://' + host + ':' + port + '/v1/health/service/' + name + '?dc=' + dc + '&token='
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception('can not connect to consul ')
        text = resp.text
        serviceListData = json.loads(text)

        for serv in serviceListData:
            status = serv.get('Checks')[1].get('Status')
            if status == 'passing':  # 选取成功的节点,也可以查看失败的节点，这里由我自己去定义。
                address = serv.get('Service').get('Address')
                port = serv.get('Service').get('Port')
                serviceList.append({'port': port, 'address': address})
    if len(serviceList) == 0:
        raise Exception('no serveice can be passing health')
    else:
        service = serviceList[randint(0, len(serviceList) - 1)]  # 随机获取一个可用的服务实例\
        print(service)
        return service


