# -*- coding: utf-8 -*-
__author__ = 'xiliangma'


from backend.utils.LogManager import Log
from backend.errors import BackendErrorCode, BackendErrorMessage
from backend.utils.BackendUtils import dbRollback, buildReturnValue
from backend.utils.SysConstant import VALUE, CODE, MESSAGE
from FlaskManager import db
from backend.model.PShareModel import PShare
from sqlalchemy import and_, or_
import json
from datetime import datetime, timedelta
from backend.utils.BackendUtils import to_json
from sqlalchemy.sql import text


logManager = Log()
log = logManager.getLogger("PShareResourcesImpl")


def addPShare(param):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None
    try:
        pshare = PShare.query.filter(PShare.ShareId == param['shareId'], PShare.NasId == param['nasId']).first()
        if pshare is not None:
            RETURNVALUE[CODE] = BackendErrorCode.PSHARE_IS_EXIST_ERROR
            RETURNVALUE[MESSAGE] = BackendErrorMessage.PSHARE_IS_EXIST_ERROR
            log.error(RETURNVALUE)
            return buildReturnValue(RETURNVALUE)

        pshare = PShare()
        pshare.Name = param['name']
        pshare.Pwd = param['pwd']
        pshare.NasId = param['nasId']
        pshare.ShareId = param['shareId']
        pshare.Tel = param['tel']
        pshare.Type = param['type']
        shareWith = param['shareWith'].replace("'", '"').replace("u", ' ')
        pshare.ShareWith = shareWith
        pshare.Notes = param['notes']
        pshare.HEAT = param['heat']
        pshare.Thumbnail = param['thumbnail']
        # pshare.expiration = param['expiration']
        pshare.expirationType = 0 if param['expiration'] == '' else 1
        pshare.expiration = datetime.now() + timedelta(days=180) if pshare.expirationType == 0 else param['expiration']
        db.session.add(pshare)
        db.session.commit()
        RETURNVALUE[VALUE] = to_json(pshare)
        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)

    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)


def getPShares(param):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None
    try:
        page = param['page']

        limit = param['limit']
        sortField = param['sortField']
        sortType = param['sortType']
        nasId = param['nasId']
        shareId = param['shareId']
        tels = param['tels']
        type = param['type']
        shareWith = param['shareWith']
        # name = param['name']
        notes = param['notes']


        if page is None:
            page = 1

        if limit is None:
            limit = 20

        if sortField == 0 or sortField is None:
            sort = PShare.Name
        elif sortField == 1:
            sort = PShare.CreateTime
        elif sortField == 2:
            sort = PShare.HEAT
        else:
            RETURNVALUE[CODE] = BackendErrorCode.PSHARE_IS_EXIST_ERROR
            RETURNVALUE[MESSAGE] = BackendErrorMessage.PSHARE_IS_EXIST_ERROR
            log.error(RETURNVALUE)
            return buildReturnValue(RETURNVALUE)

        shareWithWords = []
        if shareWith is not None:
            for x in shareWith.split(","):
                shareWithWords.append("%" + x.strip() + "%")

        telsWords = []
        if tels is not None:
            for x in tels.split(","):
                telsWords.append("%" + x.strip() + "%")

        if nasId is None:
            nasIdFilter = PShare.NasId != 0
        else:
            nasIdFilter = PShare.NasId == nasId

        if shareId is None:
            shareIdFilter = PShare.ShareId != 0
        else:
            shareIdFilter = PShare.ShareId == shareId

        if type is None:
            typeFilter = PShare.Type != 0
        else:
            typeFilter = PShare.Type == type

        notesFilter = text("LEFT(Notes, 100) LIKE :notes")
        tt = PShare.query.filter(notesFilter)
        shareWithRule = or_(*[PShare.ShareWith.like(w) for w in shareWithWords])
        telsRule = or_(*[PShare.Tel.like(w) for w in telsWords])
        if sortType == 0 or sortType is None:
            if notes is None:
                datas = PShare.query.filter(nasIdFilter, shareIdFilter, typeFilter).filter(shareWithRule).filter(telsRule).order_by(sort.desc()).paginate(page, limit, False).items
            else:
                notes = '%{0}%'.format(notes.strip())
                datas = PShare.query.filter(nasIdFilter, shareIdFilter, typeFilter).filter(shareWithRule).filter(telsRule).filter(notesFilter).params(notes=notes).order_by(sort.desc()).paginate(page, limit, False).items
        else:
            if notes is None:
                datas = PShare.query.filter(nasIdFilter, shareIdFilter, typeFilter).filter(shareWithRule).filter(telsRule).order_by(sort.desc()).paginate(page, limit, False).items
            else:
                notes = '%{0}%'.format(notes.strip())
                datas = PShare.query.filter(nasIdFilter, shareIdFilter, typeFilter).filter(shareWithRule).filter(telsRule).filter(notesFilter).params(notes=notes).order_by(sort.desc()).paginate(page, limit, False).items
        # build return value
        for data in datas:
            pshare = {}
            pshare['id'] = data.Id
            pshare['name'] = data.Name
            pshare['pwd'] = data.Pwd
            pshare['nasId'] = data.NasId
            pshare['shareId'] = data.ShareId
            pshare['createTime'] = data.CreateTime.strftime('%Y-%m-%d %H:%M:%S')
            pshare['tel'] = data.Tel
            pshare['type'] = data.Type
            pshare['shareWith'] = json.loads(data.ShareWith)
            pshare['notes'] = data.Notes
            pshare['heat'] = data.HEAT
            pshare['thumbnail'] = data.Thumbnail
            if data.expiration <> '' and data.expiration is not None:
                pshare['expiration'] = data.expiration.strftime('%Y-%m-%d %H:%M:%S')
            pshare['expirationType'] = data.expirationType
            if data.accessTime <> '' and data.accessTime is not None:
                pshare['accessTime'] = data.accessTime.strftime('%Y-%m-%d %H:%M:%S')
            RETURNVALUE[VALUE].append(pshare)

        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)

    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)


def updatePShare(id, param):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None
    try:

        pshare = PShare.query.filter(PShare.Id == id).first()

        if pshare is None:
            RETURNVALUE[CODE] = BackendErrorCode.PSHARE_NOT_EXIST_ERROR
            RETURNVALUE[MESSAGE] = BackendErrorMessage.PSHARE_NOT_EXIST_ERROR
            log.error(RETURNVALUE)
            return buildReturnValue(RETURNVALUE)

        pshare.HEAT = pshare.HEAT + 1
        pshare.accessTime = datetime.now()
        if param['expirationType'] is not None:
            pshare.expirationType = param['expirationType']

        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)

    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = BackendErrorMessage.SYSTEM_ERROR
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)


def removePShare(param):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None
    try:
        pshares = json.loads(param["params"].replace("'", '"').replace("u", ' '))["pshares"]
        for pshare in pshares:


            if pshare.has_key('shareId'):
                shareId = pshare['shareId']
            else:
                RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
                RETURNVALUE[MESSAGE] = "shareId necessary parameters"
                log.error(RETURNVALUE)
                return buildReturnValue(RETURNVALUE)

            if pshare.has_key('nasId'):
                nasId = pshare['nasId']
            else:
                RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
                RETURNVALUE[MESSAGE] = "nasId necessary parameters"
                log.error(RETURNVALUE)
                return buildReturnValue(RETURNVALUE)

            if pshare.has_key('type'):
                typeFilter = PShare.Type == pshare['type']

            #shareWith = str(pshare['shareWith']).replace("'", '"').replace("u", ' ')

            shareIdFilter = PShare.ShareId == shareId
            nasIdFilter = PShare.NasId == nasId


            if pshare.has_key('type'):
                PShare.query.filter(shareIdFilter, nasIdFilter, typeFilter).delete()
            else:
                PShare.query.filter(shareIdFilter, nasIdFilter).delete()
            #if type == 8:
            #    PShare.query.filter(shareIdFilter, nasIdFilter, typeFilter).delete()
            #else:
            #    if shareWith == 'None':
            #        PShare.query.filter(shareIdFilter, nasIdFilter, typeFilter).delete()
            #    else:
            #        shareWithFilter = PShare.ShareWithHash == hash(str(shareWith))
            #        PShare.query.filter(shareIdFilter, nasIdFilter, typeFilter, shareWithFilter).delete()

        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)
    
    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)


def removePShareByIds(param):
    RETURNVALUE = {}
    RETURNVALUE[VALUE] = []
    RETURNVALUE[CODE] = 0
    RETURNVALUE[MESSAGE] = None
    try:
        ids = param['ids']
        idsFilter = []
        for x in ids.split(","):
            idsFilter.append(x)
        rule = or_(*[PShare.Id == w for w in idsFilter])

        PShare.query.filter(rule).delete()
        log.info(RETURNVALUE)
        return buildReturnValue(RETURNVALUE)

    except Exception as e:
        dbRollback(db)
        RETURNVALUE[CODE] = BackendErrorCode.SYSTEM_ERROR
        RETURNVALUE[MESSAGE] = e
        log.error(e.message)
        return buildReturnValue(RETURNVALUE)