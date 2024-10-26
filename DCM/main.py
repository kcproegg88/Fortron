from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QStackedWidget, QComboBox, QFormLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
from parameter_display import PaceMakerMode
from login_registration import LoginPage, RegisterPage
from mainpage import MainPage


class DCM(QMainWindow):  # Main Window Class For DCM Application
    def __init__(self):
        super().__init__()
        self.logo = QPixmap("logo.png")
        self.user_file = "users.txt"
        self.read_users()
        self.setWindowTitle("DCM")
        self.setStyleSheet("background-color: rgb(205, 205, 255);")
        self.page = 0  # Page Number
        self.pages = [0]*3
        self.max_users = 10
        self.key = "1234"
        self.mode = {}
        self.user = ""
        self.user_data = {"AOO":[102, 112, 18, 97], "VOO":[102, 112, 18, 97], "AAI":[102, 112, 18, 97, 512, 325, 325], "VVI":[102, 112, 18, 97, 512, 325, 350, 1171]}

        self.run_gui()

    def read_users(self):
        self.users = {}
        self.data = {}
        with open(self.user_file, 'r') as f:
            for line in f:
                if ':' in line:
                    username, password, saved_data = line.strip().split(':', 2)
                    self.users[username] = password
                    self.data[username] = [list(map(int, mode.split())) for mode in saved_data.split(",")]

    def write_user(self, username, password, data):
        with open(self.user_file, 'a') as f:
            f.write(f"{username}:{password}:{",".join(data)}\n")
        self.read_users()

    def save_parameters(self):
        data = [" ".join(map(str, self.mode[i].send_values())) for i in ["AOO", "VOO", "AAI", "VVI"]]
        self.write_user(self.user, self.users[self.user], list(map(str, data)))

    def sign_out(self):
        self.page = 0
        self.run_gui()

    def run_gui(self):
        self.pages[0] = LoginPage(self)
        self.pages[1] = RegisterPage(self)
        self.pages[2] = MainPage(self)
        main_container = QWidget()
        main_container.setLayout(self.pages[self.page].layout)
        self.setCentralWidget(main_container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showFullScreen()
    sys.exit(app.exec())