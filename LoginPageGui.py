#To be used in the Online Features Update

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap
from MainPageGui import Ui_MainWindow, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class LoginDialog(QDialog): 
    def __init__(self):
        super().__init__() 

        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("logo.jpg")
        self.logo_label.setPixmap(self.logo_pixmap)

        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")
        self.username_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.start_offline_button = QPushButton("Start Offline")

        logo_layout = QHBoxLayout()
        logo_layout.addStretch()
        logo_layout.addWidget(self.logo_label)
        logo_layout.addStretch()

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_line_edit)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_line_edit)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.start_offline_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(logo_layout)
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)

        self.login_button.clicked.connect(self.on_login_button_clicked)
        self.start_offline_button.clicked.connect(self.on_start_offline_button_clicked)



    def startOfflineMode(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.hide()
        

    def on_login_button_clicked(self):
        print("Login button was clicked.")

    def on_start_offline_button_clicked(self):
        print("Start Offline button was clicked.")
        self.startOfflineMode()





#if __name__ == "__main__":
app = QApplication(sys.argv)
login_dialog = LoginDialog()
login_dialog.show()
sys.exit(app.exec_())