import pymysql
from pymysql.constants import CLIENT

conn = pymysql.connect(host='124.71.219.185', user='root', password='uestc2022!',
                       database='cs2329.his', charset='utf8',
                       client_flag=CLIENT.MULTI_STATEMENTS)

cursor = conn.cursor()
# 创建管理员账户表
sql = """
create table `cs2329.rootUser` (USERNAME CHAR(20) not null , PASSWORD CHAR(20) not null, primary key (USERNAME));
insert into `cs2329.rootUser` values('root', '909090');
create table `cs2329.patientUser` (Pno int unsigned DEFAULT NULL, USERNAME CHAR(20) not null, PASSWORD CHAR(20) not null, primary key (USERNAME), FOREIGN KEY (Pno) REFERENCES `cs2329.patient` (Pno) );
insert into `cs2329.patientUser` values(161, 'LiuJing', '123');
insert into `cs2329.patientUser` values(421, 'FuWeixiang', '123');
create table `cs2329.doctorUser` (Dno int unsigned DEFAULT NULL, USERNAME CHAR(20) not null, PASSWORD CHAR(20) not null, primary key (USERNAME), FOREIGN KEY (Dno) REFERENCES `cs2329.doctor` (Dno));
insert into `cs2329.doctorUser` values(82, 'YangXun', '123');
insert into `cs2329.doctorUser` values(368, 'LuoXiao', '123');
"""

try:
    cursor.execute(sql)
    conn.commit()
    print('插入成功')
except:
    conn.rollback()
    print('插入失败')
cursor.close()
conn.close()

