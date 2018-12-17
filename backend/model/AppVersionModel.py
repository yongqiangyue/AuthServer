# -*- coding: utf-8 -*-
__author__ = 'yongqiangyue'


import json
from FlaskManager import db


class AppVersion(db.Model):

    __tablename__ = 'AppVersion'

    appName = db.Column(db.String(255), primary_key=True)
    appVersion = db.Column(db.String(255), default=False)

    def __repr__(self):
        return self


if __name__ == "__main__":
   pass
   # get app version
   # appName = 'android'
   # ver = AppVersion.query.filter(AppVersion.appName == appName).first()
   # print(ver.appName, ver.appVersion)
   # add app
   # app = AppVersion()
   # app.appName = 'ios'
   # app.appVersion = '0.1.0'
   # db.session.add(app)
   # db.session.commit()
   # db.create_all()
   # db.session.commit()
   # appName = 'ios'
   # ver = AppVersion.query.filter(AppVersion.appName == appName).first()
   # print(ver.appName, ver.appVersion)

   # update app version
   # appName = 'ios'
   # ver = AppVersion.query.filter(AppVersion.appName == appName).first()
   # ver.appVersion='0.3.0'
   # db.session.commit()
   # ver2 = AppVersion.query.filter(AppVersion.appName == appName).first()
   # print(ver2.appName, ver2.appVersion)