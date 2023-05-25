import pymysql
from pymysql.constants import CLIENT

conn = pymysql.connect(host='124.71.219.185', user='root', password='uestc2022!',
                       database='cs2329.his', charset='utf8',
                       client_flag=CLIENT.MULTI_STATEMENTS)

cursor = conn.cursor()
# 创建管理员账户表
sql = """
create table `cs2329.rootUser` (No int unsigned NOT NULL AUTO_INCREMENT, USERNAME CHAR(20) not null , PASSWORD CHAR(20) not null, primary key (No));
insert into `cs2329.rootUser` (USERNAME, PASSWORD) values('root', '909090');
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

