# -*- coding: utf-8 -*-
__author__ = 'yongqiangyue'

from flask_restful import Resource, reqparse
from FlaskManager import httpAuth
from AppVersionResourceImpl import getAppVersion, updateAppVersion


class AppVersionAPI(Resource):
    @httpAuth.login_required
    def get(self, appName):
        return getAppVersion(appName)

    @httpAuth.login_required
    def post(self, appName):
        params = reqparse.RequestParser()
        params.add_argument("appVersion", type=str, location="json", required=True)
        return updateAppVersion(appName, params.parse_args())