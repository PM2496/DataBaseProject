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
        self.ui.actionQuit.triggered.connect(self.onSignOut)
        self.ui.listWidget.currentRowChanged.connect(self.display)
        self.ui.btn_createDB.clicked.connect(self.createDB)
        self.ui.btn_importDB.clicked.connect(self.importDB)

    def onSignOut(self):
        self.ui.close()
        ShareInfo.loginWin.ui.show()

    # index = 0，初始化
    # index = 1，管理员账户
    # index = 2，医生账户
    # index = 3，患者账户
    # index = 4，护士账户
    # index = 5，药剂师账户
    # index = 6，收银员账户
    def display(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
        if index >=1:
            tables = ['root', 'cs2329.doctor', 'cs2329.patient', 'cs2329.nurse', 'cs2329.pharmacist', 'cs2329.cashier']
            table = tables[index-1]
            sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'cs2329.his' AND TABLE_NAME = '%s';" % (table)
            tableHeaders = [ header[0] for header in list(jdbc.dbQueryAll(sql))]
            columnCounter = len(tableHeaders)

            sql = "SELECT * from `%s`" % (table)

            results = jdbc.dbQueryAll(sql)

            widgets = [self.ui.rootTable, self.ui.doctorTable, self.ui.patientTable, self.ui.nurseTable, self.ui.pharmacistTable, self.ui.cashierTable]

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


app = QApplication([])
jdbc = JDBC()
ShareInfo.loginWin = Win_Login()

ShareInfo.loginWin.ui.show()
app.exec_()


