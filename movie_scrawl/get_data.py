import db_op 

mysql_db = db_op.MySQLDBO()
cursor = mysql_db.db.cursor()
sql = 'select * from movie_info'
cursor.execute(sql)
data = cursor.fetchall()
print data
for d in data:
    print d
