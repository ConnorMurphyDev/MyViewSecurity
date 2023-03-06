import os.path
import sqlite3
from datetime import datetime

import time

import cv2

last_checked = {}


def localDatabaseConnect():

    if os.path.isfile("securityLog.db"):
        print("DB exist")

        # Connects to SQLite DB
        connection = sqlite3.connect("securityLog.db")
        cursor = connection.cursor()

        return cursor, connection
    else:
        print("DB does not exist, Creating SQLite DB")

        # Connects to SQLite DB
        connection = sqlite3.connect("securityLog.db")
        cursor = connection.cursor()

        # Creates log table
        cursor.execute(
            "create table log (name text, time text, cameraName text, image BLOB)")
        return cursor, connection


def updateLocalDatabase(cursor, connection, name, frame):

    if check_condition(name):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
        # Files cannot be saved with these characters
        viableFileName = dt_string.replace("/", "-").replace(":", "-")
        print("date and time =", dt_string)

        # Images of people spotted on the security camera are captured and saved as a hash of its datetime
        cv2.imwrite("FacesCaptured/" + viableFileName + ".jpg", frame)

        # Read the image file into memory as binary data
        with open("FacesCaptured/" + viableFileName + ".jpg", "rb") as f:
            image_data = f.read()

        cursor.execute("insert into log values(?,?,?,?)",
                       (name, dt_string, "Webcam", image_data))
        connection.commit()


# Condition check, only adds name to database if it hasnt already in the last 10 seconds
def check_condition(string):
    global last_checked

    if string not in last_checked or time.time() - last_checked[string] > 10:
        last_checked[string] = time.time()
        return True
    else:
        return False
