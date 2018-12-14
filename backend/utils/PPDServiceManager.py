# -*- coding: utf-8 -*-
__author__ = 'xiliangma'

from backend.utils.LogManager import Log
import jpype, time, commands, os
from SysConstant import PPD_CLASS_PATH, PPD_CONFIG, PPD_PATH

logManager = Log()
log = logManager.getLogger("PPDServiceManager")

jvmArg = '-Djava.class.path=' + PPD_CLASS_PATH
jvmPath = jpype.getDefaultJVMPath()


class JpypeManager():

    def checPPDClient(self):
        errorCode = 0
        jrePath = jvmPath.split("server")[0]
        soPath = jrePath + "libpgJNI.so"
        cplibpgJNIComm = "cp " + PPD_PATH + "libpgJNI.so " + jrePath
        log.info(cplibpgJNIComm)
        if not os.path.exists(soPath):
            (errorCode, output) = commands.getstatusoutput(cplibpgJNIComm)
        return errorCode

    def startJPype(self):
        if not jpype.isJVMStarted():
            jpype.startJVM(jvmPath, jvmArg)


    def closeJPype(self):
        jpype.shutdownJVM()


class PPDClientManager():

    def loginPPDClient(self):
        JDClass = jpype.JClass('com.peergine.tool.pgTunnelSvrTool')
        oTool = JDClass()
        oTool.Run(PPD_CONFIG)
        return oTool


# if __name__ == "__main__":
#     try:
#         pass
#         # ppdManager = PPDServiceManager()
#         # ppdManager.getPPDClient()
#         # ppdManager.loginPPDClient()
#         # time.sleep(3)
#         # ppdManager.ppdUserList()
#     except Exception as e:
#         print e.message