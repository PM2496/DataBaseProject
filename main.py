from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from DBOperation.JDBC import JDBC
from lib.share import ShareInfo


class Win_Login:
    def __init__(self):
        self.ui = QUiLoader().load('login.ui')

        self.ui.btn_login.clicked.connect(self.onSignIn)
        self.ui.edt_username.returnPressed.connect(self.onSignIn)
        self.ui.edt_password.returnPressed.connect(self.onSignIn)

    def onSignIn(self):
        self.ui.hide()
        self.ui.edt_password.clear()
        ShareInfo.rootWin = Win_Root()
        ShareInfo.rootWin.ui.show()
        return
        # if not self.ui.edt_username.text() or not self.ui.edt_password.text():
        #     QMessageBox.warning(
        #         self.ui,
        #         '输入完整',
        #         '请输入用户名和密码'
        #     )
        #     return

        # 注意这里的%s外要加上‘’， 否则会报错
        # sql = "select * from ROOT where USERNAME='%s' and PASSWORD='%s'" % (self.ui.edt_username.text(), self.ui.edt_password.text())

        # result = jdbc.dbQueryOne(sql)
        # # # 测试
        # # result = True
        # if result:
        #     # username = result[0]
        #     # password = result[1]
        #     # print("username=%s, password=%s" % (username, password))
        #     # 登录窗口隐藏，登录框密码清空
        #     self.ui.hide()
        #     self.ui.edt_password.clear()
        #     ShareInfo.rootWin = Win_Root()
        #     ShareInfo.rootWin.ui.show()
        # else:
        #     QMessageBox.critical(
        #         self.ui,
        #         '登录失败',
        #         '请检查用户名和密码'
        #     )


class Win_Root:
    def __init__(self):
        self.ui = QUiLoader().load('root.ui')
        # 起始状态下无行被选中，更新和删除按钮设置为不可点击
        self.ui.btn_patientUpdate.setEnabled(False)
        self.ui.btn_patientDelete.setEnabled(False)
        # 绑定各种事件
        self.ui.actionQuit.triggered.connect(self.onSignOut)
        self.ui.listWidget.currentRowChanged.connect(self.display)
        self.ui.btn_createDB.clicked.connect(self.createDB)
        self.ui.btn_importDB.clicked.connect(self.importDB)
        self.ui.btn_patientQuery.clicked.connect(self.queryPatient)
        self.ui.btn_patientUpdate.clicked.connect(self.updatePatient)
        self.ui.btn_patientInsert.clicked.connect(self.insertPatient)
        self.ui.btn_patientDelete.clicked.connect(self.deletePatient)
        self.ui.patientTable.cellClicked.connect(self.setPatientBtn)

    def onSignOut(self):
        self.ui.close()
        ShareInfo.loginWin.ui.show()

    # index = 0，初始化
    # index = 1，患者管理
    # index = 2，人事管理（医生，护士，药剂师，收银员）
    def display(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
        if index >= 1:
            tables = ['cs2329.patient', ['cs2329.doctor', 'cs2329.nurse', 'cs2329.pharmacist', 'cs2329.cashier']]
            table = tables[index-1]
            sql = "SELECT * from `%s`" % table
            tableHeaders = jdbc.dbQueryHeaders(sql)
            results = jdbc.dbQueryAll(sql)
            columnCounter = len(tableHeaders)

            widgets = [self.ui.patientTable, self.ui.HRTable, self.ui.treatTable]
            widgets[index-1].setRowCount(0)
            widgets[index-1].clearContents()
            widgets[index-1].setColumnCount(columnCounter)
            widgets[index-1].setHorizontalHeaderLabels(tableHeaders)
            for i in range(len(results)):
                widgets[index-1].insertRow(i)
                for j in range(columnCounter):
                    widgets[index-1].setItem(i, j, QTableWidgetItem(str(results[i][j])))

    def createDB(self):
        self.ui.Info.appendPlainText("开始创建表")
        if jdbc.createDB():
            self.ui.Info.appendPlainText("创建表成功")
        else:
            self.ui.Info.appendPlainText("表已存在")

    def importDB(self):
        self.ui.Info.appendPlainText("开始导入数据")
        if jdbc.importDB():
            self.ui.Info.appendPlainText("导入数据成功")
        else:
            self.ui.Info.appendPlainText("导入数据失败")

    # 选中后激活按钮
    def setPatientBtn(self):
        self.ui.btn_patientUpdate.setEnabled(True)
        self.ui.btn_patientDelete.setEnabled(True)

    def queryPatient(self):
        patientInfo = self.ui.patientInfo.text()
        # print("开始查询"+patientInfo)
        if patientInfo:
            # print(patientInfo)
            sql = "SELECT * from `cs2329.patient` where Pname LIKE '%%%s%%'" % patientInfo
            # print(sql)
        else:
            sql = "SELECT * from `cs2329.patient`"
            # print("None")
        results = jdbc.dbQueryAll(sql)
        columnCounter = len(jdbc.dbQueryHeaders("SELECT * from `cs2329.patient`"))
        self.ui.patientTable.setRowCount(0)
        self.ui.patientTable.clearContents()
        self.ui.patientTable.setColumnCount(columnCounter)
        if results:
            for i in range(len(results)):
                self.ui.patientTable.insertRow(i)
                for j in range(columnCounter):
                    self.ui.patientTable.setItem(i, j, QTableWidgetItem(str(results[i][j])))

    def updatePatient(self):
        currentRow = self.ui.patientTable.currentRow()
        # print(currentRow)
        pno = self.ui.patientTable.item(currentRow, 0).text()
        # print(pid)
        ShareInfo.patientInfoWin = Win_PatientInfo(pno)
        ShareInfo.patientInfoWin.ui.show()

        return

    def insertPatient(self):
        return

    def deletePatient(self):
        return


class Win_PatientInfo(Win_Root):
    def __init__(self, pno):
        self.ui = QUiLoader().load('patientInfo.ui')
        self.pid = pno
        # 只查询这些我们认为可以更改的属性（Pno和Pname是为了辨识患者，也无法更改）
        sql = "SELECT Pno, Pname, Pino, Pmno, Padd from `cs2329.patient` where Pno=%s" % pno
        [Pno, Pname, Pino, Pmno, Padd] = jdbc.dbQueryOne(sql)
        self.ui.pnoEdit.setText(str(Pno))
        self.ui.pnameEdit.setText(str(Pname))
        self.ui.pinoEdit.setText(str(Pino))
        self.ui.pmnoEdit.setText(str(Pmno))
        self.ui.paddEdit.setText(str(Padd))
        # pno为主键，设置为只读，pname设置为只读，
        self.ui.pnoEdit.setReadOnly(True)
        self.ui.pnameEdit.setReadOnly(True)



app = QApplication([])
jdbc = JDBC()
ShareInfo.loginWin = Win_Login()
ShareInfo.loginWin.ui.show()
app.exec_()


