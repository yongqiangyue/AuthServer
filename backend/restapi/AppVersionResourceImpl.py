# -*- coding: utf-8 -*-
__author__ = 'yongqiangyue'

import json
from backend.utils.LogManager import Log
from backend.errors import BackendErrorCode, BackendErrorMessage
from backend.utils.BackendUtils import dbRollback, buildReturnValue
from backend.utils.SysConstant import VALUE, CODE, MESSAGE
from backend.utils.BackendUtils import to_json
from FlaskManager import db
from backend.model.AppVersionModel import AppVersion


logManager = Log()
log = logManager.getLogger("AppVersionResourcesImpl")


def updateAppVersion(appName, params):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None

    try:
        ver = AppVersion.query.filter(AppVersion.appName == appName).first()
        if ver is None:
            ver = AppVersion()
            ver.appName = appName
            ver.appVersion = params['appVersion']
            db.session.add(ver)
        else:
            ver.appVersion = params['appVersion']
        RETURNVALUE[VALUE] = to_json(ver)
        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)
    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)


def getAppVersion(appName):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None

    try:
        ver = AppVersion.query.filter(AppVersion.appName == appName).first()
        if ver is None:
            RETURNVALUE[CODE] = BackendErrorCode.APP_VERSION_GET_ERROR
            RETURNVALUE[MESSAGE] = BackendErrorMessage.APP_VERSION_GET_ERROR
            log.error(RETURNVALUE)
            return buildReturnValue(RETURNVALUE)
        RETURNVALUE[VALUE] = to_json(ver)
        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)
    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)