import pymysql
import re
from pymysql.constants import CLIENT


class JDBC:
    def __init__(self):
        self.conn = pymysql.connect(host='124.71.219.185', user='root', password='uestc2022!',
                                    database='cs2329.his', charset='utf8',
                                    client_flag=CLIENT.MULTI_STATEMENTS)
        self.cursor = self.conn.cursor()

    def createDB(self):
        try:
            sql = """
        CREATE TABLE `cs2329.patient` (
          Pno int unsigned NOT NULL AUTO_INCREMENT COMMENT '患者编号',
          Pname varchar(20) NOT NULL COMMENT '患者姓名',
          Pid varchar(20) NOT NULL COMMENT '身份证号',
          Pino varchar(20) NOT NULL COMMENT '社保号',
          Pmno varchar(20) NOT NULL COMMENT '医疗卡号',
          Psex varchar(2) NOT NULL COMMENT '性别',
          Pbd date NOT NULL COMMENT '生日',
          Padd varchar(100) NOT NULL COMMENT '地址',
          PRIMARY KEY (Pno)
        );

        CREATE TABLE `cs2329.patient_tel` (
          Ptno int unsigned NOT NULL AUTO_INCREMENT COMMENT '患者电话编号',
          Pno int unsigned NOT NULL COMMENT '患者编号',
          Pteltype varchar(20) NOT NULL COMMENT '患者方式类型',
          Ptelcode varchar(20) NOT NULL COMMENT '联系号码',
          PRIMARY KEY (Ptno),
          FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno)
        );

        CREATE TABLE `cs2329.salary` (
          Sno int unsigned NOT NULL AUTO_INCREMENT COMMENT '工资编号',
          Slevel varchar(20) NOT NULL COMMENT '工资等级',
          Snumber decimal(10,2) unsigned NOT NULL COMMENT '工资数量',
          PRIMARY KEY (Sno)
        );

        CREATE TABLE `cs2329.title` (
          Tno int unsigned NOT NULL AUTO_INCREMENT COMMENT '职称编号',
          Sno int unsigned NOT NULL COMMENT '工资类型',
          Ttype varchar(50) NOT NULL COMMENT '职称类型',
          Ttrade varchar(20) NOT NULL COMMENT '所属行业',
          PRIMARY KEY (Tno),
          FOREIGN KEY (Sno) REFERENCES `cs2329.salary` (Sno)
        );

        CREATE TABLE `cs2329.dept` (
          DeptNo int unsigned NOT NULL AUTO_INCREMENT COMMENT '部门编号',
          DeptName varchar(20) NOT NULL COMMENT '部门名称',
          ParentDeptNo int unsigned DEFAULT NULL COMMENT '父级部门编号',
          Manager int unsigned DEFAULT NULL COMMENT '部门经理编号',
          PRIMARY KEY (DeptNo),
          FOREIGN KEY (ParentDeptNo) REFERENCES `cs2329.dept` (DeptNo)
        );

        CREATE TABLE `cs2329.doctor` (
          Dno int unsigned NOT NULL AUTO_INCREMENT COMMENT '医生编号',
          Dname varchar(20) NOT NULL COMMENT '医生姓名',
          Dsex varchar(2) NOT NULL COMMENT '性别',
          Dage int unsigned NOT NULL COMMENT '年龄',
          Ddeptno int unsigned NOT NULL COMMENT '所属部门编号',
          Tno int unsigned NOT NULL COMMENT '职称编号',
          Dregno varchar(20) NOT NULL COMMENT '医生注册号码',
          Disex varchar(1) NOT NULL COMMENT '是否专家',
          Dfee decimal(10,2) NOT NULL COMMENT '挂号费用',
          PRIMARY KEY (Dno),
          FOREIGN KEY (Tno) REFERENCES `cs2329.title`(Tno)
        );

        ALTER TABLE `cs2329.dept`
            ADD CONSTRAINT Manager_Dno FOREIGN KEY (Manager) REFERENCES `cs2329.doctor` (Dno);

        ALTER TABLE `cs2329.doctor`
            ADD CONSTRAINT Ddeptno_DeptNo FOREIGN KEY (Ddeptno) REFERENCES `cs2329.dept` (DeptNo);

        CREATE TABLE `cs2329.nurse` (
          Nno int unsigned NOT NULL AUTO_INCREMENT COMMENT '护士编号',
          Nname varchar(20) NOT NULL COMMENT '护士姓名',
          Nsex varchar(2) NOT NULL COMMENT '性别',
          Nage int unsigned NOT NULL COMMENT '年龄',
          Ndeptno int unsigned NOT NULL COMMENT '所属部门编号',
          Tno int unsigned NOT NULL COMMENT '职称编号',
          Nceno varchar(20) NOT NULL COMMENT '护士证书编号',
          Nlevel varchar(20) NOT NULL COMMENT '护士级别',
          PRIMARY KEY (Nno),
          FOREIGN KEY (Ndeptno) REFERENCES `cs2329.dept` (DeptNo),
          FOREIGN KEY (Tno) REFERENCES `cs2329.title` (Tno)
        );

        CREATE TABLE `cs2329.cashier` (
          Cno int unsigned NOT NULL AUTO_INCREMENT COMMENT '收银员编号',
          Cname varchar(20) NOT NULL COMMENT '收银员姓名',
          Csex varchar(2) NOT NULL COMMENT '性别',
          Cage int unsigned NOT NULL COMMENT '年龄',
          Cdeptno int unsigned NOT NULL COMMENT '所属部门编号',
          Tno int unsigned NOT NULL COMMENT '职称编号',
          Cceno varchar(20) NOT NULL COMMENT '资格证书号码',
          PRIMARY KEY (Cno),
          FOREIGN KEY (Cdeptno) REFERENCES `cs2329.dept` (DeptNo),
          FOREIGN KEY (Tno) REFERENCES `cs2329.title` (Tno)
        );

        CREATE TABLE `cs2329.pharmacist` (
          Phno int unsigned NOT NULL AUTO_INCREMENT COMMENT '药剂师编号',
          Phname varchar(20) NOT NULL COMMENT '药剂师姓名',
          Phsex varchar(2) NOT NULL COMMENT '性别',
          Phage int unsigned NOT NULL COMMENT '年龄',
          Phdeptno int unsigned NOT NULL COMMENT '所属部门编号',
          Tno int unsigned NOT NULL COMMENT '职称编号',
          Phceno varchar(20) NOT NULL COMMENT '药剂师资格证书号',
          Phtype varchar(20) NOT NULL COMMENT '药剂师类型',
          PRIMARY KEY (Phno),
          FOREIGN KEY (Phdeptno) REFERENCES `cs2329.dept` (DeptNo),
          FOREIGN KEY (Tno) REFERENCES `cs2329.title` (Tno)
        );

        CREATE TABLE `cs2329.godown_entry`(
          GMno int unsigned NOT NULL AUTO_INCREMENT COMMENT '主单编号',
          GMdate datetime NOT NULL COMMENT '入库时间',
          GMname varchar(20) NOT NULL COMMENT '主单名称',
          PRIMARY KEY (GMno)
        );

        CREATE TABLE `cs2329.godown_slave` (
          GSno int unsigned NOT NULL AUTO_INCREMENT COMMENT '从单编号',
          GMno int unsigned NOT NULL COMMENT '所属主单编号',
          Mno int unsigned NOT NULL COMMENT '药品编号',
          GSnumber decimal(10,2) NOT NULL COMMENT '数量',
          GSunit varchar(20) NOT NULL COMMENT '数量单位',
          GSbatch varchar(20) NOT NULL COMMENT '批次号',
          GSprice decimal(10,2) unsigned NOT NULL COMMENT '价格',
          GSexpdate date NOT NULL COMMENT '有效期',
          PRIMARY KEY (GSno),
          FOREIGN KEY (GMno) REFERENCES `cs2329.godown_entry` (GMno)
        );

        CREATE TABLE `cs2329.medicine` (
          Mno int unsigned NOT NULL AUTO_INCREMENT,
          GSno int unsigned NOT NULL COMMENT '从单编号',
          Mname varchar(20) NOT NULL COMMENT '药品名称',
          Mprice decimal(10,2) NOT NULL COMMENT '价格',
          Munit varchar(10) NOT NULL COMMENT '包装单位',
          Mtype varchar(20) NOT NULL COMMENT '药品类型',
          PRIMARY KEY (Mno)
        );
        
        ALTER TABLE `cs2329.godown_slave`
            ADD CONSTRAINT Mno_Mno FOREIGN KEY (Mno) REFERENCES `cs2329.medicine` (Mno);
        
        ALTER TABLE `cs2329.medicine`
            ADD CONSTRAINT GSno_GSno FOREIGN KEY (GSno) REFERENCES `cs2329.godown_slave` (GSno);
        
        CREATE TABLE `cs2329.diagnosis` (
          DGno int unsigned NOT NULL AUTO_INCREMENT COMMENT '诊断编号',
          Pno int unsigned NOT NULL COMMENT '患者编号',
          Dno int unsigned NOT NULL COMMENT '医生编号',
          Symptom varchar(100) NOT NULL COMMENT '症状描述',
          Diagnosis varchar(50) NOT NULL COMMENT '诊断结论',
          DGtime datetime NOT NULL COMMENT '诊断时间',
          Rfee decimal(10,2) NOT NULL COMMENT '就诊费用',
          PRIMARY KEY (DGno),
          FOREIGN KEY (Dno) REFERENCES `cs2329.doctor` (Dno),
          FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno)
        );

        CREATE TABLE `cs2329.recipe_master` (
          RMno int unsigned NOT NULL AUTO_INCREMENT COMMENT '处方编号',
          DeptNo int unsigned NOT NULL COMMENT '部门编号',
          Dno int unsigned NOT NULL COMMENT '医生编号',
          Pno int unsigned NOT NULL COMMENT '患者编号',
          RMage int unsigned NOT NULL COMMENT '年龄',
          RMtime datetime NOT NULL COMMENT '处方时间',
          PRIMARY KEY (RMno),
          FOREIGN KEY (DeptNo) REFERENCES `cs2329.dept` (DeptNo),
          FOREIGN KEY (Dno) REFERENCES `cs2329.doctor` (Dno),
          FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno)
        );

        CREATE TABLE `cs2329.recipe_detail` (
          RDno int unsigned NOT NULL AUTO_INCREMENT COMMENT '处方药品清单编号',
          RMno int unsigned NOT NULL COMMENT '所属处方编号',
          Mno int unsigned NOT NULL COMMENT '药品编号',
          RDprice decimal(10,2) NOT NULL COMMENT '价格',
          RDnumber decimal(10,2) NOT NULL COMMENT '数量',
          RDunit varchar(10) NOT NULL COMMENT '数量单位',
          PRIMARY KEY (RDno),
          FOREIGN KEY (Mno) REFERENCES `cs2329.medicine` (Mno),
          FOREIGN KEY (RMno) REFERENCES `cs2329.recipe_master` (RMno)
        );

        CREATE TABLE `cs2329.register_form` (
          RFno int unsigned NOT NULL AUTO_INCREMENT COMMENT '挂号单编号',
          RFdept int unsigned NOT NULL COMMENT '挂号科室',
          RFdoctor int unsigned NOT NULL COMMENT '挂号医生',
          RFpatient int unsigned NOT NULL COMMENT '挂号患者',
          RFcashier int unsigned NOT NULL COMMENT '挂号收银员',
          RFtime datetime NOT NULL COMMENT '挂号时间',
          RFvisittime datetime NOT NULL COMMENT '预约就诊时间',
          RFfee decimal(10,2) NOT NULL COMMENT '挂号费',
          RFnotes varchar(100) DEFAULT NULL COMMENT '备注',
          PRIMARY KEY (RFno),
          FOREIGN KEY (RFcashier) REFERENCES `cs2329.cashier` (Cno),
          FOREIGN KEY (RFdept) REFERENCES `cs2329.dept` (DeptNo),
          FOREIGN KEY (RFdoctor) REFERENCES `cs2329.doctor` (Dno),
          FOREIGN KEY (RFpatient) REFERENCES `cs2329.patient` (Pno)
        );

        CREATE TABLE `cs2329.fee` (
          Fno int unsigned NOT NULL AUTO_INCREMENT COMMENT '发票单编号',
          Fnumber varchar(20) NOT NULL COMMENT '发票号码',
          FDate datetime NOT NULL COMMENT '日期',
          DGno int unsigned NOT NULL COMMENT '就诊编号',
          Rno int unsigned NOT NULL COMMENT '处方编号',
          Cno int unsigned NOT NULL COMMENT '收银员编号',
          Pno int unsigned NOT NULL COMMENT '患者编号',
          FRecipefee decimal(10,2) NOT NULL COMMENT '应收金额',
          Fdiscount decimal(10,2) NOT NULL COMMENT '减免折扣金额',
          Fsum decimal(10,2) NOT NULL COMMENT '实收金额',
          PRIMARY KEY (Fno),
          FOREIGN KEY (Cno) REFERENCES `cs2329.cashier` (Cno),
          FOREIGN KEY (DGno) REFERENCES `cs2329.diagnosis` (DGno),
          FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno),
          FOREIGN KEY (Rno) REFERENCES `cs2329.recipe_master` (RMno)
        );
        """
            self.cursor.execute(sql)
            return True
        except:
            # print('创建表失败')
            return False

    # 判断表是否存在
    def table_exists(self, table_name):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0  # 不存在返回0

    def dbInsert(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            print("插入失败")
            self.conn.rollback()
            return False

    def dbQueryAll(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results

        except:
            print("查询失败")
            return None

    def dbQueryOne(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result

        except:
            print("查询失败")
            return None

    def dbUpdate(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def dbDelete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def dbClose(self):
        self.cursor.close()
        self.conn.close()


