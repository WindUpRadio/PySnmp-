import time

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from pysnmp.hlapi import *


class my_widget:
    def __init__(self):
        ui_file = QFile("form.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui_file)
        self.ui.pushButton_1.clicked.connect(self.runSnmp)
        self.ui.pushButton_2.clicked.connect(self.clearAll)
        self.ui.pushButton_3.clicked.connect(self.clearText)
        self.ui.pushButton_4.clicked.connect(self.statics)

    def runSnmp(self):
        communityName = self.ui.textEdit_1.toPlainText()
        IP = self.ui.textEdit_2.toPlainText()
        OID = self.ui.textEdit_3.toPlainText()
        if self.ui.comboBox.currentIndex() == 0:
            trail.ui.plainTextEdit.appendPlainText(str(getPrint(communityName, IP, OID)))
        if self.ui.comboBox.currentIndex() == 1:
            trail.ui.plainTextEdit.appendPlainText(str(nextPrint(communityName, IP, OID)))
        if self.ui.comboBox.currentIndex() == 2:
            times = int(self.ui.textEdit_4.toPlainText())
            bulkPrint(communityName, IP, OID, times)

    def clearAll(self):
        self.ui.textEdit_1.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()
        self.ui.textEdit_4.clear()

    def clearText(self):
        self.ui.plainTextEdit.clear()

    def statics(self):
        communityName = self.ui.textEdit_1.toPlainText()
        IP = self.ui.textEdit_2.toPlainText()
        if self.ui.comboBox_2.currentIndex() == 0:
            first = getPrint(communityName, IP, " .1.3.6.1.2.1.2.2.1.10.1")[1]
            time.sleep(3)
            second = getPrint(communityName, IP, " .1.3.6.1.2.1.2.2.1.10.1")[1]
            trail.ui.plainTextEdit.appendPlainText("In速率为" + str((int(second) - int(first)) * 8 / (3 * 1024)) + "Kbps")
        if self.ui.comboBox_2.currentIndex() == 1:
            first = getPrint(communityName, IP, "  .1.3.6.1.2.1.2.2.1.16.1")[1]
            time.sleep(3)
            second = getPrint(communityName, IP, "  .1.3.6.1.2.1.2.2.1.16.1")[1]
            trail.ui.plainTextEdit.appendPlainText("Out速率为" + str((int(second) - int(first)) * 8 / (3 * 1024)) + "Kbps")
        if self.ui.comboBox_2.currentIndex() == 2:
            trail.ui.plainTextEdit.appendPlainText("系统描述：" + getPrint(communityName, IP, " .1.3.6.1.2.1.1.1")[1])
            trail.ui.plainTextEdit.appendPlainText("系统名称：" + getPrint(communityName, IP, " .1.3.6.1.2.1.1.5")[1])
            trail.ui.plainTextEdit.appendPlainText("系统用户数：" + getPrint(communityName, IP, " .1.3.6.1.2.1.25.1.5")[1])
            trail.ui.plainTextEdit.appendPlainText("系统物理内存：" + getPrint(communityName, IP, " .1.3.6.1.2.1.25.2.2")[1])
            trail.ui.plainTextEdit.appendPlainText(
                "系统已启用的会话总数：" + getPrint(communityName, IP, " .1.3.6.1.4.1.77.1.2.7.0 ")[1])
        if self.ui.comboBox_2.currentIndex() == 3:
            num = int(getPrint(communityName, IP, " .1.3.6.1.2.1.2.1")[1])
            for i in range(num):
                trail.ui.plainTextEdit.appendPlainText(
                    "接口" + str(i) + "描述： " + getPrint(communityName, IP, " .1.3.6.1.2.1.2.2.1.2." + str(i))[1])
                trail.ui.plainTextEdit.appendPlainText(
                    "接口" + str(i) + "类型： " + getPrint(communityName, IP, " .1.3.6.1.2.1.2.2.1.3." + str(i))[1])
                trail.ui.plainTextEdit.appendPlainText(
                    "接口" + str(i) + "带宽： " + getPrint(communityName, IP, " .1.3.6.1.2.1.2.2.1.5." + str(i))[1])


def bulkPrint(communityName, ip, oid, times):
    oid = oid.lstrip()
    g = bulkCmd(SnmpEngine(),
                CommunityData(communityName, mpModel=1),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                0, 25,
                ObjectType(ObjectIdentity(oid)))
    i = times
    while i:
        i -= 1
        errorIndication, errorStatus, errorIndex, varBinds = next(g)
        for var in varBinds:
            for x in var:
                trail.ui.plainTextEdit.appendPlainText(x.prettyPrint())


def getPrint(communityName, ip, oid):
    oid = oid.lstrip()
    g = nextCmd(SnmpEngine(),
                CommunityData(communityName, mpModel=1),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)))
    errorIndication, errorStatus, errorIndex, varBinds = next(g)
    res = []
    for var in varBinds:
        for x in var:
            res.append(x.prettyPrint())
    return res


def nextPrint(communityName, ip, oid):
    oid = oid.lstrip()
    g = nextCmd(SnmpEngine(),
                CommunityData(communityName, mpModel=1),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)))
    _, _, _, _ = next(g)
    errorIndication, errorStatus, errorIndex, varBinds = next(g)
    res = []
    for var in varBinds:
        for x in var:
            res.append(x.prettyPrint())
    return res


app = QApplication([])
trail = my_widget()
trail.ui.show()
app.exec_()
