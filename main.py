from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget
from PySide2.QtUiTools import QUiLoader
from DBOperation.JDBC import JDBC
from lib.share import ShareInfo
from PySide2.QtCore import Signal, QObject, QSize


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 更新患者信息信号, int用于区分是哪个表格（0为patient，1为patient_tel），str是对应的表格主键
    updatePatient = Signal(int, str)
    insertPatient = Signal(int)
    # 0为doctor，1为nurse，2为pharmacist，3为cashier
    updateHR = Signal(int, str)
    insertHR = Signal(int)
    # 0为就诊，1为处方，2为收费 ，str为主键
    updateTreat = Signal(int, str)
    insertTreat = Signal(int)
    # 0为入库主单，1为入库从单，2为药品类型 ，str为主键
    updateMedicine = Signal(int, str)
    insertMedicine = Signal(int)
    #
    updateRegister = Signal(int)
    insertRegister = Signal(int)
    #
    updateDept = Signal(int, str)
    insertDept = Signal(int)


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


class Win_Root(QWidget):
    def __init__(self):
        super(Win_Root, self).__init__()
        self.ui = QUiLoader().load('root.ui')
        # # 起始状态下无行被选中，更新和删除按钮设置为不可点击
        # self.ui.btn_patientUpdate.setEnabled(False)
        # self.ui.btn_patientDelete.setEnabled(False)
        # 绑定各种事件
        self.ui.actionQuit.triggered.connect(self.onSignOut)
        self.ui.listWidget.currentRowChanged.connect(self.display)

        self.ui.btn_createDB.clicked.connect(self.createDB)
        self.ui.btn_importDB.clicked.connect(self.importDB)
        # 患者表格控件
        self.ui.btn_patientQuery.clicked.connect(self.queryPatient)
        self.ui.btn_patientUpdate.clicked.connect(self.updatePatient)
        self.ui.btn_patientInsert.clicked.connect(self.insertPatient)
        self.ui.btn_patientDelete.clicked.connect(self.deletePatient)
        self.ui.patientComboBox.currentIndexChanged.connect(self.patientDisplay)
        self.ui.patientTable.cellClicked.connect(self.setPatientBtn) # 表格选中事件绑定
        # 员工表格控件
        self.ui.btn_HRQuery.clicked.connect(self.queryHR)
        self.ui.btn_HRUpdate.clicked.connect(self.updateHR)
        self.ui.btn_HRInsert.clicked.connect(self.insertHR)
        self.ui.btn_HRDelete.clicked.connect(self.deleteHR)
        self.ui.HRComboBox.currentIndexChanged.connect(self.HRDisplay)
        self.ui.HRTable.cellClicked.connect(self.setHRBtn)
        # 就诊表格控件
        # self.ui.btn_TreatQuery.clicked.connect(self.queryTreat)
        # self.ui.btn_TreatUpdate.clicked.connect(self.updateTreat)
        # self.ui.btn_TreatInsert.clicked.connect(self.insertTreat)
        # self.ui.btn_TreatDelete.clicked.connect(self.deleteTreat)
        self.ui.TreatComboBox.currentIndexChanged.connect(self.TreatDisplay)
        self.ui.TreatTable.cellClicked.connect(self.setTreatBtn)
        # 药品表格控件
        # self.ui.btn_medicineQuery.clicked.connect(self.queryMedicine)
        # self.ui.btn_medicineUpdate.clicked.connect(self.updateMedicine)
        # self.ui.btn_medicineInsert.clicked.connect(self.insertMedicine)
        # self.ui.btn_medicineDelete.clicked.connect(self.deleteMedicine)
        self.ui.MedicineComboBox.currentIndexChanged.connect(self.MedicineDisplay)
        self.ui.MedicineTable.cellClicked.connect(self.setMedicineBtn)
        # 挂号表格控件
        # self.ui.btn_registerQuery.clicked.connect(self.queryRegister)
        # self.ui.btn_registerUpdate.clicked.connect(self.updateRegister)
        # self.ui.btn_registerInsert.clicked.connect(self.insertRegister)
        # self.ui.btn_registerDelete.clicked.connect(self.deleteRegister)
        self.ui.RegisterTable.cellClicked.connect(self.setRegisterBtn)
        # 部门表格控件
        # self.ui.btn_deptQuery.clicked.connect(self.queryDept)
        # self.ui.btn_deptUpdate.clicked.connect(self.updateDept)
        # self.ui.btn_deptInsert.clicked.connect(self.insertDept)
        # self.ui.btn_deptDelete.clicked.connect(self.deleteDept)
        self.ui.DeptComboBox.currentIndexChanged.connect(self.DeptDisplay)
        self.ui.DeptTable.cellClicked.connect(self.setDeptBtn)
        # 信号绑定
        mySignals.updatePatient.connect(self.updatePatientInfo)
        mySignals.insertPatient.connect(self.patientDisplay)

        mySignals.updateHR.connect(self.updateHRInfo)
        mySignals.insertHR.connect(self.HRDisplay)

        # mySignals.updateTreat.connect(self.updateTreatInfo)
        # mySignals.insertTreat.connect(self.TreatDisplay)

        # mySignals.updateMedicine.connect(self.updateMedicineInfo)
        # mySignals.insertMedicine.connect(self.MedicineDisplay)

        # mySignals.updateRegister.connect(self.updateRegisterInfo)
        # mySignals.insertRegister.connect(self.RegisterDisplay)

        # mySignals.updateDept.connect(self.updateDept)
        # mySignals.insertDept.connect(self.DeptDisplay)

    def onSignOut(self):
        self.ui.close()
        ShareInfo.loginWin.ui.show()

    def updateTable(self, tableName, table):
        tableHeaders = None
        sql = None
        if tableName == 'cs2329.patient':
            tableHeaders = ['患者编号', '姓名', '身份证号', '社保号', '医疗卡号', '性别', '生日', '地址']
            sql = "SELECT * from `cs2329.patient`"
        elif tableName == 'cs2329.patient_tel':
            tableHeaders = ['患者电话编号', '患者编号', '患者姓名', '联系方式类型', '联系号码']
            sql = "SELECT Ptno, PT.Pno, Pname, Pteltype, Ptelcode " \
                  "from `cs2329.patient_tel` PT, `cs2329.patient` PA " \
                  "where PT.Pno = PA.Pno"
        elif tableName == 'cs2329.doctor':
            tableHeaders = ['医生编号', '姓名', '性别', '年龄', '所属部门编号', '所属部门', '职称编号', '职称', '医生注册号码', '是否专家', '挂号费用']
            sql = "SELECT Dno, Dname, Dsex, Dage, Ddeptno, DeptName, Do.Tno, Ttype, Dregno, Disex, Dfee " \
                  "from `cs2329.doctor` Do, `cs2329.dept` De, `cs2329.title` T " \
                  "where Do.Ddeptno = De.DeptNo and Do.Tno = T.Tno"
        elif tableName == 'cs2329.nurse':
            tableHeaders = ['护士编号', '姓名', '性别', '年龄', '所属部门编号', '所属部门', '职称编号', '职称', '护士证书编号', '护士级别']
            sql = "SELECT Nno, Nname, Nsex, Nage, Ndeptno, DeptName, N.Tno, Ttype, Nceno, Nlevel " \
                  "from `cs2329.nurse` N, `cs2329.dept` De, `cs2329.title` T " \
                  "where N.Ndeptno = De.DeptNo and N.Tno = T.Tno"
        elif tableName == 'cs2329.pharmacist':
            tableHeaders = ['药剂师编号', '姓名', '性别', '年龄', '所属部门编号', '所属部门', '职称编号', '职称', '药剂师证书编号', '药剂师类型']
            sql = "SELECT Phno, Phname, Phsex, Phage, Phdeptno, DeptName, P.Tno, Ttype, Phceno, Phtype " \
                  "from `cs2329.pharmacist` P, `cs2329.dept` De, `cs2329.title` T " \
                  "where P.Phdeptno = De.DeptNo and P.Tno = T.Tno"
        elif tableName == 'cs2329.cashier':
            tableHeaders = ['收银员编号', '姓名', '性别', '年龄', '所属部门编号', '所属部门', '职称编号', '职称', '收银员证书编号']
            sql = "SELECT Cno, Cname, Csex, Cage, Cdeptno, DeptName, Ca.Tno, Ttype, Cceno " \
                  "from `cs2329.cashier` Ca, `cs2329.dept` De, `cs2329.title` T " \
                  "where Ca.Cdeptno = De.DeptNo and Ca.Tno = T.Tno"
        elif tableName == 'cs2329.diagnosis':
            tableHeaders = ['诊断编号', '患者编号', '患者姓名', '医生编号', '医生姓名', '症状描述', '诊断结论', '诊断时间', '就诊费用']
            sql = "SELECT DGno, Di.Pno, Pname, Di.Dno, Dname, Symptom, Diagnosis, DGtime, Rfee " \
                  "from `cs2329.diagnosis` Di, `cs2329.patient` P, `cs2329.doctor` Do " \
                  "where Di.Pno = P.Pno and Di.Dno = Do.Dno"
        elif tableName == 'cs2329.recipe_master':
            tableHeaders = ['处方编号', '所属部门编号', '所属部门', '医生编号', '医生姓名', '患者编号', '患者姓名', '年龄', '处方时间', '处方药品清单', '费用']
            sql = "SELECT R.RMno, R.DeptNo, DeptName, R.Dno, Dname, R.Pno, Pname, RMage, RMtime " \
                  "from `cs2329.recipe_master` R, `cs2329.dept` De, `cs2329.patient` P, `cs2329.doctor` Do " \
                  "where R.DeptNo = De.DeptNo and R.Dno = Do.Dno and R.Pno = P.Pno"
        elif tableName == 'cs2329.godown_entry':
            tableHeaders = ['主单编号', '入库时间', '主单名称']
            sql = "SELECT * from `cs2329.godown_entry` "
        elif tableName == 'cs2329.godown_slave':
            tableHeaders = ['从单编号', '所属主单编号', '主单名称', '药品编号', '药品名称', '数量', '数量单位', '批次号', '价格', '有效期']
            sql = "SELECT Gs.GSno, Gs.GMno, GMname, Gs.Mno, Mname, GSnumber, GSunit, GSbatch, GSprice, GSexpdate " \
                  "from `cs2329.godown_slave` Gs, `cs2329.godown_entry` Ge, `cs2329.medicine` M " \
                  "where Gs.GMno = Ge.GMno and Gs.Mno = M.Mno"
        elif tableName == 'cs2329.medicine':
            tableHeaders = ['药品编号', '从单编号', '药品名称', '价格', '包装单位', '药品类型']
            sql = "SELECT * from `cs2329.medicine` "
        elif tableName == 'cs2329.register_form':
            tableHeaders = ['挂号单编号', '挂号科室', '科室', '挂号医生', '医生姓名', '挂号患者', '患者姓名', '挂号收费员', '收费员姓名', '挂号时间', '预约就诊时间', '挂号费', '备注']
            sql = "SELECT RFno, RFdept, DeptName, RFdoctor, Dname, RFpatient, Pname, RFcashier, Cname, RFtime, RFvisittime, RFfee, RFnotes " \
                  "from `cs2329.register_form` Rf, `cs2329.dept` De, `cs2329.doctor` Do, `cs2329.patient` P, `cs2329.cashier` C " \
                  "where Rf.RFdept = De.DeptNo and Rf.RFdoctor = Do.Dno and Rf.RFpatient = P.Pno and Rf.RFcashier = C.Cno"
        elif tableName == 'cs2329.dept':
            tableHeaders = ['部门编号', '部门名称', '父级部门编号', '父级部门名称', '部门经理编号', '部门经理名称']
            sql = "SELECT De.DeptNo, De.DeptName, De.ParentDeptNo, PD.DeptName, De.Manager, Dname " \
                  "from `cs2329.dept` De, `cs2329.dept` PD, `cs2329.doctor` D " \
                  "where De.ParentDeptNo = PD.DeptNo and De.Manager = D.Dno"
        elif tableName == 'cs2329.title':
            tableHeaders = ['职称编号', '工资类型', '工资', '职称类型', '所属行业']
            sql = "SELECT Tno, T.Sno, Snumber, Ttype, Ttrade " \
                  "from `cs2329.title` T, `cs2329.salary` S " \
                  "where T.Sno = S.Sno"
        elif tableName == 'cs2329.salary':
            tableHeaders = ['工资编号', '工资等级', '工资数量']
            sql = "SELECT Sno, Slevel, Snumber " \
                  "from `cs2329.salary` "

        results = jdbc.dbQueryAll(sql)
        table.setRowCount(0)
        table.clearContents()
        if results:
            columnCounter = len(tableHeaders)
            table.setColumnCount(columnCounter)
            table.setHorizontalHeaderLabels(tableHeaders)
            if tableName == 'cs2329.recipe_master':
                columnCounter = columnCounter - 2  # 后两列用于添加按钮
                for i in range(len(results)):
                    table.insertRow(i)
                    for j in range(columnCounter):
                        table.setItem(i, j, QTableWidgetItem(str(results[i][j])))
                    # 创建按钮
                    btn_recipe_detail = QPushButton("药品详情")
                    btn_fee = QPushButton("费用详情")
                    # 编辑按钮样式
                    btn_recipe_detail.setFixedSize(QSize(120, 40))
                    btn_fee.setFixedSize(QSize(120, 40))
                    btn_recipe_detail.setStyleSheet(
                        "QPushButton{color:white;background-color:rgb(51,204,255);font-family:黑体;border-radius: 15px;}"
                        "QPushButton:pressed{background-color:rgb(51,129,172)}")
                    btn_fee.setStyleSheet(
                        "QPushButton{color:white;background-color:rgb(51,204,255);font-family:黑体;border-radius: 15px;}"
                        "QPushButton:pressed{background-color:rgb(51,129,172)}")
                    btn_recipe_detail.clicked.connect(self.showRecipe_Detail_Info)
                    btn_fee.clicked.connect(self.showFee_Info)
                    vLayout1 = QHBoxLayout()
                    vLayout2 = QHBoxLayout()
                    widget_btn1 = QWidget()
                    widget_btn2 = QWidget()
                    vLayout1.addWidget(btn_recipe_detail)  # 布局中添加了控件
                    vLayout2.addWidget(btn_fee)
                    widget_btn1.setLayout(vLayout1)  # Widget中添加布局
                    widget_btn2.setLayout(vLayout2)
                    table.setCellWidget(i, columnCounter, widget_btn1)  # 表格中添加Widget
                    table.setCellWidget(i, columnCounter+1, widget_btn2)
            else:
                for i in range(len(results)):
                    table.insertRow(i)
                    for j in range(columnCounter):
                        table.setItem(i, j, QTableWidgetItem(str(results[i][j])))
    # 展示处方药品详情
    def showRecipe_Detail_Info(self):
        button = self.sender()
        if button:
            # 确定按钮所在行号
            row = self.ui.TreatTable.indexAt(button.parent().pos()).row()
            rmno = self.ui.TreatTable.item(row, 0).text()
            ShareInfo.Recipe_Detail_Win = Win_Recipe_Detail(rmno)
            ShareInfo.Recipe_Detail_Win.ui.show()

    # 展示处方药品详情
    def showFee_Info(self):
        button = self.sender()
        if button:
            # 确定按钮所在行号
            row = self.ui.TreatTable.indexAt(button.parent().pos()).row()
            rmno = self.ui.TreatTable.item(row, 0).text()
            ShareInfo.FeeWin = Win_Fee(rmno)
            ShareInfo.FeeWin.ui.show()

    def patientDisplay(self, index):
        self.resetBtn(0)
        tables = ['cs2329.patient', 'cs2329.patient_tel']
        tableName = tables[index]
        self.updateTable(tableName, self.ui.patientTable)

    def HRDisplay(self, index):
        self.resetBtn(1)
        tables = ['cs2329.doctor', 'cs2329.nurse', 'cs2329.pharmacist', 'cs2329.cashier']
        tableName = tables[index]
        self.updateTable(tableName, self.ui.HRTable)

    def TreatDisplay(self, index):
        self.resetBtn(2)
        tables = ['cs2329.diagnosis', 'cs2329.recipe_master']
        tableName = tables[index]
        self.updateTable(tableName, self.ui.TreatTable)

    def MedicineDisplay(self, index):
        self.resetBtn(3)
        tables = ['cs2329.godown_entry', 'cs2329.godown_slave', 'cs2329.medicine']
        tableName = tables[index]
        self.updateTable(tableName, self.ui.MedicineTable)

    def RegisterDisplay(self):
        self.resetBtn(4)
        tableName = 'cs2329.register_form'
        self.updateTable(tableName, self.ui.RegisterTable)

    def DeptDisplay(self, index):
        self.resetBtn(5)
        tables = ['cs2329.dept', 'cs2329.title', 'cs2329.salary']
        tableName = tables[index]
        self.updateTable(tableName, self.ui.DeptTable)

    # index = 0，初始化
    # index = 1，患者管理
    # index = 2，人事管理（医生，护士，药剂师，收银员）
    # index = 3，就诊管理（就诊表，处方表，药品表，费用表）
    # index = 4，药品管理（入库，出库，药品类型）
    # index = 5，挂号管理
    # index = 6，部门管理（组织机构，职称，工资）
    def display(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
        if index >= 1:
            if index == 1:
                self.ui.patientComboBox.setCurrentIndex(0)
                self.patientDisplay(0)
            if index == 2:
                self.ui.HRComboBox.setCurrentIndex(0)
                self.HRDisplay(0)
            if index == 3:
                self.ui.TreatComboBox.setCurrentIndex(0)
                self.TreatDisplay(0)
            if index == 4:
                self.ui.MedicineComboBox.setCurrentIndex(0)
                self.MedicineDisplay(0)
            if index == 5:
                self.RegisterDisplay()
            if index == 6:
                self.ui.DeptComboBox.setCurrentIndex(0)
                self.DeptDisplay(0)

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

    def setHRBtn(self):
        self.ui.btn_HRUpdate.setEnabled(True)
        self.ui.btn_HRDelete.setEnabled(True)

    def setTreatBtn(self):
        # print(self.ui.TreatTable.currentRow())
        self.ui.btn_TreatUpdate.setEnabled(True)
        self.ui.btn_TreatDelete.setEnabled(True)

    def setMedicineBtn(self):
        self.ui.btn_medicineUpdate.setEnabled(True)
        self.ui.btn_medicineDelete.setEnabled(True)

    def setRegisterBtn(self):
        self.ui.btn_registerUpdate.setEnabled(True)
        self.ui.btn_registerDelete.setEnabled(True)

    def setDeptBtn(self):
        self.ui.btn_deptUpdate.setEnabled(True)
        self.ui.btn_deptDelete.setEnabled(True)

    # 重置按钮
    # index用于区分是哪个表格的按钮
    # 0: patientTable
    # 1: HRTable
    # 2: TreatTable
    # 3: MedicineTable
    # 4: RegisterTable
    def resetBtn(self, index):
        if index == 0:
            self.ui.btn_patientUpdate.setEnabled(False)
            self.ui.btn_patientDelete.setEnabled(False)
        if index == 1:
            self.ui.btn_HRUpdate.setEnabled(False)
            self.ui.btn_HRDelete.setEnabled(False)
        if index == 2:
            self.ui.btn_TreatUpdate.setEnabled(False)
            self.ui.btn_TreatDelete.setEnabled(False)
        if index == 3:
            self.ui.btn_medicineUpdate.setEnabled(False)
            self.ui.btn_medicineDelete.setEnabled(False)
        if index == 4:
            self.ui.btn_registerUpdate.setEnabled(False)
            self.ui.btn_registerDelete.setEnabled(False)
        if index == 5:
            self.ui.btn_deptUpdate.setEnabled(False)
            self.ui.btn_deptDelete.setEnabled(False)

    def queryPatient(self):
        patientInfo = self.ui.patientInfo.text()
        # print("开始查询"+patientInfo)
        currentIndex = self.ui.patientComboBox.currentIndex()

        if patientInfo:
            if currentIndex == 0:
                sql = "SELECT * from `cs2329.patient` PA where PA.Pname  LIKE '%%%s%%'" % patientInfo
                columnCounter = 8
            else:
                sql = "SELECT Ptno, PT.Pno, Pname, Pteltype, Ptelcode " \
                      "from `cs2329.patient_tel` PT, `cs2329.patient` PA " \
                      "where PT.Pno = PA.Pno and PA.Pname LIKE '%%%s%%'" % patientInfo
                columnCounter = 5
        else:
            if currentIndex == 0:
                sql = "SELECT * from `cs2329.patient`"
                columnCounter = 8
            else:
                sql = "SELECT Ptno, PT.Pno, Pname, Pteltype, Ptelcode " \
                      "from `cs2329.patient_tel` PT, `cs2329.patient` PA " \
                      "where PT.Pno = PA.Pno"
                columnCounter = 5
        results = jdbc.dbQueryAll(sql)
        self.ui.patientTable.setRowCount(0)
        self.ui.patientTable.clearContents()
        self.ui.patientTable.setColumnCount(columnCounter)
        if results:
            for i in range(len(results)):
                self.ui.patientTable.insertRow(i)
                for j in range(columnCounter):
                    self.ui.patientTable.setItem(i, j, QTableWidgetItem(str(results[i][j])))

    def updatePatient(self):
        currentIndex = self.ui.patientComboBox.currentIndex()
        currentRow = self.ui.patientTable.currentRow()
        if currentIndex == 0:
            pno = self.ui.patientTable.item(currentRow, 0).text()
            ShareInfo.updatePatientWin = Win_updatePatient(pno)
            ShareInfo.updatePatientWin.ui.show()
        else:
            ptno = self.ui.patientTable.item(currentRow, 0).text()
            ShareInfo.updatePatientTelWin = Win_updatePatientTel(ptno)
            ShareInfo.updatePatientTelWin.ui.show()

    def updatePatientInfo(self, index, key):
        currentRow = self.ui.patientTable.currentRow()
        if index == 0:
            sql = "SELECT * from `cs2329.patient` where Pno=%s" % key
        else:
            sql = "SELECT Ptno, PT.Pno, Pname, Pteltype, Ptelcode " \
                  "from `cs2329.patient_tel` PT, `cs2329.patient` PA " \
                  "where PT.Pno = PA.Pno and Ptno=%s" % key
        results = jdbc.dbQueryOne(sql)
        for i in range(len(results)):
            self.ui.patientTable.setItem(currentRow, i, QTableWidgetItem(str(results[i])))

    def insertPatient(self):
        currentIndex = self.ui.patientComboBox.currentIndex()
        if currentIndex == 0:
            ShareInfo.insertPatientWin = Win_insertPatient()
            ShareInfo.insertPatientWin.ui.show()
        else:
            ShareInfo.insertPatientTelWin = Win_insertPatientTel()
            ShareInfo.insertPatientTelWin.ui.show()

    def deletePatient(self):
        currentRow = self.ui.patientTable.currentRow()
        currentIndex = self.ui.patientComboBox.currentIndex()
        tables = [['cs2329.patient', 'Pno'], ['cs2329.patient_tel', 'Ptno']]
        sql = "DELETE from `%s` where %s = %s" % (tables[currentIndex][0], tables[currentIndex][1], int(self.ui.patientTable.item(currentRow, 0).text()))

        jdbc.dbDelete(sql)
        self.patientDisplay(currentIndex)

    def queryHR(self):
        HRInfo = self.ui.HRInfo.text()
        currentIndex = self.ui.HRComboBox.currentIndex()
        if HRInfo:
            if currentIndex == 0:
                sql = "SELECT Dno, Dname, Dsex, Dage, Ddeptno, DeptName, Do.Tno, Ttype, Dregno, Disex, Dfee " \
                      "from `cs2329.doctor` Do, `cs2329.dept` De, `cs2329.title` T " \
                      "where Do.Ddeptno = De.DeptNo and Do.Tno = T.Tno and Dname LIKE '%%%s%%'" % HRInfo
                columnCounter = 11
            elif currentIndex == 1:
                sql = "SELECT Nno, Nname, Nsex, Nage, Ndeptno, DeptName, N.Tno, Ttype, Nceno, Nlevel " \
                      "from `cs2329.nurse` N, `cs2329.dept` De, `cs2329.title` T " \
                      "where N.Ndeptno = De.DeptNo and N.Tno = T.Tno and Nname LIKE '%%%s%%'" % HRInfo
                columnCounter = 10
            elif currentIndex == 2:
                sql = "SELECT Phno, Phname, Phsex, Phage, Phdeptno, DeptName, P.Tno, Ttype, Phceno, Phtype " \
                      "from `cs2329.pharmacist` P, `cs2329.dept` De, `cs2329.title` T " \
                      "where P.Phdeptno = De.DeptNo and P.Tno = T.Tno and Phname LIKE '%%%s%%'" % HRInfo
                columnCounter = 10
            elif currentIndex == 3:
                sql = "SELECT Cno, Cname, Csex, Cage, Cdeptno, DeptName, Ca.Tno, Ttype, Cceno " \
                      "from `cs2329.cashier` Ca, `cs2329.dept` De, `cs2329.title` T " \
                      "where Ca.Cdeptno = De.DeptNo and Ca.Tno = T.Tno and Cname LIKE '%%%s%%'" %HRInfo
                columnCounter = 9
        else:
            if currentIndex == 0:
                sql = "SELECT Dno, Dname, Dsex, Dage, Ddeptno, DeptName, Do.Tno, Ttype, Dregno, Disex, Dfee " \
                      "from `cs2329.doctor` Do, `cs2329.dept` De, `cs2329.title` T " \
                      "where Do.Ddeptno = De.DeptNo and Do.Tno = T.Tno"
                columnCounter = 11
            elif currentIndex == 1:
                sql = "SELECT Nno, Nname, Nsex, Nage, Ndeptno, DeptName, N.Tno, Ttype, Nceno, Nlevel " \
                      "from `cs2329.nurse` N, `cs2329.dept` De, `cs2329.title` T " \
                      "where N.Ndeptno = De.DeptNo and N.Tno = T.Tno"
                columnCounter = 10
            elif currentIndex == 2:
                sql = "SELECT Phno, Phname, Phsex, Phage, Phdeptno, DeptName, P.Tno, Ttype, Phceno, Phtype " \
                      "from `cs2329.pharmacist` P, `cs2329.dept` De, `cs2329.title` T " \
                      "where P.Phdeptno = De.DeptNo and P.Tno = T.Tno"
                columnCounter = 10
            elif currentIndex == 3:
                sql = "SELECT Cno, Cname, Csex, Cage, Cdeptno, DeptName, Ca.Tno, Ttype, Cceno " \
                      "from `cs2329.cashier` Ca, `cs2329.dept` De, `cs2329.title` T " \
                      "where Ca.Cdeptno = De.DeptNo and Ca.Tno = T.Tno"
                columnCounter = 9

        results = jdbc.dbQueryAll(sql)
        self.ui.HRTable.setRowCount(0)
        self.ui.HRTable.clearContents()
        self.ui.HRTable.setColumnCount(columnCounter)
        if results:
            for i in range(len(results)):
                self.ui.HRTable.insertRow(i)
                for j in range(columnCounter):
                    self.ui.HRTable.setItem(i, j, QTableWidgetItem(str(results[i][j])))

    def updateHR(self):
        currentIndex = self.ui.HRComboBox.currentIndex()
        currentRow = self.ui.HRTable.currentRow()
        if currentIndex == 0:
            dno = self.ui.HRTable.item(currentRow, 0).text()
            ShareInfo.updateDoctorWin = Win_updateDoctor(dno)
            ShareInfo.updateDoctorWin.ui.show()
        elif currentIndex == 1:
            nno = self.ui.HRTable.item(currentRow, 0).text()
            ShareInfo.updateNurseWin = Win_updateNurse(nno)
            ShareInfo.updateNurseWin.ui.show()
        elif currentIndex == 2:
            phno = self.ui.HRTable.item(currentRow, 0).text()
            ShareInfo.updatePharmacistWin = Win_updatePharmacist(phno)
            ShareInfo.updatePharmacistWin.ui.show()
        elif currentIndex == 3:
            cno = self.ui.HRTable.item(currentRow, 0).text()
            ShareInfo.updateCashierWin = Win_updateCashier(cno)
            ShareInfo.updateCashierWin.ui.show()

    def updateHRInfo(self, index, key):
        currentRow = self.ui.HRTable.currentRow()
        if index == 0:
            sql = "SELECT Dno, Dname, Dsex, Dage, Ddeptno, DeptName, Do.Tno, Ttype, Dregno, Disex, Dfee " \
                  "from `cs2329.doctor` Do, `cs2329.dept` De, `cs2329.title` T " \
                  "where Do.Ddeptno = De.DeptNo and Do.Tno = T.Tno and Dno=%s" % key
        elif index == 1:
            sql = "SELECT Nno, Nname, Nsex, Nage, Ndeptno, DeptName, N.Tno, Ttype, Nceno, Nlevel " \
                  "from `cs2329.nurse` N, `cs2329.dept` De, `cs2329.title` T " \
                  "where N.Ndeptno = De.DeptNo and N.Tno = T.Tno and Nno=%s" % key
        elif index == 2:
            sql = "SELECT Phno, Phname, Phsex, Phage, Phdeptno, DeptName, P.Tno, Ttype, Phceno, Phtype " \
                  "from `cs2329.pharmacist` P, `cs2329.dept` De, `cs2329.title` T " \
                  "where P.Phdeptno = De.DeptNo and P.Tno = T.Tno and Phno=%s" % key
        elif index == 3:
            sql = "SELECT Cno, Cname, Csex, Cage, Cdeptno, DeptName, Ca.Tno, Ttype, Cceno " \
                  "from `cs2329.cashier` Ca, `cs2329.dept` De, `cs2329.title` T " \
                  "where Ca.Cdeptno = De.DeptNo and Ca.Tno = T.Tno and Cno=%s" % key
        results = jdbc.dbQueryOne(sql)
        for i in range(len(results)):
            self.ui.HRTable.setItem(currentRow, i, QTableWidgetItem(str(results[i])))

    def insertHR(self):
        currentIndex = self.ui.HRComboBox.currentIndex()
        if currentIndex == 0:
            ShareInfo.insertDoctorWin = Win_insertDoctor()
            ShareInfo.insertDoctorWin.ui.show()
        elif currentIndex == 1:
            ShareInfo.insertNurseWin = Win_insertNurse()
            ShareInfo.insertNurseWin.ui.show()
        elif currentIndex == 2:
            ShareInfo.insertPharmacistWin = Win_insertPharmacist()
            ShareInfo.insertPharmacistWin.ui.show()
        elif currentIndex == 3:
            ShareInfo.insertCashierWin = Win_insertCashier()
            ShareInfo.insertCashierWin.ui.show()
    def deleteHR(self):
        currentRow = self.ui.HRTable.currentRow()
        currentIndex = self.ui.HRComboBox.currentIndex()
        tables = [['cs2329.doctor', 'Dno'], ['cs2329.nurse', 'Nno'], ['cs2329.pharmacist', 'Phno'], ['cs2329.cashier', 'Cno']]
        sql = "DELETE from `%s` where %s = %s" % (tables[currentIndex][0], tables[currentIndex][1], int(self.ui.HRTable.item(currentRow, 0).text()))

        jdbc.dbDelete(sql)
        self.HRDisplay(currentIndex)


class Win_updatePatient:
    def __init__(self, pno):
        self.ui = QUiLoader().load('updatePatient.ui')
        self.pno = pno
        # 只查询这些我们认为可以更改的属性（Pno是为了辨识患者，无法更改）
        sql = "SELECT Pno, Pname, Pino, Pmno, Padd from `cs2329.patient` where Pno=%s" % pno
        [Pno, Pname, Pino, Pmno, Padd] = jdbc.dbQueryOne(sql)
        self.ui.pnoEdit.setText(str(Pno))
        self.ui.pnameEdit.setText(str(Pname))
        self.ui.pinoEdit.setText(str(Pino))
        self.ui.pmnoEdit.setText(str(Pmno))
        self.ui.paddEdit.setText(str(Padd))
        # pno为主键，设置为只读
        self.ui.pnoEdit.setReadOnly(True)
        # self.ui.pnameEdit.setReadOnly(True)
        self.ui.btn_update.clicked.connect(self.updateInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def updateInfo(self):
        pno = self.ui.pnoEdit.text()
        pname = self.ui.pnameEdit.text()
        pino = self.ui.pinoEdit.text()
        pmno = self.ui.pmnoEdit.text()
        padd = self.ui.paddEdit.text()
        sql = "update `cs2329.patient` set Pname='%s', Pino='%s', Pmno='%s', Padd='%s' where Pno = %s" % (pname, pino, pmno, padd, pno)
        # 需要对patientTable数据进行更新
        if jdbc.dbUpdate(sql):
            mySignals.updatePatient.emit(0, self.pno)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_insertPatient:
    def __init__(self):
        self.ui = QUiLoader().load('insertPatient.ui')
        self.ui.btn_insert.clicked.connect(self.insertInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def insertInfo(self):
        pno = self.ui.pnoEdit.text()
        pname = self.ui.pnameEdit.text()
        pid = self.ui.pidEdit.text()
        pino = self.ui.pinoEdit.text()
        pmno = self.ui.pmnoEdit.text()
        if self.ui.rbtn_male.isChecked():
            psex = '男'
        else:
            psex = '女'
        pbd = self.ui.pbdEdit.text()
        padd = self.ui.paddEdit.text()
        mTel = self.ui.mTelEdit.text()

        sql1 = "insert into `cs2329.patient` (Pno, Pname, Pid, Pino, Pmno, Psex, Pbd, Padd) values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (pno, pname, pid, pino, pmno, psex, pbd, padd)
        sql2 = "insert into `cs2329.patient_tel` (Pno, Pteltype, Ptelcode) values (%s, '%s', '%s')" % (pno, "手机", mTel)

        # 需要对patientTable数据进行更新
        if jdbc.dbInsert(sql1) and jdbc.dbInsert(sql2):
            mySignals.insertPatient.emit(0)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_updatePatientTel:
    def __init__(self, ptno):
        self.ui = QUiLoader().load('updatePatientTel.ui')
        self.ptno = ptno
        # 只查询这些我们认为可以更改的属性（Pno和Pname是为了辨识患者，也无法更改）
        sql = "SELECT Ptno, Pno, Pteltype, Ptelcode from `cs2329.patient_tel` where Ptno=%s" % ptno
        [Ptno, Pno, Pteltype, Ptelcode] = jdbc.dbQueryOne(sql)
        self.ui.ptnoEdit.setText(str(Ptno))
        self.ui.pnoEdit.setText(str(Pno))
        self.ui.pteltypeEdit.setText(str(Pteltype))
        self.ui.ptelcodeEdit.setText(str(Ptelcode))
        # pno为主键，设置为只读，pname设置为只读，
        self.ui.ptnoEdit.setReadOnly(True)
        self.ui.pnoEdit.setReadOnly(True)
        self.ui.btn_update.clicked.connect(self.updateInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def updateInfo(self):
        ptno = self.ui.ptnoEdit.text()
        pteltype = self.ui.pteltypeEdit.text()
        ptelcode = self.ui.ptelcodeEdit.text()
        sql = "update `cs2329.patient_tel` set Pteltype='%s', Ptelcode='%s' where Ptno = %s" % (pteltype, ptelcode, ptno)
        # 需要对patientTable数据进行更新
        if jdbc.dbUpdate(sql):
            mySignals.updatePatient.emit(1, self.ptno)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_insertPatientTel:
    def __init__(self):
        self.ui = QUiLoader().load('insertPatientTel.ui')
        self.ui.btn_insert.clicked.connect(self.insertInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def insertInfo(self):
        ptno = self.ui.ptnoEdit.text()
        pno = self.ui.pnoEdit.text()
        pteltype = self.ui.pteltypeEdit.text()
        ptelcode = self.ui.ptelcodeEdit.text()

        sql = "insert into `cs2329.patient_tel` (Ptno, Pno, Pteltype, Ptelcode) values (%s, %s, '%s', '%s')" % (ptno, pno, pteltype, ptelcode)

        # 需要对patientTable数据进行更新
        if jdbc.dbInsert(sql):
            mySignals.insertPatient.emit(1)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_updateDoctor:
    def __init__(self, dno):
        self.ui = QUiLoader().load('updateDoctor.ui')
        self.Dno = dno

        sql = "SELECT Dno, Dname, Dsex, Dage, Ddeptno, Tno, Dregno, Disex, Dfee from `cs2329.doctor` where Dno=%s" % dno
        [Dno, Dname, Dsex, Dage, Ddeptno, Tno, Dregno, Disex, Dfee] = jdbc.dbQueryOne(sql)
        self.ui.DnoEdit.setText(str(Dno))
        self.ui.DnameEdit.setText(str(Dname))
        if str(Dsex) == '男':
            self.ui.rbtn_male.setChecked(True)
        else:
            self.ui.rbtn_female.setChecked(True)
        self.ui.DageEdit.setText(str(Dage))
        self.ui.DdeptnoEdit.setText(str(Ddeptno))
        self.ui.TnoEdit.setText(str(Tno))
        self.ui.DregnoEdit.setText(str(Dregno))
        if str(Disex) == '是':
            self.ui.rbtn_isex.setChecked(True)
        else:
            self.ui.rbtn_notex.setChecked(True)
        self.ui.DfeeEdit.setText(str(Dfee))
        # dno为主键，设置为只读
        self.ui.DnoEdit.setReadOnly(True)

        self.ui.btn_update.clicked.connect(self.updateInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def updateInfo(self):
        dno = self.ui.DnoEdit.text()
        dname = self.ui.DnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            dsex = '男'
        else:
            dsex = '女'
        dage = self.ui.DageEdit.text()
        ddeptno = self.ui.DdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        dregno = self.ui.DregnoEdit.text()
        if self.ui.rbtn_isex.isChecked():
            disex = '是'
        else:
            disex = '否'
        dfee = self.ui.DfeeEdit.text()
        sql = "update `cs2329.doctor` set Dname='%s', Dsex='%s', Dage=%s, Ddeptno=%s, Tno=%s, Dregno='%s', Disex='%s', Dfee=%s where Dno = %s" % (dname, dsex, dage, ddeptno, tno, dregno, disex, dfee, dno)
        # 需要对HRTable数据进行更新
        if jdbc.dbUpdate(sql):
            mySignals.updateHR.emit(0, self.Dno)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_insertDoctor:
    def __init__(self):
        self.ui = QUiLoader().load('insertDoctor.ui')
        self.ui.btn_insert.clicked.connect(self.insertInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def insertInfo(self):
        dno = self.ui.DnoEdit.text()
        dname = self.ui.DnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            dsex = '男'
        else:
            dsex = '女'
        dage = self.ui.DageEdit.text()
        ddeptno = self.ui.DdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        dregno = self.ui.DregnoEdit.text()
        if self.ui.rbtn_isex.isChecked():
            disex = '是'
        else:
            disex = '否'
        dfee = self.ui.DfeeEdit.text()

        sql = "insert into `cs2329.doctor` (Dno, Dname, Dsex, Dage, Ddeptno, Tno, Dregno, Disex, Dfee) values (%s, '%s', '%s', %s, %s, %s, '%s', '%s', %s)" % (
        dno, dname, dsex, dage, ddeptno, tno, dregno, disex, dfee)

        # 需要对HRTable数据进行更新
        if jdbc.dbInsert(sql):
            mySignals.insertHR.emit(0)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_updateNurse:
    def __init__(self, nno):
        self.ui = QUiLoader().load('updateNurse.ui')
        self.Nno = nno

        sql = "SELECT Nno, Nname, Nsex, Nage, Ndeptno, Tno, Nceno, Nlevel from `cs2329.nurse` where Nno=%s" % nno
        [Nno, Nname, Nsex, Nage, Ndeptno, Tno, Nceno, Nlevel] = jdbc.dbQueryOne(sql)
        self.ui.NnoEdit.setText(str(Nno))
        self.ui.NnameEdit.setText(str(Nname))
        if str(Nsex) == '男':
            self.ui.rbtn_male.setChecked(True)
        else:
            self.ui.rbtn_female.setChecked(True)
        self.ui.NageEdit.setText(str(Nage))
        self.ui.NdeptnoEdit.setText(str(Ndeptno))
        self.ui.TnoEdit.setText(str(Tno))
        self.ui.NcenoEdit.setText(str(Nceno))
        self.ui.NlevelEdit.setText(str(Nlevel))
        # nno为主键，设置为只读
        self.ui.NnoEdit.setReadOnly(True)

        self.ui.btn_update.clicked.connect(self.updateInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def updateInfo(self):
        nno = self.ui.NnoEdit.text()
        nname = self.ui.NnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            nsex = '男'
        else:
            nsex = '女'
        nage = self.ui.NageEdit.text()
        ndeptno = self.ui.NdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        nceno = self.ui.NcenoEdit.text()
        nlevel = self.ui.NlevelEdit.text()
        sql = "update `cs2329.nurse` set Nname='%s', Nsex='%s', Nage=%s, Ndeptno=%s, Tno=%s, Nceno='%s', Nlevel='%s' where Nno = %s" % (nname, nsex, nage, ndeptno, tno, nceno, nlevel, nno)
        # 需要对patientTable数据进行更新
        if jdbc.dbUpdate(sql):
            mySignals.updateHR.emit(1, self.Nno)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_insertNurse:
    def __init__(self):
        self.ui = QUiLoader().load('insertNurse.ui')
        self.ui.btn_insert.clicked.connect(self.insertInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def insertInfo(self):
        nno = self.ui.NnoEdit.text()
        nname = self.ui.NnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            nsex = '男'
        else:
            nsex = '女'
        nage = self.ui.NageEdit.text()
        ndeptno = self.ui.NdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        nceno = self.ui.NcenoEdit.text()
        nlevel = self.ui.NlevelEdit.text()

        sql = "insert into `cs2329.nurse` (Nno, Nname, Nsex, Nage, Ndeptno, Tno, Nceno, Nlevel) values (%s, '%s', '%s', %s, %s, %s, '%s', '%s')" % (
        nno, nname, nsex, nage, ndeptno, tno, nceno, nlevel)

        # 需要对patientTable数据进行更新
        if jdbc.dbInsert(sql):
            mySignals.insertHR.emit(1)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_updatePharmacist:
    def __init__(self, phno):
        self.ui = QUiLoader().load('updatePharmacist.ui')
        self.Phno = phno

        sql = "SELECT Phno, Phname, Phsex, Phage, Phdeptno, Tno, Phceno, Phtype from `cs2329.pharmacist` where Phno=%s" % phno
        [Phno, Phname, Phsex, Phage, Phdeptno, Tno, Phceno, Phtype] = jdbc.dbQueryOne(sql)
        self.ui.PhnoEdit.setText(str(Phno))
        self.ui.PhnameEdit.setText(str(Phname))
        if str(Phsex) == '男':
            self.ui.rbtn_male.setChecked(True)
        else:
            self.ui.rbtn_female.setChecked(True)
        self.ui.PhageEdit.setText(str(Phage))
        self.ui.PhdeptnoEdit.setText(str(Phdeptno))
        self.ui.TnoEdit.setText(str(Tno))
        self.ui.PhcenoEdit.setText(str(Phceno))
        self.ui.PhtypeEdit.setText(str(Phtype))
        # pno为主键，设置为只读
        self.ui.PhnoEdit.setReadOnly(True)
        # self.ui.pnameEdit.setReadOnly(True)
        self.ui.btn_update.clicked.connect(self.updateInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def updateInfo(self):
        phno = self.ui.PhnoEdit.text()
        phname = self.ui.PhnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            phsex = '男'
        else:
            phsex = '女'
        phage = self.ui.PhageEdit.text()
        phdeptno = self.ui.PhdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        phceno = self.ui.PhcenoEdit.text()
        phtype = self.ui.PhtypeEdit.text()
        sql = "update `cs2329.pharmacist` set Phname='%s', Phsex='%s', Phage=%s, Phdeptno=%s, Tno=%s, Phceno='%s', Phtype='%s' where Phno = %s" % (phname, phsex, phage, phdeptno, tno, phceno, phtype, phno)

        if jdbc.dbUpdate(sql):
            mySignals.updateHR.emit(2, self.Phno)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_insertPharmacist:
    def __init__(self):
        self.ui = QUiLoader().load('insertPharmacist.ui')
        self.ui.btn_insert.clicked.connect(self.insertInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def insertInfo(self):
        phno = self.ui.PhnoEdit.text()
        phname = self.ui.PhnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            phsex = '男'
        else:
            phsex = '女'
        phage = self.ui.PhageEdit.text()
        phdeptno = self.ui.PhdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        phceno = self.ui.PhcenoEdit.text()
        phtype = self.ui.PhtypeEdit.text()

        sql = "insert into `cs2329.pharmacist` (Phno, Phname, Phsex, Phage, Phdeptno, Tno, Phceno, Phtype) values (%s, '%s', '%s', %s, %s, %s, '%s', '%s')" % (
        phno, phname, phsex, phage, phdeptno, tno, phceno, phtype)

        if jdbc.dbInsert(sql):
            mySignals.insertHR.emit(2)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_updateCashier:
    def __init__(self, cno):
        self.ui = QUiLoader().load('updateCashier.ui')
        self.Cno = cno

        sql = "SELECT Cno, Cname, Csex, Cage, Cdeptno, Tno, Cceno from `cs2329.cashier` where Cno=%s" % cno
        [Cno, Cname, Csex, Cage, Cdeptno, Tno, Cceno] = jdbc.dbQueryOne(sql)
        self.ui.CnoEdit.setText(str(Cno))
        self.ui.CnameEdit.setText(str(Cname))
        if str(Csex) == '男':
            self.ui.rbtn_male.setChecked(True)
        else:
            self.ui.rbtn_female.setChecked(True)
        self.ui.CageEdit.setText(str(Cage))
        self.ui.CdeptnoEdit.setText(str(Cdeptno))
        self.ui.TnoEdit.setText(str(Tno))
        self.ui.CcenoEdit.setText(str(Cceno))
        # nno为主键，设置为只读
        self.ui.CnoEdit.setReadOnly(True)

        self.ui.btn_update.clicked.connect(self.updateInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def updateInfo(self):
        cno = self.ui.CnoEdit.text()
        cname = self.ui.CnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            csex = '男'
        else:
            csex = '女'
        cage = self.ui.CageEdit.text()
        cdeptno = self.ui.CdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        cceno = self.ui.CcenoEdit.text()
        sql = "update `cs2329.cashier` set Cname='%s', Csex='%s', Cage=%s, Cdeptno=%s, Tno=%s, Cceno='%s' where Cno = %s" % (cname, csex, cage, cdeptno, tno, cceno, cno)
        # 需要对patientTable数据进行更新
        if jdbc.dbUpdate(sql):
            mySignals.updateHR.emit(3, self.Cno)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_insertCashier:
    def __init__(self):
        self.ui = QUiLoader().load('insertCashier.ui')
        self.ui.btn_insert.clicked.connect(self.insertInfo)
        self.ui.btn_quit.clicked.connect(self.quitInfo)

    def insertInfo(self):
        cno = self.ui.CnoEdit.text()
        cname = self.ui.CnameEdit.text()
        if self.ui.rbtn_male.isChecked():
            csex = '男'
        else:
            csex = '女'
        cage = self.ui.CageEdit.text()
        cdeptno = self.ui.CdeptnoEdit.text()
        tno = self.ui.TnoEdit.text()
        cceno = self.ui.CcenoEdit.text()

        sql = "insert into `cs2329.cashier` (Cno, Cname, Csex, Cage, Cdeptno, Tno, Cceno) values (%s, '%s', '%s', %s, %s, %s, '%s')" % (
        cno, cname, csex, cage, cdeptno, tno, cceno)

        if jdbc.dbInsert(sql):
            mySignals.insertHR.emit(3)
            self.ui.close()

    def quitInfo(self):
        self.ui.close()


class Win_Recipe_Detail:
    def __init__(self, rmno):
        self.ui = QUiLoader().load('RecipeDetail.ui')
        self.RMno = rmno
        self.ui.btn_close.clicked.connect(self.close)

        sql = "SELECT RDno, RMno, R.Mno, Mname, RDprice, RDnumber, RDunit " \
              "from `cs2329.recipe_detail` R, `cs2329.medicine` M " \
              "where R.RMno = %s and R.Mno = M.Mno" % self.RMno
        [RDno, RMno, Mno, Mname, RDprice, RDnumber, RDunit] = jdbc.dbQueryOne(sql)
        self.ui.RDnoEdit.setText(str(RDno))
        self.ui.RMnoEdit.setText(str(RMno))
        self.ui.MnoEdit.setText(str(Mno))
        self.ui.MnameEdit.setText(str(Mname))
        self.ui.RDpriceEdit.setText(str(RDprice))
        self.ui.RDnumberEdit.setText(str(RDnumber))
        self.ui.RDunitEdit.setText(str(RDunit))

    def close(self):
        self.ui.close()


class Win_Fee:
    def __init__(self, rmno):
        self.ui = QUiLoader().load('Fee.ui')
        self.RMno = rmno
        self.ui.btn_close.clicked.connect(self.close)

        sql = "SELECT Fno, Fnumber, Fdate, DGno, F.Rno, F.Cno, Cname, F.Pno, Pname, Do.Dno, Dname, FRecipefee, Fdiscount, Fsum " \
              "from `cs2329.fee` F, `cs2329.cashier` C, `cs2329.doctor` Do, `cs2329.recipe_master` R, `cs2329.patient` P " \
              "where F.Rno = %s and F.Cno = C.Cno and F.Pno = P.Pno and R.RMno=%s and R.Dno = Do.Dno" % (self.RMno, self.RMno)
        [Fno, Fnumber, Fdate, DGno, Rno, Cno, Cname, Pno, Pname, Dno, Dname, FRecipefee, Fdiscount, Fsum] = jdbc.dbQueryOne(sql)
        self.ui.FnoEdit.setText(str(Fno))
        self.ui.FnumberEdit.setText(str(Fnumber))
        self.ui.FdateEdit.setText(str(Fdate))
        self.ui.DGnoEdit.setText(str(DGno))
        self.ui.RnoEdit.setText(str(Rno))
        self.ui.CnoEdit.setText(str(Cno))
        self.ui.CnameEdit.setText(str(Cname))
        self.ui.PnoEdit.setText(str(Pno))
        self.ui.PnameEdit.setText(str(Pname))
        self.ui.DnoEdit.setText(str(Dno))
        self.ui.DnameEdit.setText(str(Dname))
        self.ui.FRecipefeeEdit.setText(str(FRecipefee))
        self.ui.FdiscountEdit.setText(str(Fdiscount))
        self.ui.FsumEdit.setText(str(Fsum))

    def close(self):
        self.ui.close()


app = QApplication([])
jdbc = JDBC()
mySignals = MySignals()
ShareInfo.loginWin = Win_Login()
ShareInfo.loginWin.ui.show()
app.exec_()


