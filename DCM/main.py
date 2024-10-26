from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap
import sys
from login_registration import LoginPage, RegisterPage
from mainpage import MainPage


class DCM(QMainWindow):  # Main application window
    def __init__(self):
        super().__init__()

        # Main attributes and settings
        self.logo = QPixmap("logo.png")
        self.user_file = "users.txt"
        self.users, self.data = {}, {}
        self.read_users()

        self.setWindowTitle("DCM")
        self.setStyleSheet("background-color: rgb(205, 205, 255);")

        # State variables for page navigation and user data
        self.page = 0
        self.pages = [None] * 3
        self.max_users, self.key = 10, "1234"
        self.mode, self.user = {}, ""
        self.user_data = {"AOO": [102, 112, 18, 97], "VOO": [102, 112, 18, 97],
                          "AAI": [102, 112, 18, 97, 512, 325, 325],"VVI": [102, 112, 18, 97, 512, 325, 350, 1171]}

        self.run_gui()

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
        data = [" ".join(map(str, self.mode[i].send_values())) for i in ["AOO", "VOO", "AAI", "VVI"]]
        self.write_user(self.user, self.users[self.user], list(map(str, data)))

    def sign_out(self):
        """Log out current user and return to the login page."""
        self.page = 0
        self.run_gui()

    def run_gui(self):
        """Initialize and set the current page layout."""
        self.pages[0], self.pages[1], self.pages[2] = LoginPage(self), RegisterPage(self), MainPage(self)
        main_container = QWidget()
        main_container.setLayout(self.pages[self.page].layout)
        self.setCentralWidget(main_container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showFullScreen()
    sys.exit(app.exec())
