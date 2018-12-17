# -*- coding: utf-8 -*-
__author__ = 'yongqiangyue'

from backend.utils.LogManager import Log
from backend.errors import BackendErrorCode, BackendErrorMessage
from backend.utils.BackendUtils import dbRollback, buildReturnValue
from backend.utils.SysConstant import VALUE, CODE, MESSAGE
from backend.utils.BackendUtils import to_json
from FlaskManager import db
from backend.model.HouseAddressModel import HouseAddress


logManager = Log()
log = logManager.getLogger("HouseAddressResourcesImpl")


def updateHouseAddress(tel, params):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None

    try:
        addr = HouseAddress.query.filter(HouseAddress.tel == tel).first()
        if addr is None:
            addr = HouseAddress()
            addr.tel = tel
            addr.addressJson = params['addressJson']
            db.session.add(addr)
        else:
            addr.addressJson = params['addressJson']
        RETURNVALUE[VALUE] = to_json(addr)
        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)
    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)


def getHouseAddress(tel):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None

    try:
        addr = HouseAddress.query.filter(HouseAddress.tel == tel).first()
        if addr is None:
            RETURNVALUE[CODE] = BackendErrorCode.HOUSE_ADDRESS_GET_ERROR
            RETURNVALUE[MESSAGE] = BackendErrorMessage.HOUSE_ADDRESS_GET_ERROR
            log.error(RETURNVALUE)
            return buildReturnValue(RETURNVALUE)
        RETURNVALUE[VALUE] = to_json(addr)
        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)
    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)