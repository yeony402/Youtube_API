import sqlite3

con = sqlite3.connect('youtube.db')
cursor = con.cursor()

table = '''create table if not exists ex(a varchar(100) not null, b varchar(100) not null, c varchar(100) not null)'''
cursor.execute(table)

a=1
b=8
c='eee'

vv = 'CREATE UNIQUE INDEX IF NOT EXISTS a_unique_index ON ex (a,b)'
cursor.execute(vv)

sql = "insert or ignore into ex(a,b,c) VALUES(?,?,?)"
cursor.execute(sql, (a,b,c))
con.commit()
