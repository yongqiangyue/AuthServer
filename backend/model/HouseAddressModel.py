# -*- coding: utf-8 -*-
__author__ = 'yongqiangyue'


from FlaskManager import db
# import json


class HouseAddress(db.Model):

    __tablename__ = 'HouseAddress'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    tel = db.Column(db.BigInteger)
    addressJson = db.Column(db.LargeBinary(length=65536))

    def __repr__(self):
        return self


if __name__ == "__main__":
    pass
    # add address
    # hs = HouseAddress();
    # hs.tel = 8615810838355
    # pObj = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]
    # hs.addressJson = json.dumps(pObj)
    # db.session.add(hs)
    # db.session.commit()

    # hs2 = HouseAddress.query.first()
    # print(hs2.id, hs2.tel, hs2.addressJson)