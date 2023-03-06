#Currently kept for notes and reference on SQLite syntax
#Will be removed


import sqlite3

connection = sqlite3.connect("securityLog.db")
cursor = connection.cursor()

cursor.execute("create table log (name text, time text, cameraName text)")



cursor.execute("insert into log values('Connor','4pm','webcam')")

connection.commit()



#print database rows
for row in cursor.execute("select * from log"):
    print(row)








connection.close()






"""
#how to execute sql commands
cursor.execute("insert into log values (?,?,?)")



#print database rows
for row in cursor.execute("select * from log"):
    print(row)


#How to create a table
# cursor.execute("create table log (name text, time text, cameraName text)")


#open connection
connection = sqlite3.connect("securityLog.db")
cursor = connection.cursor()


#saves changes made. if closed without doing this all changes will be rolled back.
connection.commit()




#close connection
connection.close()
"""