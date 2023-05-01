import pymysql
from pymysql.constants import CLIENT

conn = pymysql.connect(host='124.71.219.185', user='root', password='uestc2022!',
                       database='cs2329.his', charset='utf8',
                       client_flag=CLIENT.MULTI_STATEMENTS)

cursor = conn.cursor()
# 创建管理员账户表
sql = """
create table ROOT(USERNAME CHAR(20) not null , PASSWORD CHAR(20) not null, primary key (USERNAME));
insert into root values('root', '909090')
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

