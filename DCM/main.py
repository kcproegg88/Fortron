from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPixmap
import sys
import os
from login_registration import LoginPage, RegisterPage
from mainpage import MainPage
from parameter_display import PaceMakerMode
from serial_coms import check_connection, serial_comm
from graph import LiveGraphWidget


class DCM(QMainWindow):  # Main application window
    def __init__(self):
        super().__init__()

        # Main attributes and settings
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo = QPixmap(os.path.join(current_dir, "logo.png"))
        self.user_file = os.path.join(current_dir, "users.txt")
        self.logo = QPixmap("logo.png")
        self.pacemaker_serial = "000621000000"
        self.users, self.data = {}, {}
        self.read_users()

        self.setWindowTitle("DCM")
        self.setStyleSheet("background-color: rgb(205, 205, 255);")

        # State variables for page navigation and user data
        self.max_users, self.key = 10, "1234"
        self.init_modes()

        self.graph = LiveGraphWidget(self)

        self.page = 0
        self.pages_stacked_widget = QStackedWidget()
        self.login_page, self.register_page, self.main_page = LoginPage(self), RegisterPage(self), MainPage(self)
        [self.pages_stacked_widget.addWidget(page_widget) for page_widget in [self.login_page, self.register_page, self.main_page]]
        self.setCentralWidget(self.pages_stacked_widget)
        self.run_gui()
        print(check_connection(self.pacemaker_serial))

    def init_modes(self):
        """Creates and adds parameter widgets for each pacing mode."""
        self.pacemaker_modes, self.user = {}, ""
        self.default_data = {"AOO": [60, 120, 5, 40], "VOO": [60, 120, 5, 40],
                             "AAI": [60, 120, 5, 40, 75, 250, 250, 60, 0], "VVI": [60, 120, 5, 40, 250, 320, 60, 0],
                             "AOOR": [60, 120, 120, 5, 40, 30, 8, 5], "VOOR": [60, 120, 120, 5, 40, 30, 8, 5],
                             "AAIR": [60, 120, 120, 5, 40, 75, 250, 250, 60, 0, 30, 8, 5],
                             "VVIR": [60, 120, 120, 5, 40, 250, 320, 60, 0, 30, 8, 5]}

        self.user_data = {mode: values[:] for mode, values in self.default_data.items()}
        modes_params = {
            "AOO": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Atrial amplitude", 5, 32, 10], ["Atrial pulse width", 5, 190, 100]],
            "VOO": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Ventricular amplitude", 5, 32, 10], ["Ventricular pulse width", 5, 190, 100]],
            "AAI": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Atrial amplitude", 5, 32, 10], ["Atrial pulse width", 5, 190, 100],
                    ["Atrial sensitivity", 25, 1000, 100], ["ARP", 150, 500, 1], ["PVARP", 150, 500, 1],
                    ["Hysteresis", 30, 175, 1], ["Rate Smoothing", 0, 25, 1]],
            "VVI": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Ventricular amplitude", 5, 32, 10], ["Ventricular pulse width", 5, 190, 100],
                    ["Ventricular sensitivity", 25, 1000, 100], ["VRP", 150, 500, 1],
                    ["Hysteresis", 30, 175, 1], ["Rate Smoothing", 0, 25, 1]],
            "AOOR": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                     ["Maximum Sensor Rate", 50, 175, 1], ["Atrial amplitude", 5, 32, 10],
                     ["Atrial pulse width", 5, 190, 100],
                     ["Reaction Time", 10, 50, 1], ["Response Factor", 1, 16, 1], ["Recovery Time", 2, 16, 1]],
            "VOOR": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                     ["Maximum Sensor Rate", 50, 175, 1], ["Ventricular amplitude", 5, 32, 10],
                     ["Ventricular pulse width", 5, 190, 100],
                     ["Reaction Time", 10, 50, 1], ["Response Factor", 1, 16, 1], ["Recovery Time", 2, 16, 1]],
            "AAIR": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                     ["Maximum Sensor Rate", 50, 175, 1], ["Atrial amplitude", 5, 32, 10],
                     ["Atrial pulse width", 5, 190, 100], ["Atrial Sensitivity", 25, 1000, 100], ["ARP", 150, 500, 10],
                     ["PVARP", 150, 500, 10], ["Hysteresis", 30, 175, 1], ["Rate Smoothing", 0, 25, 1],
                     ["Reaction Time", 10, 50, 10], ["Response Factor", 1, 16, 1], ["Recovery Time", 2, 16, 1]],
            "VVIR": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                     ["Maximum Sensor Rate", 50, 175, 1], ["Ventricular amplitude", 5, 32, 10],
                     ["Ventricular pulse width", 5, 190, 100], ["Ventricular Sensitivity", 25, 1000, 100], ["VRP", 150, 500, 10],
                     ["Hysteresis", 30, 175, 1], ["Rate Smoothing", 0, 25, 1],
                     ["Reaction Time", 10, 50, 10], ["Response Factor", 1, 16, 1], ["Recovery Time", 2, 16, 1]]}

        for mode, params in modes_params.items():
            self.pacemaker_modes[mode] = PaceMakerMode(mode, self, params)

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

    def save_all(self):
        """Save the current user's settings for all modes."""
        data = [" ".join(map(str, self.pacemaker_modes[i].send_values())) for i in self.pacemaker_modes]
        self.write_user(self.user, self.users[self.user], list(map(str, data)))

    def reset_all(self):
        [self.pacemaker_modes[mode].reset_parameters() for mode in self.pacemaker_modes]

    def save_mode(self):
        current_index = self.main_page.mode_tabs.currentIndex()
        current_mode = self.main_page.mode_tabs.tabText(current_index)
        self.user_data[current_mode] = self.pacemaker_modes[current_mode].send_values()
        data = [" ".join(map(str, self.user_data[i])) for i in self.user_data]
        self.write_user(self.user, self.users[self.user], list(map(str, data)))

    def update_modes(self):
        for mode in self.pacemaker_modes:
            self.pacemaker_modes[mode].update_parameters()

    def check_port_connection(self):
        port = check_connection(self.pacemaker_serial)
        if port:
            self.main_page.device_status.setText("Device Connected")
            self.main_page.device_status.setStyleSheet("color: green;")
        else:
            self.main_page.device_status.setText("No Device Detected")
            self.main_page.device_status.setStyleSheet("color: red;")
        return port

    def run_gui(self):
        """Initialize and set the current page layout."""
        self.check_port_connection()
        self.pages_stacked_widget.setCurrentIndex(self.page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dcm = DCM()
    dcm.showMaximized()
    sys.exit(app.exec())
