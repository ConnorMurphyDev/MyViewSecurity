import os.path
import sqlite3
from datetime import datetime



def localDatabaseConnect():


    if os.path.isfile("securityLog.db"):
        print("DB exist")

        #Connects to SQLite DB
        connection = sqlite3.connect("securityLog.db")
        cursor = connection.cursor()

        return cursor, connection
    else:
        print("DB does not exist, Creating SQLite DB")

        #Connects to SQLite DB
        connection = sqlite3.connect("securityLog.db")
        cursor = connection.cursor()

        #Creates log table
        cursor.execute("create table log (name text, time text, cameraName text)")
        return cursor, connection




def updateLocalDatabase(cursor, connection, name):

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
    print("date and time =", dt_string)


    cursor.execute("insert into log values(?,?,?)",(name,dt_string,"Webcam"))
    connection.commit()