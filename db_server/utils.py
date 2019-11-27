from fdfs_client.client import get_tracker_conf,Fdfs_client

def delete_fdfs(path:bytes):
    """
    #上传FDFS，api
    :param path:文件的绝对路径
    :return: 上传后FDFS返回的信息
    """

    trackers = get_tracker_conf(r'C:\Users\Admin\Desktop\client.conf')
    client = Fdfs_client(trackers)
    try:
        ret = client.delete_file(path)
        return ret

    except Exception as e:
        return "删除失败，没有这个文件"


