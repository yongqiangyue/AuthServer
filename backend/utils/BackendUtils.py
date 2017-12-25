# -*- coding: utf-8 -*-
__author__ = 'xiliangma'

import commands
import os
import random
import hashlib
import time
from flask import jsonify
from flask import request
from functools import wraps
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from backend.model.UserSessionModel import UserSession
from backend.model.PPDevicesModel import PPDevices
from backend.model.UserModel import User
from backend.utils.SysConstant import *
from FlaskManager import db, httpAuth
from backend.errors import BackendErrorCode
from backend.errors import BackendErrorMessage
from backend.utils.SysConstant import admin, md5Pwd

@httpAuth.verify_password
def verify_password(username, password):

    if username == admin:
        code, message = adminAuth(password)
        if code != 0:
            return False
    else:
        code, message = userAuth(username, password)
        if code != 0:
            return False
    return True


def requiresAuth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        RETURNVALUE = {}
        RETURNVALUE[VALUE] = []
        RETURNVALUE[CODE] = 0
        RETURNVALUE[MESSAGE] = None

        auth = request.authorization

        if auth is None:
            RETURNVALUE[MESSAGE] = BackendErrorMessage.USER_NOT_EXIST_ERROR
            RETURNVALUE[CODE] = BackendErrorCode.USER_NOT_EXIST_ERROR
            return buildReturnValue(RETURNVALUE)

        if auth.username == admin:
            RETURNVALUE[CODE], RETURNVALUE[MESSAGE] = adminAuth(auth.password)
            if RETURNVALUE[CODE] != 0:
                return buildReturnValue(RETURNVALUE)
        else:
            RETURNVALUE[CODE], RETURNVALUE[MESSAGE] = userAuth(auth.username, auth.password)
            if RETURNVALUE[CODE] != 0:
                return buildReturnValue(RETURNVALUE)

        return f(*args, **kwargs)
    return decorated


def adminAuth(pwd):
    if md5Pwd != hashlib.md5(pwd).hexdigest():
        return BackendErrorCode.USER_PWD_ERROR, BackendErrorMessage.USER_PWD_ERROR
    return 0, None


def userAuth(tel, pwd):
    user = User.query.filter(User.Tel == tel).first()
    if user is None:
        return BackendErrorCode.USER_NOT_EXIST_ERROR, BackendErrorMessage.USER_NOT_EXIST_ERROR

    if user.Pwd != hashlib.md5(pwd).hexdigest():
        return BackendErrorCode.USER_PWD_ERROR, BackendErrorMessage.USER_PWD_ERROR
    return 0, None


'''
   返回参数
   {"code": "",
    "message": "",
    "value": ""}
'''


def buildReturnValue(RETURNVALUE):
    if RETURNVALUE[CODE] == 0:
        if RETURNVALUE[MESSAGE] is None:
            RETURNVALUE[MESSAGE] = 'SUCCESS'
        return jsonify(RETURNVALUE)
    else:
        if RETURNVALUE[MESSAGE] is None:
            RETURNVALUE[MESSAGE] = 'FAILED'
        return jsonify(RETURNVALUE)


'''
   @commType
        0 gen
        1 verify
   ./tls_licence_tools gen 私钥文件路径 sig将要存放的路径 sdkappid 用户id（用户名）
'''
tlsPath = os.path.abspath(os.path.dirname("AuthServer.py")) + tlsDir
def sigKey(commType, tel, sdkAppId):

    (errorCode, output) = commands.getstatusoutput(buildSigKeyComm(commType, str(tel), sdkAppId))
    if errorCode != 0:
        return errorCode, output

    filePath = tlsPath + str(tel) + "_sig"
    # get sigKey from file
    (errorCode, output) = getSigKey(filePath)
    return errorCode, output




def buildSigKeyComm(commType, tel, sdkAppId):
    publicKey = tlsPath + PUBLIC_KEY
    ecKey = tlsPath + PRIVATE_KEY
    sig = tlsPath + str(tel) + '_sig'
    space = ' '

    if (commType == 0):
        type = 'tls_licence_tools gen'
        comm = tlsPath + type + space + ecKey + space + sig + space + sdkAppId + space + str(tel)
    else:
        type = 'tls_licence_tools verify'
        comm = tlsPath + type + space + publicKey + space + sig + space + sdkAppId + space + str(tel)

    return comm


def getSigKey(filePath):
    (errorCode, output) = commands.getstatusoutput("cat " + filePath)
    return errorCode, output


'''
    @type
        0 user
        1 nas
'''
def allocationPPDeviceID(object, type, tel):
    usedPPDevices = PPDevices.query.filter(PPDevices.IsUsed == tel).first()
    if usedPPDevices is None:
        pPDevices = PPDevices.query.filter(PPDevices.IsUsed == None).first()
        if type == 0:
            pPDevices.IsUsed = tel
        else:
            pPDevices.IsUsed = object.NasId



def dbRollback(db):
    db.session.rollback()
    db.session.flush()


'''
    Generating four digit random code
'''
def createPhoneCode():
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
    verifyCode = "".join(x)
    return verifyCode


'''
params : [5031, 4]
phone_numbers: 18701657257

'''

ssender = SmsSingleSender(APP_ID, APP_KEY)
def senMessage(params, phone_numbers):
    try:
        return ssender.send_with_param(86, phone_numbers, TEMPLATE_ID, params)
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)


def checkRandomCodeIsValid(tel, randomCode):
    errorCode = 0
    errorMessage = None

    userSession = UserSession.query.filter(UserSession.Tel == tel).first()

    if userSession is None:
        errorCode = BackendErrorCode.RANDOM_CODE_INVALID_ERROR
        errorMessage = BackendErrorMessage.RANDOM_CODE_INVALID_ERROR
        return userSession, errorCode, errorMessage

    # validate randomCode
    if userSession.RandomCode != randomCode:
        errorCode = BackendErrorCode.RANDOM_CODE_VALIDATE_ERROR
        errorMessage = BackendErrorMessage.RANDOM_CODE_VALIDATE_ERROR
        return userSession, errorCode, errorMessage

    # validate randomCode is invalid
    localTime = time.time()
    createTime = time.mktime(time.strptime(str(userSession.CreateTime), '%Y-%m-%d %H:%M:%S'))
    timeDiff = (localTime - createTime)/60

    if (timeDiff > 5):
        db.session.delete(userSession)
        errorCode = BackendErrorCode.RANDOM_CODE_INVALID_ERROR
        errorMessage = BackendErrorMessage.RANDOM_CODE_INVALID_ERROR
        return userSession, errorCode, errorMessage

    return userSession, errorCode, errorMessage



if __name__ == "__main__":
    checkRandomCodeIsValid('18701656257')
    pass
    # sigKey(1, 'maxl', '1255610113')
    # sigKey(1, 'test2', '1255610839')
    # getSigKey()