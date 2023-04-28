from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
import pymysql
from pymysql.constants import CLIENT

class Win_Login:
    def __init__(self):
        self.ui = QUiLoader().load('login.ui')

        self.ui.btn_login.clicked.connect(self.onSignIn)
        self.ui.edt_password.returnPressed.connect(self.onSignIn)

    def onSignIn(self):
        if not self.ui.edt_username.text() or not self.ui.edt_password.text():
            print('请输入用户名和密码')
            return

        conn = pymysql.connect(host='124.71.219.185', user='root', password='uestc2022!',
                               database='cs2329.his', charset='utf8',
                               client_flag=CLIENT.MULTI_STATEMENTS)
        cursor = conn.cursor()
        print(self.ui.edt_username.text())
        print(self.ui.edt_password.text())
        # 注意这里的%s外要加上‘’， 否则会报错
        sql = "select * from ROOT where USERNAME='%s' and PASSWORD='%s'"%(self.ui.edt_username.text(), self.ui.edt_password.text())

        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            username = row[0]
            password = row[1]
            print("username=%s, password=%s"%(username, password))

        conn.close()


app = QApplication([])
stats = Win_Login()
stats.ui.show()
app.exec_()


