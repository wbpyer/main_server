
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db_server.model import Model_base
from fdfs_client.client import get_tracker_conf,Fdfs_client
import requests
import os

"""模板加载器，用来加载各部门模板模板。"""

TRCKER_CONF = 'C:\\Users\\Admin\\Desktop\\client2.conf'


host = '172.16.240.1'
user = 'root'
password = '123456'
port = 3306
database = "manage_table"
conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
engine = sqlalchemy.create_engine(conn_str, echo=True)

Session = sessionmaker(bind=engine)
session = Session()


def upload_fdfs(path:str):
    """
    #上传FDFS，api
    :param path:文件的绝对路径
    :return: 上传后FDFS返回的信息
    """

    trackers = get_tracker_conf(TRCKER_CONF)
    client = Fdfs_client(trackers)
    ret = client.upload_by_filename(path)
    if ret.get('Status') == 'Upload successed.':

        return ret
    return

def adder(name,path,depart,id):
    print()
    s1 = Model_base(textname=name,path=path,department=depart,file_id=id)

    try:

        session.add(s1)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e



if __name__ == "__main__":

    pass
    # file = "C:\\Users\\Admin\\Desktop\\物资设备部"

    # for root, dirs, files in os.walk(file):
    #     # print(root)  # 当前目录路径
    #     # print(dirs)  # 当前路径下所有子目录
    #     # print(files)  # 当前路径下所有非目录子文件
    #
    #     for i in files:
    #         try:
    #             temp = (i.split("、"))
    #             fil = "C:\\Users\\Admin\\Desktop\\物资设备部" + "\\" + i
    #             print(fil)
    #             ret = upload_fdfs(fil)
    #             if ret:
    #                 file_name = ret.get('Local file name')
    #                 file_name = file_name.split('\\')[-1]
    #
    #                 # mysql_date['path'] = "http://" + ret.get("Storage IP").decode() + "/" + ret.get('Remote file_id').decode()  # 最终路径
    #                 path = ret.get('Remote file_id').decode()
    #                 file_ip = ret.get('Storage IP').decode()
    #
    #                 # print(path)
    #
    #                 adder(name=temp[1],path =path,depart="物资设备部",id=temp[0])
    #         except Exception as e:
    #             print(e)



    # ret = upload_fdfs("C:\\Users\\Admin\\Desktop\\无标题.sql")
    # print(ret)

    #测试下载
    # def download_fdfs_file(path: str, name):
    #     """
    #     下载别人上报和发下的数据
    #     :param path:  下载路径
    #     :param name:  文件名
    #     :param work_id:  项目id
    #     :param date_id:  日期id
    #     :return:
    #     """
    #     # 下到本机后变成什么。
    #
    #
    #     # dest = "C:\\Users\\Admin\\Desktop\\我的办公桌\\收\\" + name
    #     dest = "C:\\Users\\admin\\Desktop\\" + name
    #     # 目前上报和发下，都下载到一个文件夹
    #     # dest = "C:\\Users\\worker\\Desktop\\test\\{0}\\{1}\\收\\".format(work_id,date_id)+ name
    #     if not os.path.exists(dest):
    #         # todo 这里的逻辑就是，如果存在收的这个文件，就什么都不做，如果不在就下载，证明这个时新报送上来的，这里已经实线了，就这么办。
    #
    #         url = "http://172.16.240.1:8888/" + path
    #         req = requests.get(url)
    #
    #         with open(dest, 'wb') as fobj:
    #             fobj.write(req.content)
    #             print("dowload over")
    #
    #     return
    #
    # # ret = upload_fdfs("C:\\Users\\Admin\\Desktop\\无标题.sql")
    # # print(ret)
    #
    # download_fdfs_file("group1/M00/00/01/rBDwAV6LJfaACPr0AAARqdiNTEI115.sql","tetst")
