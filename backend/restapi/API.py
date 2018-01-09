# -*- coding: utf-8 -*-
__author__ = 'xiliangma'

from flask.ext.restful import Api

from FlaskManager import app
from backend.restapi.APIDocResource import APIDoc
from backend.restapi.UserResource import getRandomCodeAPI, checTelAPI, registerAPI, loginAPI, updatePwdAPI
from backend.restapi.PShareResource import addPShareAPI, getPSharesAPI, updatePShareAPI, removePShareAPI


api = Api(app)

"""
    API Doc
"""
api.add_resource(APIDoc, '/authserver')

############################ User ############################

"""
 @api {get} /api/user/<tel>/checktel
 @apiVersion 1.0.0
 @apiName checktel
 @apiGroup User
 @apiDescription  Check tel whether or not it has been registered

 @apiSuccessExample {json} Success-Response:
                    {
                    "code": 0,
                    "message": "SUCCESS",
                    "value": ""
                    }
@apiErrorExample {json} Error-Response:
                    {
                    "code": 1,
                    "message": "The phone number has been registered.",
                    "value": ""
                    }
"""
api.add_resource(checTelAPI, '/authserver/api/user/<int:tel>/checktel', endpoint = "checktel")


"""
  @api {get} api/user/<tel>/getrandomcode
  @apiVersion 1.0.0
  @apiName getrandomcode
  @apiGroup User
  @apiDescription  Get random code

  @apiSuccessExample {json} Success-Response:
                     {
                     "code": 0,
                     "message": "SUCCESS",
                     "value": ""
                     }
 @apiErrorExample {json} Error-Response:
                     {
                     "code": 1,
                     "message": "",
                     "value": ""
                     }
"""
api.add_resource(getRandomCodeAPI, '/authserver/api/user/<int:tel>/getrandomcode', endpoint = 'getrandomcode')


"""
    @api {post} /api/user/register
    @apiVersion 1.0.0
    @apiName register
    @apiGroup User
    @apiDescription  User register

    @apiParam {Number} tel required = True
    @apiParam {String} pwd required = True
    @apiParam {Number} type required = True(0 app 1 nas)
    @apiParam {Number} randomCode (type=0 required = True, type=1 required = False)
    @apiParam {String} email required = False
    @apiParam {String} name required = False

    @apiParamExample {json} Request-Example:
                          {
                            "tel":18701656257,
                            "pwd": "abc123",
                            "randomCode": 3333,
                            "type": 0,
                            "email": "894244011@qq.com",
                            "name": "test"
                          }

    @apiSuccessExample {json} Success-Response:
                        {
                        "code": 0,
                        "message": "SUCCESS",
                        "value": ""
                        }
    @apiErrorExample {json} Error-Response:
                        {
                        "code": 1,
                        "message": "",
                        "value": ""
                        }
"""
api.add_resource(registerAPI, '/authserver/api/user/register', endpoint = 'register')


"""
    @api {get} /api/user/login
    @apiVersion 1.0.0
    @apiName login
    @apiGroup User
    @apiDescription  User login

    @apiSuccessExample {json} Success-Response:
                       {
                       "code": 0,
                       "message": "SUCCESS",
                       "value": ""
                       }
    @apiErrorExample {json} Error-Response:
                       {
                       "code": 1,
                       "message": "",
                       "value": ""
                       }
"""
api.add_resource(loginAPI, '/authserver/api/user/login', endpoint = 'login')


"""
    @api {put} /api/user/<tel>/updatepwd
    @apiVersion 1.0.0
    @apiName updatepwd
    @apiGroup User
    @apiDescription  Update user pwd

    @apiParam {String} newPwd required = True
    @apiParam {Number} randomCode required = True

    @apiParamExample {json} Request-Example:
                         {
                           "newPwd": "abc123",
                           "randomCode": 3333
                         }

    @apiSuccessExample {json} Success-Response:
                      {
                      "code": 0,
                      "message": "SUCCESS",
                      "value": ""
                      }
    @apiErrorExample {json} Error-Response:
                      {
                      "code": 1,
                      "message": "",
                      "value": ""
                      }
"""
api.add_resource(updatePwdAPI, '/authserver/api/user/<int:tel>/updatepwd', endpoint = 'updatepwd')


############################ PShare ############################
"""
    @api {put} /api/pshare
    @apiVersion 1.0.0
    @apiName addPShare
    @apiGroup PShare
    @apiDescription  add public share

    @apiParam {Number} nasId required = True
    @apiParam {Number} shareId required = True
    @apiParam {String} name required = True
    @apiParam {Number} tel required = True
    @apiParam {Number} heat required = False

    @apiParamExample {json} Request-Example:
                         {
                           "nasId": 12344544,
                           "shareId": 1,
                           "name": "share1",
                           "tel": 18701656257,
                           "heat": 100
                         }

    @apiSuccessExample {json} Success-Response:
                      {
                      "code": 0,
                      "message": "SUCCESS",
                      "value": ""
                      }
    @apiErrorExample {json} Error-Response:
                      {
                      "code": 1,
                      "message": "",
                      "value": ""
                      }
"""
api.add_resource(addPShareAPI, '/authserver/api/pshare', endpoint = 'addpshare')


"""
    @api {post} /api/pshares
    @apiVersion 1.0.0
    @apiName getPShares
    @apiGroup PShare
    @apiDescription  get public shares

    @apiParam {Number} page required = False, default 1
    @apiParam {Number} limit required = False, default 20
    @apiParam {Number} sortField required = False, (default 0, name 0, createTime 1, heat 2)
    @apiParam {Number} sortType required = Flase, (default asce, asce 0, desc 1)

    @apiParamExample {json} Request-Example:
                 {
                   "page", 1,
                   "limit": 20,
                   "sortField": 0,
                   "sortType": 1
                 }

    @apiSuccessExample {json} Success-Response:
              {
              "code": 0,
              "message": "SUCCESS",
              "value": [
                {
                  "createTime": "2018-01-03 16:51:06",
                  "heat": 5,
                  "name": "share6",
                  "nasId": 123456,
                  "shaeId": 6,
                  "tel": 199
                },
                {
                  "createTime": "2018-01-03 16:51:04",
                  "heat": 3,
                  "name": "share5",
                  "nasId": 123456,
                  "shaeId": 5,
                  "tel": 188
                }
              ]
            }
    @apiErrorExample {json} Error-Response:
             {
              "code": 1,
              "message": "",
              "value": ""
              }
"""
api.add_resource(getPSharesAPI, '/authserver/api/pshares', endpoint = 'getpshares')


"""
    @api {put} /api/pshare/<int:shareId>/<int:nasId>
    @apiVersion 1.0.0
    @apiName updatePShare
    @apiGroup PShare
    @apiDescription  update public share

    @apiParam {Boolean} isHeat required = True

    @apiParamExample {json} Request-Example:
                         {
                           "isHeat": true
                         }

    @apiSuccessExample {json} Success-Response:
                      {
                      "code": 0,
                      "message": "SUCCESS",
                      "value": []
                    }
    @apiErrorExample {json} Error-Response:
                     {
                      "code": 1,
                      "message": "",
                      "value": ""
                      }
"""
api.add_resource(updatePShareAPI, '/authserver/api/pshare/<int:shareId>/<int:nasId>', endpoint = 'updatePShare')


"""
    @api {delete} /api/pshare/<int:shareId>/<int:nasId>
    @apiVersion 1.0.0
    @apiName removePShare
    @apiGroup PShare
    @apiDescription  remove public share

    @apiSuccessExample {json} Success-Response:
                      {
                      "code": 0,
                      "message": "SUCCESS",
                      "value": []
                    }
    @apiErrorExample {json} Error-Response:
                     {
                      "code": 1,
                      "message": "",
                      "value": ""
                      }
"""
api.add_resource(removePShareAPI, '/authserver/api/pshare/<int:shareId>/<int:nasId>', endpoint = 'removePShare')