from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from login_registration import handle_login
import sys


class DCM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logo = QPixmap("logo.png")
        self.setWindowTitle('DCM')
        self.setStyleSheet("background-color: rgb(205, 205, 255);")
        self.page = 0
        self.run_gui()

    def run_gui(self):
        container = QWidget()
        if self.page == 0:
            container.setLayout(self.login_page())
        elif self.page == 1:
            container.setLayout(self.register_page())
        self.setCentralWidget(container)

    def login_page(self):
        welcome_layout = QHBoxLayout()

        # login page side
        # title
        leftside = QVBoxLayout()
        title = QLabel("Login")
        title.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        title.setAlignment(Qt.AlignCenter)

        # form
        login_layout = QFormLayout()
        button1 = QLabel("User Name")
        button1.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.username = QLineEdit()
        self.username.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        button2 = QLabel("Password")
        button2.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.password = QLineEdit()
        self.password.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.password.setEchoMode(QLineEdit.Password)

        login_layout.addRow(button1, self.username)
        login_layout.addRow(button2, self.password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(lambda: handle_login(self))

        leftside.addStretch() #top
        leftside.addWidget(title)
        leftside.addLayout(login_layout)
        leftside.addWidget(login_button)
        leftside.addStretch() #bottom


        login_side = QWidget()
        login_side.setLayout(leftside)

        #
        rightside = QVBoxLayout()
        logolable = QLabel()
        logolable.setPixmap(self.logo)

        rightside.addStretch()
        rightside.addWidget(logolable, alignment=Qt.AlignCenter)
        rightside.addStretch()

        welcome_layout.addWidget(login_side, 1, alignment=Qt.AlignHCenter)
        welcome_layout.addLayout(rightside, 1)
        return welcome_layout

    def register_page(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showFullScreen()
    sys.exit(app.exec())