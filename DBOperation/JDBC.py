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
          Pid varchar(20) NOT NULL UNIQUE COMMENT '身份证号',
          Pino varchar(20) NOT NULL COMMENT '社保号',
          Pmno varchar(20) NOT NULL COMMENT '医疗卡号',
          Psex varchar(2) NOT NULL COMMENT '性别',
          Pbd date NOT NULL COMMENT '生日',
          Padd varchar(100) NOT NULL COMMENT '地址',
          PRIMARY KEY (Pno)
        );

        CREATE TABLE `cs2329.patient_tel` (
          Ptno int unsigned NOT NULL AUTO_INCREMENT COMMENT '患者电话编号',
          Pno int unsigned DEFAULT NULL COMMENT '患者编号',
          Pteltype varchar(20) NOT NULL COMMENT '患者方式类型',
          Ptelcode varchar(20) NOT NULL COMMENT '联系号码',
          PRIMARY KEY (Ptno),
          FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno) 
          ON DELETE CASCADE
          ON UPDATE CASCADE
        );

        CREATE TABLE `cs2329.salary` (
          Sno int unsigned NOT NULL AUTO_INCREMENT COMMENT '工资编号',
          Slevel varchar(20) NOT NULL COMMENT '工资等级',
          Snumber decimal(10,2) unsigned NOT NULL COMMENT '工资数量',
          PRIMARY KEY (Sno)
        );

        CREATE TABLE `cs2329.title` (
          Tno int unsigned NOT NULL AUTO_INCREMENT COMMENT '职称编号',
          Sno int unsigned DEFAULT NULL COMMENT '工资类型',
          Ttype varchar(50) NOT NULL COMMENT '职称类型',
          Ttrade varchar(20) NOT NULL COMMENT '所属行业',
          PRIMARY KEY (Tno),
          FOREIGN KEY (Sno) REFERENCES `cs2329.salary` (Sno)
          ON DELETE CASCADE
          ON UPDATE CASCADE
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
          Ddeptno int unsigned DEFAULT NULL COMMENT '所属部门编号',
          Tno int unsigned DEFAULT NULL COMMENT '职称编号',
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
          Ndeptno int unsigned DEFAULT NULL COMMENT '所属部门编号',
          Tno int unsigned DEFAULT NULL COMMENT '职称编号',
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
          Cdeptno int unsigned DEFAULT NULL COMMENT '所属部门编号',
          Tno int unsigned DEFAULT NULL COMMENT '职称编号',
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
          Phdeptno int unsigned DEFAULT NULL COMMENT '所属部门编号',
          Tno int unsigned DEFAULT NULL COMMENT '职称编号',
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
          GMno int unsigned DEFAULT NULL COMMENT '所属主单编号',
          Mno int unsigned DEFAULT NULL COMMENT '药品编号',
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
          GSno int unsigned DEFAULT NULL COMMENT '从单编号',
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
          Pno int unsigned DEFAULT NULL COMMENT '患者编号',
          Dno int unsigned DEFAULT NULL COMMENT '医生编号',
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
          DeptNo int unsigned DEFAULT NULL COMMENT '部门编号',
          Dno int unsigned DEFAULT NULL COMMENT '医生编号',
          Pno int unsigned DEFAULT NULL COMMENT '患者编号',
          RMage int unsigned NOT NULL COMMENT '年龄',
          RMtime datetime NOT NULL COMMENT '处方时间',
          PRIMARY KEY (RMno),
          FOREIGN KEY (DeptNo) REFERENCES `cs2329.dept` (DeptNo),
          FOREIGN KEY (Dno) REFERENCES `cs2329.doctor` (Dno),
          FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno)
        );

        CREATE TABLE `cs2329.recipe_detail` (
          RDno int unsigned NOT NULL AUTO_INCREMENT COMMENT '处方药品清单编号',
          RMno int unsigned DEFAULT NULL COMMENT '所属处方编号',
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
          RFdept int unsigned DEFAULT NULL COMMENT '挂号科室',
          RFdoctor int unsigned DEFAULT NULL COMMENT '挂号医生',
          RFpatient int unsigned DEFAULT NULL COMMENT '挂号患者',
          RFcashier int unsigned DEFAULT NULL COMMENT '挂号收银员',
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
          DGno int unsigned DEFAULT NULL COMMENT '就诊编号',
          Rno int unsigned DEFAULT NULL COMMENT '处方编号',
          Cno int unsigned DEFAULT NULL COMMENT '收银员编号',
          Pno int unsigned DEFAULT NULL COMMENT '患者编号',
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

    def importDB(self):
        # 导入患者信息
        sqls = ["insert into `cs2329.patient` values(161, '刘景', '142201198702130061', '1201676', '6781121941', '男', '1987-2-13', '新华路光源街')",
                "insert into `cs2329.patient_tel` values(01, 161, '手机', '12988011007')",
                "insert into `cs2329.patient_tel` values(02, 161, '家庭电话', '12988011007')",
                "insert into `cs2329.patient_tel` values(03, 161, '单位电话', '12988011007')",
                "insert into `cs2329.patient` values(181, '陈禄', '142201196608190213', '1204001', '5461021938', '男', '1987-8-19', '城建路茂源巷')",
                "insert into `cs2329.patient_tel` values(04, 181, '手机', '12988011007')",
                "insert into `cs2329.patient_tel` values(05, 181, '家庭电话', '12988011007')",
                "insert into `cs2329.patient_tel` values(06, 181, '单位电话', '12988011007')",
                "insert into `cs2329.patient` values(201, '曾华', '142201197803110234', '0800920', '1231111932', '男', '1987-3-11', '新建路柳巷')",
                "insert into `cs2329.patient_tel` values(07, 201, '手机', '12988011007')",
                "insert into `cs2329.patient_tel` values(08, 201, '家庭电话', '12988011007')",
                "insert into `cs2329.patient_tel` values(09, 201, '单位电话', '12988011007')",
                "insert into `cs2329.patient` values(421, '傅伟相', '142201199109230221', '0700235', '4901021947', '男', '1987-9-23', '高新区西源大道')",
                "insert into `cs2329.patient_tel` values(10, 421, '手机', '12988011007')",
                "insert into `cs2329.patient_tel` values(11, 421, '家庭电话', '12988011007')",
                "insert into `cs2329.patient_tel` values(12, 421, '单位电话', '12988011007')",
                "insert into `cs2329.patient` values(481, '张珍', '142201199206200321', '1200432', '3451121953', '女', '1987-6-20', '西湖区南街')",
                "insert into `cs2329.patient_tel` values(13, 481, '手机', '12988011007')",
                "insert into `cs2329.patient_tel` values(14, 481, '家庭电话', '12988011007')",
                "insert into `cs2329.patient_tel` values(15, 481, '单位电话', '12988011007')",
                "insert into `cs2329.patient` values(501, '李秀', '142201198803300432', '0692015', '3341111936', '女', '1987-3-30', '泰山大道北路')",
                "insert into `cs2329.patient_tel` values(16, 501, '手机', '12988011007')",
                "insert into `cs2329.patient_tel` values(17, 501, '家庭电话', '12988011007')",
                "insert into `cs2329.patient_tel` values(18, 501, '单位电话', '12988011007')",
                ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入工资信息
        sqls = [
            "insert into `cs2329.salary` values(03, '高级', 4000)",
            "insert into `cs2329.salary` values(05, '中级', 3000)",
            "insert into `cs2329.salary` values(01, '高级', 5000)",
            "insert into `cs2329.salary` values(06, '初级', 2500)"
        ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入职称信息
        sqls = [
            "insert into `cs2329.title` values(102, 05,'医师', '医疗')",
            "insert into `cs2329.title` values(104, 03,'副主任医师', '医疗')",
            "insert into `cs2329.title` values(103, 01,'主治医师', '医疗')",
            "insert into `cs2329.title` values(105, 01,'主任医师', '医疗')",
            "insert into `cs2329.title` values(223, 06,'初级护士', '护理')",
            "insert into `cs2329.title` values(235, 03,'主任护士', '护理')",
            "insert into `cs2329.title` values(236, 06,'收银员', '收银')",
            "insert into `cs2329.title` values(237, 06,'药剂师', '药剂')"
        ]
        for sql in sqls:
            self.cursor.execute(sql)
            self.conn.commit()

        # 导入组织机构信息，由于外键约束，这里只能先将Manager置空
        sqls = [
            "insert into `cs2329.dept` values(01, '人民医院', null, null)",
            "insert into `cs2329.dept` values(10, '门诊部', 01, null)",
            "insert into `cs2329.dept` values(101, '消化内科', 10, null)",
            "insert into `cs2329.dept` values(104, '急诊内科', 10, null)",
            "insert into `cs2329.dept` values(103, '门内三诊室', 10, null)",
            "insert into `cs2329.dept` values(20, '社区医疗部', 01, null)",
            "insert into `cs2329.dept` values(105, '家庭病床病区', 20, null)",
        ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入医生信息
        sqls = [
            "insert into `cs2329.doctor` values(140, '郝亦柯', '男', 28, 101, 102, '140', '是', 20)",
            "insert into `cs2329.doctor` values(21, '刘伟', '男', 43, 104, 103, '21', '是', 20)",
            "insert into `cs2329.doctor` values(368, '罗晓', '女', 27, 103, 104, '368', '是', 20)",
            "insert into `cs2329.doctor` values(73, '邓英超', '女', 43, 105, 105, '73', '否', 10)",
            "insert into `cs2329.doctor` values(82, '杨勋', '男', 25, 104, 103, '82', '否', 10)",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 更新组织机构的Manager信息
        sqls = [
            "update `cs2329.dept` set Manager = 140 where DeptNo = 101",
            "update `cs2329.dept` set Manager = 21 where DeptNo = 104",
            "update `cs2329.dept` set Manager = 368 where DeptNo = 103",
            "update `cs2329.dept` set Manager = 73 where DeptNo = 20",
            "update `cs2329.dept` set Manager = 82 where DeptNo = 105",
        ]
        for sql in sqls:
            if not self.dbUpdate(sql):
                return False

        # 导入护士信息
        sqls = [
            "insert into `cs2329.nurse` values(01, '王亦柯', '男', 28, 101, 223, '140', '20')",
            "insert into `cs2329.nurse` values(02, '周伟', '男', 43, 104, 235, '21', '20')",
            "insert into `cs2329.nurse` values(03, '刘晓', '女', 27, 103, 235, '368', '20')",
            "insert into `cs2329.nurse` values(04, '邓超', '女', 43, 105, 223, '73', '10')",
            "insert into `cs2329.nurse` values(05, '钱勋', '男', 25, 104, 235, '82', '10')",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入收银员信息
        sqls = [
            "insert into `cs2329.cashier` values(01, '张三', '男', 28, 101, 236, '140')",
            "insert into `cs2329.cashier` values(02, '李伟', '男', 43, 104, 236, '21')",
            "insert into `cs2329.cashier` values(08, '韩晓', '女', 27, 103, 236, '368')",
            "insert into `cs2329.cashier` values(09, '周超', '女', 43, 105, 236, '73')",
            "insert into `cs2329.cashier` values(05, '李勋', '男', 25, 104, 236, '82')",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入药剂师信息
        sqls = [
            "insert into `cs2329.pharmacist` values(01, '王柯', '男', 28, 101, 237, '140', '20')",
            "insert into `cs2329.pharmacist` values(02, '李伟', '男', 43, 104, 237, '21', '20')",
            "insert into `cs2329.pharmacist` values(03, '孙晓', '女', 27, 103, 237, '368', '20')",
            "insert into `cs2329.pharmacist` values(04, '李英', '女', 43, 105, 237, '73', '10')",
            "insert into `cs2329.pharmacist` values(05, '赵勋', '男', 25, 104, 237, '82', '10')",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入入库主单信息
        sqls = [
            "insert into `cs2329.godown_entry` values(1, '2016-1-2 13:00:12', '抗生素类药品')",
            "insert into `cs2329.godown_entry` values(12, '2016-11-24 18:00:00', '心脑血管用药')",
            "insert into `cs2329.godown_entry` values(31, '2017-1-14 9:02:01', '消化系统用药')",
            "insert into `cs2329.godown_entry` values(34, '2017-3-20 12:19:10', '呼吸系统用药')",
            "insert into `cs2329.godown_entry` values(25, '2016-1-3 14:00:00', '泌尿系统用药')",
            "insert into `cs2329.godown_entry` values(11, '2016-11-20 18:00:00', '血液系统用药')",
            "insert into `cs2329.godown_entry` values(3, '2016-1-10 9:10:22', '抗风湿类药品')",
            "insert into `cs2329.godown_entry` values(9, '2016-4-27 13:20:00', '注射剂类药品')",
            "insert into `cs2329.godown_entry` values(14, '2016-12-20 17:00:31', '激素类药品')",
            "insert into `cs2329.godown_entry` values(4, '2016-1-20 20:10:02', '皮肤科用药')",
            "insert into `cs2329.godown_entry` values(6, '2016-4-27 13:20:00', '妇科用药')",
            "insert into `cs2329.godown_entry` values(17, '2016-5-10 18:30:05', '抗肿瘤用药')",
            "insert into `cs2329.godown_entry` values(13, '2016-12-01 12:15:00', '抗精神病药品')",
            "insert into `cs2329.godown_entry` values(8, '2016-6-06 15:50:20', '清热解毒药品')",
            "insert into `cs2329.godown_entry` values(33, '2017-2-24 8:02:52', '维生素、矿物质药品')",
            "insert into `cs2329.godown_entry` values(32, '2017-1-19 7:22:00', '糖尿病用药')"
        ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入入库从单信息，由于外键约束，这里先将Mno置空
        sqls = [
            "insert into `cs2329.godown_slave` values(02, 17, null, 23, '箱', '232342345', 3000, '2019-12-30')",
            "insert into `cs2329.godown_slave` values(12, 1, null, 50, '箱', '345465675', 2560, '2020-12-30')",
            "insert into `cs2329.godown_slave` values(34, 12, null, 100, '盒', '678786994', 50300, '2022-3-10')",
            "insert into `cs2329.godown_slave` values(55, 25, null, 85, '盒', '534525342', 1450, '2022-6-20')"
        ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入药品信息
        sqls = [
            "insert into `cs2329.medicine` values(314172, 34, '卡托利普片', 0.037, '片', '西药')",
            "insert into `cs2329.medicine` values(314418, 02, '卡托利普片', 11.5, '瓶', '西药')",
            "insert into `cs2329.medicine` values(314941, 12, '卡托利普片', 27.1, '盒', '西药')",
            "insert into `cs2329.medicine` values(315189, 12, '卡托利普片', 26.9, '盒', '西药')",
            "insert into `cs2329.medicine` values(315501, 55, '卡托利普片', 21, '盒', '西药')",
            "insert into `cs2329.medicine` values(315722, 34, '卡托利普片', 26.9, '盒', '西药')",
            "insert into `cs2329.medicine` values(315805, 34, '卡托利普片', 0.1267, '粒', '西药')",
            "insert into `cs2329.medicine` values(315977, 02, '卡托利普片', 26.5, '盒', '西药')",
            "insert into `cs2329.medicine` values(316792, 12, '卡托利普片', 2.3, '粒', '西药')",
            "insert into `cs2329.medicine` values(316910, 55, '卡托利普片', 46, '支', '西药')",
            "insert into `cs2329.medicine` values(317660, 34, '卡托利普片', 25.5, '盒', '中成药')"
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 更新入库从单Mno信息
        sqls = [
            "update `cs2329.godown_slave` set Mno = 314941 where GSno = 02",
            "update `cs2329.godown_slave` set Mno = 315189 where GSno = 12",
            "update `cs2329.godown_slave` set Mno = 314172 where GSno = 34",
            "update `cs2329.godown_slave` set Mno = 315501 where GSno = 55",

        ]
        for sql in sqls:
            if not self.dbUpdate(sql):
                return False

        # 导入就诊信息
        sqls = [
            "insert into `cs2329.diagnosis` values(1645, 481, 140, '呼吸道感染', '伤风感冒', '2007-7-21 01:12:01', 3)",
            "insert into `cs2329.diagnosis` values(2170, 201, 21, '皮肤和软组织感染', '细菌感染', '2007-7-22 10:10:03', 5)",
            "insert into `cs2329.diagnosis` values(3265, 161, 82, '胃溃疡', '螺杆菌感染', '2007-7-23 10:59:42', 5)",
            "insert into `cs2329.diagnosis` values(3308, 181, 82, '消化不良', '胃病', '2007-7-23 11:11:34', 5)",
            "insert into `cs2329.diagnosis` values(3523, 501, 73, '心力衰竭', '高血压', '2007-7-23 02:01:05', 7)",
            "insert into `cs2329.diagnosis` values(7816, 421, 368, '肾盂结石', '肾结石', '2008-1-8 05:17:03', 3)",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入处方信息
        sqls = [
            "insert into `cs2329.recipe_master` values(1282317, 103, 140, 181, 12, '20016-7-21 01:12:01')",
            "insert into `cs2329.recipe_master` values(1282872, 101, 368, 161, 50, '2007-7-22 10:10:03')",
            "insert into `cs2329.recipe_master` values(1283998, 20, 73, 481, 23, '2007-7-23 10:59:42')",
            "insert into `cs2329.recipe_master` values(1284041, 101, 368, 501, 48, '2007-7-23 11:11:34')",
            "insert into `cs2329.recipe_master` values(1284256, 103, 21, 201, 36, '2007-7-23 02:01:05')",
            "insert into `cs2329.recipe_master` values(1458878, 104, 82, 421, 30, '2008-1-8 05:17:03')",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入处方药品清单信息
        sqls = [
            "insert into `cs2329.recipe_detail` values(16, 1282872, 314941, 200, 3, '盒')",
            "insert into `cs2329.recipe_detail` values(32, 1458878, 315189, 360, 4, '盒')",
            "insert into `cs2329.recipe_detail` values(47, 1284041, 315977, 14, 1, '片')",
            "insert into `cs2329.recipe_detail` values(89, 1282317, 316910, 2.5, 10, '粒')",
            "insert into `cs2329.recipe_detail` values(12, 1283998, 317660, 14, 3, '盒')",
            "insert into `cs2329.recipe_detail` values(13, 1284256, 315501, 15, 2, '片')",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入挂号单信息
        sqls = [
            "insert into `cs2329.register_form` values(13, 20, 73, 481, 01, '2016-7-11 06:12:09', '2016-7-11 08:00:00', 5, null)",
            "insert into `cs2329.register_form` values(56, 101, 368, 161, 08, '2016-7-28 09:20:19', '2016-7-28 09:30:00', 7, null)",
            "insert into `cs2329.register_form` values(71, 103, 140, 181, 09, '2017-1-10 16:09:02', '2017-1-10 17:30:00', 7, null)",
            "insert into `cs2329.register_form` values(89, 104, 82, 421, 02, '2017-3-16 19:18:10', '2017-3-16 19:20:10', 5, null)",
            ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        # 导入费用信息
        sqls = [
            "insert into `cs2329.fee` values(1281645, '02995606', '2016-7-21 01:12:01', 1645, 1282317, 09, 181, 200, 0, 200)",
            "insert into `cs2329.fee` values(1282170, '02994356', '2016-7-22 10:10:03', 7816, 1282872, 01, 481, 189, 37.8, 151.2)",
            "insert into `cs2329.fee` values(1283265, '02996768', '2016-7-23 10:59:42', 2170, 1283998, 02, 501, 560, 112, 448)",
            "insert into `cs2329.fee` values(1283308, '02995687', '2016-7-23 11:11:34', 3308, 1284041, 05, 201, 17, 3.4, 13.6)",
            "insert into `cs2329.fee` values(1283523, '02997432', '2016-7-23 02:01:05', 3523, 1284256, 08, 481, 13, 0, 13)",
            "insert into `cs2329.fee` values(1457816, '02990101', '2017-1-8 05:17:03', 3265, 1458878, 09, 201, 111, 0, 111)",
        ]
        for sql in sqls:
            if not self.dbInsert(sql):
                return False

        return True
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

    def dbQueryHeaders(self, sql):
        try:
            self.cursor.execute(sql)
            description = self.cursor.description
            headers = [desc[0] for desc in description]
            return headers
        except:
            print("查询失败")
            return None

    def dbQueryAll(self, sql):
        # try:
        self.cursor.execute(sql)
        queryResults = self.cursor.fetchall()
        results = [list(result) for result in queryResults]
        return results
        # except:
        #     print("查询失败")
        #     return None

    def dbQueryOne(self, sql):
        try:
            self.cursor.execute(sql)
            queryResult = self.cursor.fetchone()
            result = list(queryResult)
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


