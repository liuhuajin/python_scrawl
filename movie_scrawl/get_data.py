#-*- encoding:utf-8 -*-
import db_op 

mysql_db = db_op.MySQLDBO()
cursor = mysql_db.db.cursor()
sql = 'select * from movie_info'
cursor.execute(sql)
data = cursor.fetchall()
f = open('a.txt', 'w')
for d in data:
    print '------'
    print d[0]
    print d[1]
    print d[2]
    print d[3]
    print d[4]
    f.write(d[0]+'\n')
    f.write(d[1]+'\n')
    f.write(d[2]+'\n')
    f.write(d[3]+'\n')
    f.write(d[4]+'\n')
f.close()
