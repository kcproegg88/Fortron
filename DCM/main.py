from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt5.QtGui import QPixmap
import sys
import os
from login_registration import LoginPage, RegisterPage
from mainpage import MainPage
from serial_coms import serial_stuff


class DCM(QMainWindow):  # Main application window
    def __init__(self):
        super().__init__()

        # Main attributes and settings
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo = QPixmap(os.path.join(current_dir, "logo.png"))
        self.user_file = os.path.join(current_dir, "users.txt")
        self.logo = QPixmap("logo.png")
        self.user_file = "users.txt"
        self.users, self.data = {}, {}
        self.read_users()

        self.setWindowTitle("DCM")
        self.setStyleSheet("background-color: rgb(205, 205, 255);")

        # State variables for page navigation and user data
        self.max_users, self.key = 10, "1234"
        self.pacemaker_modes, self.user = {}, ""
        self.default_data = {"AOO": [102, 112, 18, 97], "VOO": [102, 112, 18, 97],
                             "AAI": [102, 112, 18, 97, 512, 325, 325], "VVI": [102, 112, 18, 97, 512, 325, 350, 1171]}
        self.user_data = {}
        self.page = 0
        self.pages_stacked_widget = QStackedWidget()
        self.login_page, self.register_page, self.main_page = LoginPage(self), RegisterPage(self), MainPage(self)
        [self.pages_stacked_widget.addWidget(page_widget) for page_widget in [self.login_page, self.register_page, self.main_page]]
        self.setCentralWidget(self.pages_stacked_widget)
        self.run_gui()
        serial_stuff(dcm)

    def read_users(self):
        """Load user credentials and settings from file."""
        with open(self.user_file, 'r') as f:
            for line in f:
                if ':' in line:
                    username, password, saved_data = line.strip().split(':', 2)
                    self.users[username] = password
                    self.data[username] = [list(map(int, mode.split())) for mode in saved_data.split(",")]

    def write_user(self, username, password, data):
        """Append a new user's data to the user file."""
        with open(self.user_file, 'a') as f:
            f.write(f"{username}:{password}:{','.join(data)}\n")
        self.read_users()  # Refresh user data

    def save_parameters(self):
        """Save the current user's settings for all modes."""
        data = [" ".join(map(str, self.pacemaker_modes[i].send_values())) for i in self.pacemaker_modes]
        self.write_user(self.user, self.users[self.user], list(map(str, data)))

    def sign_out(self):
        """Log out current user and return to the login page."""
        self.page = 0
        self.run_gui()

    def update_modes(self):
        for mode in self.pacemaker_modes:
            self.pacemaker_modes[mode].update_parameters()

    def run_gui(self):
        """Initialize and set the current page layout."""
        self.pages_stacked_widget.setCurrentIndex(self.page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showMaximized()
    sys.exit(app.exec())
