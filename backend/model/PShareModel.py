# -*- coding: utf-8 -*-
__author__ = 'xiliangma'

from sqlalchemy import text
from FlaskManager import db
from NASDevicesModel import NASDevices
from UserModel import User


class PShare(db.Model):

    __tablename__ = 'PShare'

    Id = db.Column(db.Integer, primary_key=True)
    NasId = db.Column(db.BigInteger, db.ForeignKey(NASDevices.NasId))
    ShareId = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Pwd = db.Column(db.String(255))
    Type = db.Column(db.Integer)
    ShareWith = db.Column(db.Text)
    ShareWithHash = db.Column(db.String(255))
    Notes = db.Column(db.Text)
    Tel = db.Column(db.BigInteger, db.ForeignKey(User.Tel))
    CreateTime = db.Column(db.TIMESTAMP, nullable=False, server_default=text('NOW()'))
    HEAT = db.Column(db.Integer)
    Thumbnail = db.Column(db.LargeBinary(length=65536))
    expiration = db.Column(db.TIMESTAMP)
    expirationType = db.Column(db.Integer)
    accessTime = db.Column(db.TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

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
    # from datetime import datetime, timedelta
    # s = PShare()
    # s.NasId = 114
    # s.Tel = 8615810838355
    # s.Name = 'zhang张'
    # import time
    # s.expiration = "2018-12-19 15:16:50"
    # s.expiration =  datetime.now() + timedelta(days=120)
    # s.CreateTime = time.time()
    # s.expirationType = 1
    # s.HEAT = 200
    # s.accessTime = "2088-12-19 15:16:50"
    # db.session.add(s)
    # db.session.commit()
    # print('yueyq:', s.Id)
    # s = PShare.query.filter(PShare.Id == 17).first()
    # if s.accessTime <> '' and s.accessTime is not None:
    #     print(s.accessTime.strftime('%Y-%m-%d %H:%M:%S'))
    # db.create_all()
    # db.session.commit()
