"""
Author: Connor Murphy

This file contains two classes:
-One to run the GUI using PyQt5
-One to run the video captures and facial recognition

It calls the video capure class with a "QThread" to be run seperately. The frames are sent back and displayed in the Gui.
As those frames are captures they are stored in a SQLite Database, which is then read by the Gui class, and loaded into tables.
"""


import sqlite3
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QPixmap, QImage, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import QTimer, Qt, QItemSelectionModel

from datetime import date, datetime
import face_recognition
import cv2
import numpy as np
from PushNotificationNotes import *
import localDataFuntions


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1220, 960)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Logo_Qlabel = QtWidgets.QLabel(self.centralwidget)
        self.Logo_Qlabel.setGeometry(QtCore.QRect(93, 0, 200, 125))
        self.Logo_Qlabel.setObjectName("Logo_Qlabel")
        self.Logo_Qlabel.setStyleSheet("border: 0px")
        self.DataBase_tableView = QtWidgets.QTableView(self.centralwidget)
        self.DataBase_tableView.setGeometry(QtCore.QRect(0, 371, 475, 540))
        self.DataBase_tableView.setObjectName("DataBase_tableView")
        self.DataBase_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.DataBase_tableView.clicked.connect(self.on_selectionChanged)

        self.SecurityShot_Qlabel = QtWidgets.QLabel(self.centralwidget)
        self.SecurityShot_Qlabel.setGeometry(QtCore.QRect(485, 643, 351, 271))
        self.SecurityShot_Qlabel.setObjectName("SecurityShot_Qlabel")
        # Active
        self.SecurityVideo_Qlabel = QtWidgets.QLabel(self.centralwidget)
        self.SecurityVideo_Qlabel.setGeometry(QtCore.QRect(485, 13, 351, 271))
        self.SecurityVideo_Qlabel.setObjectName("SecurityVideo_Qlabel")
        # Inactive, for placement in update
        self.SecurityVideo2_Qlabel = QtWidgets.QLabel(self.centralwidget)
        self.SecurityVideo2_Qlabel.setGeometry(QtCore.QRect(485, 330, 351, 271))
        self.SecurityVideo2_Qlabel.setObjectName("SecurityVideo3_Qlabel")
        self.SecurityVideo3_Qlabel = QtWidgets.QLabel(self.centralwidget)
        self.SecurityVideo3_Qlabel.setGeometry(QtCore.QRect(850, 13, 351, 271))
        self.SecurityVideo3_Qlabel.setObjectName("SecurityVideo3_Qlabel")
        self.SecurityVideo4_Qlabel = QtWidgets.QLabel(self.centralwidget)
        self.SecurityVideo4_Qlabel.setGeometry(QtCore.QRect(850, 330, 351, 271))
        self.SecurityVideo4_Qlabel.setObjectName("SecurityVideo4_Qlabel")

        # Active
        self.startCamera1_pushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.startCamera1_pushButton.setGeometry(QtCore.QRect(485, 290, 70, 31))
        self.startCamera1_pushButton.setObjectName("startCamera1_pushButton")
        self.stopCamera1_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopCamera1_pushButton.setGeometry(QtCore.QRect(560, 290, 70, 31))
        self.stopCamera1_pushButton.setObjectName("stopCamera1_pushButton")
        # Inactive, for placement in update
        self.startCamera2_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startCamera2_pushButton.setGeometry(QtCore.QRect(485, 607, 70, 31))
        self.startCamera2_pushButton.setObjectName("startCamera2_pushButton")
        self.stopCamera2_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopCamera2_pushButton.setGeometry(QtCore.QRect(560, 607, 70, 31))
        self.stopCamera2_pushButton.setObjectName("stopCamera2_pushButton")
        self.startCamera2_pushButton.setText("Start")
        self.stopCamera2_pushButton.setText("Stop")

        self.startCamera3_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startCamera3_pushButton.setGeometry(QtCore.QRect(850, 290, 70, 31))
        self.startCamera3_pushButton.setObjectName("startCamera3_pushButton")
        self.stopCamera3_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopCamera3_pushButton.setGeometry(QtCore.QRect(925, 290, 70, 31))
        self.stopCamera3_pushButton.setObjectName("stopCamera3_pushButton")
        self.startCamera3_pushButton.setText("Start")
        self.stopCamera3_pushButton.setText("Stop")

        self.startCamera4_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startCamera4_pushButton.setGeometry(QtCore.QRect(850, 607, 70, 31))
        self.startCamera4_pushButton.setObjectName("startCamera4_pushButton")
        self.stopCamera4_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopCamera4_pushButton.setGeometry(QtCore.QRect(925, 607, 70, 31))
        self.stopCamera4_pushButton.setObjectName("stopCamera4_pushButton")
        self.startCamera4_pushButton.setText("Start")
        self.stopCamera4_pushButton.setText("Stop")

        self.OpenFaces_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.OpenFaces_pushButton.setGeometry(QtCore.QRect(850, 880, 151, 31))
        self.OpenFaces_pushButton.setObjectName("OpenFaces_pushButton")
        self.openInstructions_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.openInstructions_pushButton.setGeometry(QtCore.QRect(1005, 880, 151, 31))
        self.openInstructions_pushButton.setObjectName("openInstructions_pushButton")
        self.Clock_label = QtWidgets.QLabel(self.centralwidget)
        self.Clock_label.setGeometry(QtCore.QRect(950, 775, 161, 35))
        self.Clock_label.setObjectName("Clock_label")
        self.Date_label = QtWidgets.QLabel(self.centralwidget)
        self.Date_label.setGeometry(QtCore.QRect(950, 750, 161, 35))
        self.Date_label.setObjectName("Date_label")

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 170, 361, 191))
        self.calendarWidget.setObjectName("calendarWidget")
        # Listens for calander selection
        self.calendarWidget.selectionChanged.connect(self.calendarSelected)
        self.displayAll_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.displayAll_pushButton.setGeometry(QtCore.QRect(380, 330, 95, 31))
        self.displayAll_pushButton.setObjectName("displayAll_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 989, 21))
        self.menubar.setObjectName("menubar")
        self.menuHome = QtWidgets.QMenu(self.menubar)
        self.menuHome.setObjectName("menuHome")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        # TOGGLE RECORD BUTTONS
        # Active
        self.toggle_button = QtWidgets.QPushButton(self.centralwidget)
        self.toggle_button.setGeometry(QtCore.QRect(665, 290, 151, 31))
        self.toggle_button.setText("Not Recording")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle)
        self.toggle_button.setStyleSheet("QPushButton {background-color:lightgreen}")
        self.manualToggle = 0
        # Inactive
        self.toggle_button2 = QtWidgets.QPushButton(self.centralwidget)
        self.toggle_button2.setGeometry(QtCore.QRect(665, 607, 151, 31))
        self.toggle_button2.setText("Not Recording")
        self.toggle_button2.setStyleSheet("QPushButton {background-color:lightgreen}")
        self.manualToggle2 = 0

        self.toggle_button3 = QtWidgets.QPushButton(self.centralwidget)
        self.toggle_button3.setGeometry(QtCore.QRect(1030, 290, 151, 31))
        self.toggle_button3.setText("Not Recording")
        self.toggle_button3.setStyleSheet("QPushButton {background-color:lightgreen}")
        self.manualToggle3 = 0

        self.toggle_button4 = QtWidgets.QPushButton(self.centralwidget)
        self.toggle_button4.setGeometry(QtCore.QRect(1030, 607, 151, 31))
        self.toggle_button4.setText("Not Recording")
        self.toggle_button4.setStyleSheet("QPushButton {background-color:lightgreen}")
        self.manualToggle4 = 0

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Set up button connections
        self.displayAll_pushButton.clicked.connect(self.displayAll_button_clicked)
        self.openInstructions_pushButton.clicked.connect(self.openInstructions_button_clicked)
        self.OpenFaces_pushButton.clicked.connect(self.openFaces_button_clicked)

		#dict for multiple threads, multiple cameras
        self.thread = {}
        self.startCamera1_pushButton.clicked.connect(self.start_worker_1)
        self.stopCamera1_pushButton.clicked.connect(self.stop_worker_1)

        # Displays logo
        self.Logo_pixmap = QPixmap("logo.jpg")
        self.Logo_Qlabel.setPixmap(self.Logo_pixmap)

        # Start the program off with the table filled
        self.getData()

        # Icon for no camera active
        pixmap = QPixmap("noPhoto2.jpg")
        # Places the image and resizes it to fix the box
        self.SecurityVideo_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.SecurityVideo2_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.SecurityVideo3_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.SecurityVideo4_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Updates the clock once per second
        self.timer = QTimer()
        self.timer.setInterval(1000/1)  # 1 fps
        self.timer.timeout.connect(self.updateClock)
        self.timer.start()

    # Button Functions

    def displayAll_button_clicked(self):
        print("Display All button was clicked.")
        self.getData()

    def openInstructions_button_clicked(self):
        print("Open Instructions All button was clicked.")
        os.startfile("README Instructions.txt")

    def openFaces_button_clicked(self):
        print("Open Faces All button was clicked.")
        os.startfile(r'Faces')

    def updateClock(self):

        font = QFont("Arial Black", 16)
        self.Clock_label.setFont(font)
        self.Date_label.setFont(font)

        currentTime = datetime.datetime.now()
        formattedTime = currentTime.strftime("%I:%M:%S %p")
        self.Clock_label.setText(formattedTime)

        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        self.Date_label.setText(date_str)

    # Pulls the selected row and sends its time reference to obtainSecurityShot()

    def on_selectionChanged(self):
        print("A Row was selected")

        print(self.DataBase_tableView.selectionModel().selectedIndexes()[1].data())
        timeReference = self.DataBase_tableView.selectionModel().selectedIndexes()[1].data()
        self.displaySecurityShot(timeReference)

    def calendarSelected(self):
        print("A calander date was selected")

        dateString = self.calendarWidget.selectedDate().toString("dd-MM-yyyy")
        dateString = dateString.replace("-", "/")
        dateString = "%" + dateString + "%"

        print(dateString)

        model = QStandardItemModel()

        connection = sqlite3.connect('securityLog.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM log WHERE time LIKE ?", (dateString,))

        rows = cursor.fetchall()

        # In case of empty table, sets blank
        if not rows:
            emptyModel = QStandardItemModel(self.DataBase_tableView)
            self.DataBase_tableView.setModel(emptyModel)
            self.setNoImageAvailable()
            return

        model.setColumnCount(len(rows[0]))
        headers = ['Name', 'Date & Time', 'Camera', 'Image Data']
        model.setHorizontalHeaderLabels(headers)

        for row in rows:
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)

        self.DataBase_tableView.setModel(model)

        # auto selects the top Row and displays its image
        selection_model = self.DataBase_tableView.selectionModel()
        first_row_index = self.DataBase_tableView.model().index(0, 0)
        selection_model.select(first_row_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.on_selectionChanged()

    def setNoImageAvailable(self):
        pixmap = QPixmap("noPhoto.jpg")
        # Places the image and resizes it to fix the box
        self.SecurityShot_Qlabel.setPixmap(pixmap.scaled(
            self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

 

    def getData(self):

        model = QStandardItemModel()

        cursor, connection = localDataFuntions.localDatabaseConnect()

        cursor.execute("SELECT * FROM log")
        rows = cursor.fetchall()

        # In case of empty database, sets blank
        if not rows:
            emptyModel = QStandardItemModel(self.DataBase_tableView)
            self.DataBase_tableView.setModel(emptyModel)
            self.setNoImageAvailable()
            return

        model.setColumnCount(len(rows[0]))
        headers = ['Name', 'Date & Time', 'Camera', 'Image Data']
        model.setHorizontalHeaderLabels(headers)

        for row in rows:
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)

        self.DataBase_tableView.setModel(model)

        # auto selects the top Row and displays its image
        selection_model = self.DataBase_tableView.selectionModel()
        first_row_index = self.DataBase_tableView.model().index(0, 0)
        selection_model.select(first_row_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.on_selectionChanged()

        self.DataBase_tableView.setColumnWidth(0, 75)
        self.DataBase_tableView.setColumnWidth(1, 150)

    # Display selected security shot

    def displaySecurityShot(self, timeReference):
        con = sqlite3.connect("securityLog.db")
        cur = con.cursor()
        cur.execute("SELECT image FROM log WHERE time = ?", (timeReference,))
        image_Data = cur.fetchone()[0]

        pixmap = QPixmap()
        pixmap.loadFromData(image_Data)

        # Places the image and resizes it to fix the box
        self.SecurityShot_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyViewSecurity"))
        self.OpenFaces_pushButton.setText(_translate("MainWindow", "Open Known Faces"))
        self.openInstructions_pushButton.setText(_translate("MainWindow", "Open Instructions"))
        self.startCamera1_pushButton.setText(_translate("MainWindow", "Start"))
        self.stopCamera1_pushButton.setText(_translate("MainWindow", "Stop"))

        self.Clock_label.setText(_translate("MainWindow", "TextLabel"))
        self.displayAll_pushButton.setText(_translate("MainWindow", "Display All"))
        self.menuHome.setTitle(_translate("MainWindow", "Home"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))

    # Connects and to the FaceRcognition Qthreat, recieves the video frames,  and sends them to displayAndSaveFrames to be displayed

    def start_worker_1(self):
        self.thread[1] = ThreadClass(parent=None, index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.displayAndSaveFrames)
        # So you cant enable the same thread twice
        self.startCamera1_pushButton.setEnabled(False)

    def stop_worker_1(self):
        self.thread[1].stop()
        # So you cant enable the same thread twice
        self.startCamera1_pushButton.setEnabled(True)
        pixmap = QPixmap("noPhoto2.jpg")
        self.SecurityVideo_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # Retrieves frames from thread to display in gui and save to security footage
    def displayAndSaveFrames(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimage = QImage(frame, frame.shape[1],frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        self.SecurityVideo_Qlabel.setPixmap(pixmap.scaled(self.SecurityShot_Qlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        if self.manualToggle == 1:
            # Writes frames to security footage output video
            self.out.write(frame)

    # Starts and tops recording variables
    def toggle(self):
        if self.toggle_button.isChecked():
            print("Not Recording")
            self.toggle_button.setText("Not Recording")
            self.toggle_button.setStyleSheet("QPushButton {background-color:lightgreen}")

            self.manualToggle = 0

            # Only closes them if theyve been initialized first
            if hasattr(self, 'out') and hasattr(self, 'fourcc'):
                self.out.release()

        else:
            print("Recording")
            self.toggle_button.setText("Recording")
            self.toggle_button.setStyleSheet("QPushButton {background-color:lightcoral}")

            # File name is Date and Tme
            now = datetime.datetime.now()
            date_time_string = now.strftime("%Y-%m-%d %H-%M-%S")
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            # Save location and name
            filename = os.path.join("Security_Footage", f"{date_time_string}.mp4")
            self.out = cv2.VideoWriter(filename, self.fourcc, 30.0, (640, 480))

            self.manualToggle = 1


# QThread that runs the camera and facial detection. Starts in start_worker1
class ThreadClass(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):

        print('Starting thread...', self.index)

        # Sets up / connects to local DB
        cursor, connection = localDataFuntions.localDatabaseConnect()

        # For current version, this pulls the video from the webcam. "To open default camera using default backend just pass 0"
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FPS, 30)

        # Only gets the jpeg files
        files = [file for file in os.listdir("Faces/") if file.endswith(('.jpeg', '.jpg'))]
        faceImages = [None] * len(files)
        known_face_encodings = [None] * len(files)
        known_face_names = [os.path.splitext(file)[0] for file in files]

        # Create arrays of known face encodings and their names.
        i = 0
        while i < len(files):
            faceImages[i] = face_recognition.load_image_file("Faces/" + files[i])
            known_face_encodings[i] = face_recognition.face_encodings(faceImages[i])[0]
            i = i + 1

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:

            # Returns one frame at a time. "video_capture.read: Grabs, decodes and returns the next video frame"
            ret, frame = video_capture.read()

            # Only process every other frame
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, model="small")  # testing small for better fps

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            # Switchinges between True and False to only process every other frame
            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top),(right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),(right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6),font, 1.0, (255, 255, 255), 1)

                # Saves names and timestamps to the local SQLite Database
                localDataFuntions.updateLocalDatabase(
                    cursor, connection, name, frame)

            # Sends frames back to the UI Class
            self.any_signal.emit(frame)

            # Hit 'q' on the keyboard to quit. Get rid of this?
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def stop(self):  
        self.is_running = False
        print('Stopping thread...', self.index)
        self.terminate()



def start():
    import sys

    app = QtWidgets.QApplication(sys.argv)

    style = """
    
        QLabel{
            color: #010101;
        }
        QLabel#round_count_label, QLabel#highscore_count_label{
            border: 1px solid #fff;
            border-radius: 8px;
            padding: 2px;
        }
        QPushButton
        {
             color: white;
            background: #284b63;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none;
        }
        QPushButton:hover{
            border: 1px #C6C6C6 solid;
            color: #fff;
            background: #0892D0;
        }
        QLabel#picture_label {
        border-radius: 5px;
        overflow: hidden;
        }
        """


    app.setStyleSheet(style)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
start()

