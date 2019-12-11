from fdfs_client.client import get_tracker_conf,Fdfs_client

def delete_fdfs(path:bytes):
    """
    #删除FDFS
    :param path:文件的绝对路径
    :return: 上传后FDFS返回的信息
    """

    trackers = get_tracker_conf('client.conf')  #todo，这个需要再容器里改一下
    client = Fdfs_client(trackers)
    try:
        ret = client.delete_file(path)
        return ret

    except Exception as e:
        return "删除失败，没有这个文件"


if __name__ == '__main__':
    print(delete_fdfs(b'group1/M00/00/01/rBANAV3tr52APVPAAAAFsEslqZ418.conf'))


