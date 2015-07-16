import MySQLdb
 
try:
    conn=MySQLdb.connect(host='203.195.179.183',user='cdb_outerroot',passwd='24203cjy',port=8295,db='test',charset='utf8')
    cur=conn.cursor()
     
    cur.execute('create database if not exists test')
    conn.select_db('test')
      
    value=[1,'hi rollen']
    cur.execute('insert into book values(%s,%s)',value)
     
    values=[]
    for i in range(20):
        values.append((i,'hi rollen'+str(i)))
         
    cur.executemany('insert into book values(%s,%s)',values)
 
    cur.execute('update book set link="rollen" where title=3')
 
    conn.commit()
    cur.close()
    conn.close()
 
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])