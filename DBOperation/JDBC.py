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
              `Pno` int unsigned NOT NULL AUTO_INCREMENT,
              `Pname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '患者姓名',
              `Pid` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '身份证号',
              `Pino` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '社保号',
              `Pmno` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '医保卡号',
              `Psex` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
              `Pbd` date DEFAULT NULL COMMENT '生日',
              `Padd` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '地址',
              PRIMARY KEY (`Pno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='患者信息';
    
            CREATE TABLE `cs2329.patient_tel` (
              `Ptno` int unsigned NOT NULL AUTO_INCREMENT,
              `Pno` int unsigned NOT NULL COMMENT '患者编号',
              `Pteltype` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '患者电话类型',
              `Ptelcode` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '患者电话号码',
              PRIMARY KEY (`Ptno`),
              KEY `Patient_pt` (`Pno`),
              CONSTRAINT `Patient_pt` FOREIGN KEY (`Pno`) REFERENCES `cs2329.patient` (`Pno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.dept` (
              `DeptNo` int unsigned NOT NULL AUTO_INCREMENT,
              `DeptName` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '部门名称',
              `ParentDeptNo` int unsigned DEFAULT NULL COMMENT '父级部门编号',
              `Manager` int unsigned DEFAULT NULL COMMENT '部门经理编号',
              PRIMARY KEY (`DeptNo`),
              KEY `Parent_dept` (`ParentDeptNo`),
              KEY `Leader_dept` (`Manager`),
              CONSTRAINT `Leader_dept` FOREIGN KEY (`Manager`) REFERENCES `cs2329.doctor` (`Dno`),
              CONSTRAINT `Parent_dept` FOREIGN KEY (`ParentDeptNo`) REFERENCES `cs2329.dept` (`DeptNo`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.doctor` (
              `Dno` int unsigned NOT NULL AUTO_INCREMENT,
              `Dname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '医生姓名',
              `Dsex` varchar(2) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '医生性别',
              `Dage` int unsigned DEFAULT NULL COMMENT '医生年龄',
              `DeptNo` int unsigned DEFAULT NULL COMMENT '所属部门',
              `Tno` int unsigned DEFAULT NULL COMMENT '职称编号',
              `Dregno` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '医生注册号码',
              `Dissp` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否专家',
              `Dfee` decimal(10,2) DEFAULT NULL COMMENT '挂号费用',
              PRIMARY KEY (`Dno`),
              KEY `Dept_dt` (`DeptNo`),
              KEY `Title_dt` (`Tno`),
              CONSTRAINT `Dept_dt` FOREIGN KEY (`DeptNo`) REFERENCES `cs2329.dept` (`DeptNo`),
              CONSTRAINT `Title_dt` FOREIGN KEY (`Tno`) REFERENCES `cs2329.title` (`Tno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            
            CREATE TABLE `cs2329.nurse` (
              `Nno` int unsigned NOT NULL AUTO_INCREMENT,
              `Nname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '护士姓名',
              `Nsex` varchar(2) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '护士性别',
              `Nage` int unsigned DEFAULT NULL COMMENT '护士年龄',
              `DeptNo` int unsigned DEFAULT NULL COMMENT '所属部门',
              `Tno` int unsigned DEFAULT NULL COMMENT '职称编号',
              `Nceno` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '护士证书编号',
              `Nlevel` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '护士级别',
              PRIMARY KEY (`Nno`),
              KEY `Dept_nu` (`DeptNo`),
              KEY `Title_nu` (`Tno`),
              CONSTRAINT `Dept_nu` FOREIGN KEY (`DeptNo`) REFERENCES `cs2329.dept` (`DeptNo`),
              CONSTRAINT `Title_nu` FOREIGN KEY (`Tno`) REFERENCES `cs2329.title` (`Tno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.cashier` (
              `Cno` int unsigned NOT NULL AUTO_INCREMENT,
              `Cname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '收银员姓名',
              `Csex` varchar(2) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '收银员性别',
              `Cage` int unsigned DEFAULT NULL COMMENT '收银员年龄',
              `DeptNo` int unsigned DEFAULT NULL COMMENT '所属部门',
              `Tno` int unsigned DEFAULT NULL COMMENT '职称编号',
              `Cceno` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '收银员证书编号',
              PRIMARY KEY (`Cno`),
              KEY `Dept_ca` (`DeptNo`),
              KEY `Title_ca` (`Tno`),
              CONSTRAINT `Dept_ca` FOREIGN KEY (`DeptNo`) REFERENCES `cs2329.dept` (`DeptNo`),
              CONSTRAINT `Title_ca` FOREIGN KEY (`Tno`) REFERENCES `cs2329.title` (`Tno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.pharmacist` (
              `Phno` int unsigned NOT NULL AUTO_INCREMENT,
              `Phname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '药剂师姓名',
              `Phsex` varchar(2) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '药剂师性别',
              `Phage` int unsigned DEFAULT NULL COMMENT '药剂师年龄',
              `DeptNo` int unsigned DEFAULT NULL COMMENT '所属部门',
              `Tno` int unsigned DEFAULT NULL COMMENT '职称编号',
              `Phceno` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '药剂师证书编号',
              `Phtype` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '药剂师类型',
              PRIMARY KEY (`Phno`),
              KEY `Dept_ph` (`DeptNo`),
              KEY `Title_ph` (`Tno`),
              CONSTRAINT `Dept_ph` FOREIGN KEY (`DeptNo`) REFERENCES `cs2329.dept` (`DeptNo`),
              CONSTRAINT `Title_ph` FOREIGN KEY (`Tno`) REFERENCES `cs2329.title` (`Tno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
    
            CREATE TABLE `cs2329.title` (
              `Tno` int unsigned NOT NULL AUTO_INCREMENT,
              `Sno` int unsigned DEFAULT NULL COMMENT '工资类型编号',
              `Ttype` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '职称类型',
              `Ttrade` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '所属行业',
              PRIMARY KEY (`Tno`),
              KEY `Salary_title` (`Sno`),
              CONSTRAINT `Salary_title` FOREIGN KEY (`Sno`) REFERENCES `cs2329.salary` (`Sno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            
            CREATE TABLE `cs2329.salary` (
              `Sno` int unsigned NOT NULL AUTO_INCREMENT,
              `Slevel` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '工资等级',
              `Snumber` decimal(10,2) unsigned DEFAULT NULL COMMENT '工资数量',
              PRIMARY KEY (`Sno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.godown_entry` (
              `GMno` int unsigned NOT NULL AUTO_INCREMENT,
              `GMdata` datetime DEFAULT NULL COMMENT '入库时间',
              `GMname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '主单名称',
              PRIMARY KEY (`GMno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.godown_slave` (
              `GSno` int unsigned NOT NULL AUTO_INCREMENT,
              `GMno` int unsigned DEFAULT NULL COMMENT '所属主单编号',
              `Mno` int unsigned DEFAULT NULL COMMENT '药品编号',
              `GSnumber` decimal(10,2) DEFAULT NULL COMMENT '数量',
              `GSunit` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数量单位',
              `GSbatch` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '批次号',
              `GSprice` decimal(10,2) unsigned DEFAULT NULL COMMENT '价格',
              `GSexpdate` date DEFAULT NULL COMMENT '有效期',
              PRIMARY KEY (`GSno`),
              KEY `Master_gs` (`GMno`),
              KEY `Medicine_gs` (`Mno`),
              CONSTRAINT `Master_gs` FOREIGN KEY (`GMno`) REFERENCES `cs2329.godown_entry` (`GMno`),
              CONSTRAINT `Medicine_gs` FOREIGN KEY (`Mno`) REFERENCES `cs2329.medicine` (`Mno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            
            CREATE TABLE `cs2329.medicine` (
              `Mno` int unsigned NOT NULL AUTO_INCREMENT,
              `GSno` int unsigned DEFAULT NULL COMMENT '从单编号',
              `Mname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '药品名称',
              `Mprice` decimal(10,2) DEFAULT NULL COMMENT '价格',
              `Munit` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '包装单位',
              `Mtype` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '药品类型',
              PRIMARY KEY (`Mno`),
              KEY `Slave_md` (`GSno`),
              CONSTRAINT `Slave_md` FOREIGN KEY (`GSno`) REFERENCES `cs2329.godown_slave` (`GSno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            
            CREATE TABLE `cs2329.diagnosis` (
              `DGno` int unsigned NOT NULL AUTO_INCREMENT,
              `Pno` int unsigned NOT NULL COMMENT '患者编号',
              `Dno` int unsigned NOT NULL COMMENT '医生编号',
              `Symptom` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '症状描述',
              `Diagnosis` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '诊断结论',
              `DGtime` datetime DEFAULT NULL COMMENT '诊断时间',
              `Rfee` decimal(10,2) DEFAULT NULL COMMENT '就诊费用',
              PRIMARY KEY (`DGno`),
              KEY `Doctor_dg` (`Dno`),
              KEY `Patient_dg` (`Pno`),
              CONSTRAINT `Doctor_dg` FOREIGN KEY (`Dno`) REFERENCES `cs2329.doctor` (`Dno`),
              CONSTRAINT `Patient_dg` FOREIGN KEY (`Pno`) REFERENCES `cs2329.patient` (`Pno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.recipe_master` (
              `RMno` int unsigned NOT NULL AUTO_INCREMENT,
              `DeptNo` int unsigned DEFAULT NULL COMMENT '部门编号',
              `Dno` int unsigned NOT NULL COMMENT '医生编号',
              `Pno` int unsigned NOT NULL COMMENT '患者编号',
              `RMage` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '年龄',
              `RMtime` datetime DEFAULT NULL COMMENT '处方时间',
              PRIMARY KEY (`RMno`),
              KEY `Dept_rm` (`DeptNo`),
              KEY `Doctor_rm` (`Dno`),
              KEY `Patient_rm` (`Pno`),
              CONSTRAINT `Dept_rm` FOREIGN KEY (`DeptNo`) REFERENCES `cs2329.dept` (`DeptNo`),
              CONSTRAINT `Doctor_rm` FOREIGN KEY (`Dno`) REFERENCES `cs2329.doctor` (`Dno`),
              CONSTRAINT `Patient_rm` FOREIGN KEY (`Pno`) REFERENCES `cs2329.patient` (`Pno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.recipe_detail` (
              `RDno` int unsigned NOT NULL AUTO_INCREMENT,
              `RMno` int unsigned DEFAULT NULL COMMENT '处方编号',
              `Mno` int unsigned DEFAULT NULL COMMENT '药品编号',
              `RDprice` decimal(10,2) DEFAULT NULL COMMENT '价格',
              `RDnumber` decimal(10,2) DEFAULT NULL COMMENT '数量',
              `RDunit` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '数量单位',
              PRIMARY KEY (`RDno`),
              KEY `Recipe_rd` (`RMno`),
              KEY `Medicine_rd` (`Mno`),
              CONSTRAINT `Medicine_rd` FOREIGN KEY (`Mno`) REFERENCES `cs2329.medicine` (`Mno`),
              CONSTRAINT `Recipe_rd` FOREIGN KEY (`RMno`) REFERENCES `cs2329.recipe_master` (`RMno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
            CREATE TABLE `cs2329.register_form` (
              `RFno` int unsigned NOT NULL AUTO_INCREMENT,
              `RFdept` int unsigned DEFAULT NULL COMMENT '挂号科室',
              `RFdoctor` int unsigned DEFAULT NULL COMMENT '挂号医生',
              `RFpatient` int unsigned DEFAULT NULL COMMENT '挂号患者',
              `RFcashier` int unsigned DEFAULT NULL COMMENT '挂号收银员',
              `RFtime` datetime DEFAULT NULL COMMENT '挂号时间',
              `RFvisittime` datetime DEFAULT NULL COMMENT '预约就诊时间',
              `Rffee` decimal(10,2) DEFAULT NULL COMMENT '挂号费',
              `RFnotes` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
              PRIMARY KEY (`RFno`),
              KEY `Dept_rf` (`RFdept`),
              KEY `Patient_rf` (`RFpatient`),
              KEY `Doctor_rf` (`RFdoctor`),
              KEY `Cashier_rf` (`RFcashier`),
              CONSTRAINT `Cashier_rf` FOREIGN KEY (`RFcashier`) REFERENCES `cs2329.cashier` (`Cno`),
              CONSTRAINT `Dept_rf` FOREIGN KEY (`RFdept`) REFERENCES `cs2329.dept` (`DeptNo`),
              CONSTRAINT `Doctor_rf` FOREIGN KEY (`RFdoctor`) REFERENCES `cs2329.doctor` (`Dno`),
              CONSTRAINT `Patient_rf` FOREIGN KEY (`RFpatient`) REFERENCES `cs2329.patient` (`Pno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            
            CREATE TABLE `cs2329.fee` (
              `Fno` int unsigned NOT NULL AUTO_INCREMENT,
              `Fnumber` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '发票号码',
              `FDate` datetime NOT NULL COMMENT '日期',
              `DGno` int unsigned NOT NULL COMMENT '就诊编号',
              `Rno` int unsigned NOT NULL COMMENT '处方编号',
              `Cno` int unsigned DEFAULT NULL COMMENT '收银员编号',
              `Pno` int unsigned NOT NULL COMMENT '患者编号',
              `FRecipefee` decimal(10,2) NOT NULL COMMENT '应收金额',
              `Fdiscount` decimal(10,2) DEFAULT NULL COMMENT '减免折扣金额',
              `Fsum` decimal(10,2) NOT NULL COMMENT '实收金额',
              PRIMARY KEY (`Fno`),
              KEY `Diagnosis_fee` (`DGno`),
              KEY `Cashier_fee` (`Cno`),
              KEY `Patient_fee` (`Pno`),
              KEY `Recipe_fee` (`Rno`),
              CONSTRAINT `Cashier_fee` FOREIGN KEY (`Cno`) REFERENCES `cs2329.cashier` (`Cno`),
              CONSTRAINT `Diagnosis_fee` FOREIGN KEY (`DGno`) REFERENCES `cs2329.diagnosis` (`DGno`),
              CONSTRAINT `Patient_fee` FOREIGN KEY (`Pno`) REFERENCES `cs2329.patient` (`Pno`),
              CONSTRAINT `Recipe_fee` FOREIGN KEY (`Rno`) REFERENCES `cs2329.recipe_master` (`RMno`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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


