import pymysql

#打开数据库连接
db = pymysql.connect(host='a.com',
                     port=3306
                     user='root',
                     password='******',
                     database='db1')

#使用cursor()方法创建一个游标对象
cursor = db.cursor()

def select_all():
    sql = 'select * from department'
    
    #使用execute()方法执行SQL
    cursor.execute(sql)
    
    #获取所有记录并打印
    results = cursor.fetchall()
    for i in results:
        print(i)
    print()

select_all()

sql = '''INSERT INTO db1.department (DEPT_NO,DEPT_NAME)
	    VALUES ('05','外语系');'''
try:
   #执行SQL语句
   cursor.execute(sql)
   #提交到数据库执行
   db.commit()
except:
   #发生错误时回滚
   db.rollback()

select_all()

#关闭数据库连接
db.close()