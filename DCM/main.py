from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout
import sys


class DCM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DCM')
        # self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.welcome_screen()

    def welcome_screen(self):
        welcome_layout = QHBoxLayout()
        QLabel("Login")
        login_layout = QFormLayout()
        button1 = QLabel("User Name")
        lineEdit1 = QLineEdit()
        button2 = QLabel("Password")
        lineEdit2 = QLineEdit()
        login_layout.addRow(button1, lineEdit1)
        login_layout.addRow(button2, lineEdit2)
        welcome_layout.addLayout(login_layout)
        self.textbox = QLineEdit(self)
        welcome_layout.addWidget(self.textbox)

        self.textbox1 = QLineEdit(self)
        self.textbox1.resize(300, 40)
        welcome_layout.addWidget(self.textbox1)
        welcome_layout.addWidget(QPushButton("Left-Most"))
        welcome_layout.addWidget(QPushButton("Center"), 1)
        welcome_layout.addWidget(QPushButton("Right-Most"), 2)

        container = QWidget()
        container.setLayout(welcome_layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showFullScreen()
    sys.exit(app.exec())