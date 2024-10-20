from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

class DCM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logo = QPixmap("logo.png")  # Ensure the logo path is correct
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
        leftside = QVBoxLayout()
        title = QLabel("Login")
        title.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        title.setAlignment(Qt.AlignCenter)

        # form
        login_layout = QFormLayout()
        button1 = QLabel("User Name")
        button1.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        button2 = QLabel("Password")
        button2.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.lineEdit2.setEchoMode(QLineEdit.Password)

        login_layout.addRow(button1, self.lineEdit1)
        login_layout.addRow(button2, self.lineEdit2)

        leftside.addStretch()  # top
        leftside.addWidget(title)
        leftside.addLayout(login_layout)

        # Add login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)  # Connect to the handle_login method
        leftside.addWidget(login_button)

        leftside.addStretch()  # bottom

        login_side = QWidget()
        login_side.setLayout(leftside)

        # right side for logo
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
        # Placeholder for registration page layout
        register_layout = QVBoxLayout()
        register_label = QLabel("Registration Page")
        register_label.setAlignment(Qt.AlignCenter)
        register_layout.addWidget(register_label)
        return register_layout

    def handle_login(self):
        username = self.lineEdit1.text()
        password = self.lineEdit2.text()
        print(f"Username: {username}, Password: {password}")

        # Here you could add your login logic and switch to the next page
        # For example:
        # if valid_login(username, password):
        #     self.page = 1  # Switch to registration or another page
        #     self.run_gui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showFullScreen()
    sys.exit(app.exec())
