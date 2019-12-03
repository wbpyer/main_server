from flask import Blueprint
from flask import Flask,request,jsonify

health = Blueprint('health',__name__)



@health.route("/health/check",methods=['GET'])
def health_check():
    """
    健康监测接口，用来接收主服务器发送的心跳，并返回状态
    :return:
    """

    return "passing",200

