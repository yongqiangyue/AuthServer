# -*- coding: utf-8 -*-
__author__ = 'xiliangma'

from sqlalchemy.sql.sqltypes import TIMESTAMP
from FlaskManager import db
from NASDevicesModel import NASDevices
from UserModel import User


class PShare(db.Model):

    __tablename__ = 'PShare'

    Id = db.Column(db.Integer, primary_key = True)
    NasId = db.Column(db.BigInteger, db.ForeignKey(NASDevices.NasId))
    ShareId = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Pwd = db.Column(db.String(255))
    Type = db.Column(db.Integer)
    ShareWith = db.Column(db.Text)
    ShareWithHash = db.Column(db.String(255))
    Notes = db.Column(db.Text)
    Tel = db.Column(db.BigInteger, db.ForeignKey(User.Tel))
    CreateTime = db.Column(TIMESTAMP)
    HEAT = db.Column(db.Integer)
    Thumbnail = db.Column(db.LargeBinary(length=65536))
    expiration = db.Column(TIMESTAMP)

    def __repr__(self):
        return self

if __name__ == "__main__":
    pass
    # from datetime import datetime
    # t = datetime.now()
    # print(t)
    # s = PShare.query.filter(PShare.Id == 3).first()
    # # t2 = datetime.strptime(s.expiration, '%Y-%m-%d %H:%M:%S')
    # # t2 = s.expiration.strftime("%Y-%m-%d %H:%M:%S")
    # t2 = s.expiration
    # print(t2)
    # if t < t2:
    #     print('show')
    # else:
    #     print('hide')
    # print(t2)

    # s = PShare()
    # s.NasId = 114
    # s.Tel = 8615810838355
    # s.Name = 'zhang张'
    # import time
    # s.expiration = "2018-12-19 15:16:50"
    # # s.CreateTime = time.time()
    # db.session.add(s)
    # db.session.commit()
    # s = PShare.query.filter(PShare.Id == 3).first()
    # print(s.Tel, s.expiration)

    # db.create_all()
    # db.session.commit()
