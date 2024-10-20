from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


class DCM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logo = QPixmap("logo.png")
        self.setWindowTitle('DCM')
        # self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.run_gui()

    def run_gui(self):
        container = QWidget()
        container.setLayout(self.welcome_screen())
        self.setCentralWidget(container)

    def welcome_screen(self):
        welcome_layout = QHBoxLayout()

        #login page side
        leftside = QVBoxLayout()

        login_layout = QFormLayout()
        button1 = QLabel("User Name")
        lineEdit1 = QLineEdit()
        button2 = QLabel("Password")
        lineEdit2 = QLineEdit()
        login_layout.addRow(button1, lineEdit1)
        login_layout.addRow(button2, lineEdit2)

        leftside.addStretch()
        leftside.addLayout(login_layout)
        leftside.addStretch()

        #
        rightside = QVBoxLayout()
        logolable = QLabel()
        logolable.setPixmap(self.logo)

        rightside.addStretch()
        rightside.addWidget(logolable, alignment=Qt.AlignCenter)
        rightside.addStretch()

        welcome_layout.addLayout(leftside, 1)
        welcome_layout.addLayout(rightside, 1)
        # textbox = QLineEdit(self)
        # welcome_layout.addWidget(textbox)
        # self.textbox1 = QLineEdit(self)
        # self.textbox1.resize(300, 40)
        # welcome_layout.addWidget(self.textbox1)
        # welcome_layout.addWidget(QPushButton("Left-Most"))
        # welcome_layout.addWidget(QPushButton("Center"), 1)
        # welcome_layout.addWidget(QPushButton("Right-Most"), 2)
        return welcome_layout
        # container = QWidget()
        # container.setLayout(welcome_layout)
        # self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showFullScreen()
    sys.exit(app.exec())