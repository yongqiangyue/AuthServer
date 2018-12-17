# -*- coding: utf-8 -*-
__author__ = 'yongqiangyue'

from flask_restful import Resource, reqparse
from FlaskManager import httpAuth
from HouseAddressResourceImpl import getHouseAddress, updateHouseAddress


class HouseAddressAPI(Resource):
    @httpAuth.login_required
    def get(self, tel):
        return getHouseAddress(tel)

    @httpAuth.login_required
    def post(self, tel):
        params = reqparse.RequestParser()
        params.add_argument("addressJson", type=str, location="json", required=True)
        return updateHouseAddress(tel, params.parse_args())