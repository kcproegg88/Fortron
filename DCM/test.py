from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton,
    QFormLayout, QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
from  parameter_display import PaceMakerMode

class DCM(QMainWindow):  # Main window class for DCM application
    def __init__(self):
        super().__init__()  # Initialize parent class
        self.logo = QPixmap("logo.png")  # Load logo image (don't show up for me for whatever reason)
        self.setWindowTitle('DCM')  # Set window title
        self.setStyleSheet("background-color: rgb(205, 205, 255);")
        self.page = 0  # number for page type shit
        self.users_file = "users.txt"  # File to store user data
        self.max_users = 10  # Maximum 10 users
        self.ensure_users_file_exists()  # Ensure the users file exists
        self.run_gui()  # Run GUI setup
        AOO = PaceMakerMode("AOO", ["Hi", "hello", "wsg"])
        VOO = PaceMakerMode("VOO", ["Hi", "hello", "wsg"])
        AAI = PaceMakerMode("AAI", ["Hi", "hello", "wsg"])
        VVI = PaceMakerMode("VVI", ["Hi", "hello", "wsg"])
        self.mode = {"A00": AOO, "VOO": VOO, "AAI": AAI, "VVI": VVI}

    def ensure_users_file_exists(self):
        """Ensure that the users file exists. If not, create it."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                pass  # Create an empty file

    def run_gui(self):
        container = QWidget()  # Create main container widget
        print(self.page)
        if self.page == 0:
            container.setLayout(self.login_page())  # Change to login layout
        elif self.page == 1:
            container.setLayout(self.register_page())  # Change to register layout
        elif self.page == 2:
            container.setLayout(self.main_page())  # Change to main layout
        self.setCentralWidget(container)  # Set container as central widget

    def read_users(self):
        """
        Read users from the users file.
        Returns a dictionary with username as key and password as value.
        """
        users = {}
        with open(self.users_file, 'r') as f:
            for line in f:
                if ':' in line:
                    username, password = line.strip().split(':', 1)
                    users[username] = password
        return users

    def write_user(self, username, password):
        """
        Write a new user to the users file.
        """
        with open(self.users_file, 'a') as f:
            f.write(f"{username}:{password}\n")

    def login_page(self):
        welcome_layout = QHBoxLayout()  # Main layout

        # Left side (Login form)
        leftside = QVBoxLayout()  # Vertical layout for login form
        title = QLabel("Login")  # Title
        title.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        title.setAlignment(Qt.AlignCenter)  # Center title

        # Login form layout
        login_layout = QFormLayout()  # Form layout for inputs
        label_username = QLabel("User Name")  # Username label
        label_username.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Label
        self.username_input = QLineEdit()  # Input for username
        self.username_input.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Input
        label_password = QLabel("Password")  # Password label
        label_password.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Label
        self.password_input = QLineEdit()  # Input for password
        self.password_input.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Input
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password

        login_layout.addRow(label_username, self.username_input)  # Add username row
        login_layout.addRow(label_password, self.password_input)  # Add password row

        # Login and Register buttons
        login_button = QPushButton("Login")  # Login button
        login_button.clicked.connect(self.handle_login)  # Call handle_login method
        register_button = QPushButton("Register")  # Register button
        register_button.clicked.connect(self.show_register_page)  # Call show_register_page method

        # Warning label for login errors
        self.login_warning = QLabel("")  # Label
        self.login_warning.setStyleSheet("color: red;")  # Red
        self.login_warning.setAlignment(Qt.AlignCenter)  # Center

        # Assemble left side layout
        leftside.addStretch()  # Top
        leftside.addWidget(title)  # Title
        leftside.addLayout(login_layout)  # Add form
        leftside.addWidget(self.login_warning)  # Add warning label
        leftside.addWidget(login_button)  # Add login button
        leftside.addWidget(register_button)  # Add register button
        leftside.addStretch()  # Bottom

        login_side = QWidget()  # Widget for left side
        login_side.setLayout(leftside)  # Layout for widget

        # Right side (Logo image)
        rightside = QVBoxLayout()  # Vertical layout for image
        logolabel = QLabel()  # Label to hold image
        logolabel.setPixmap(self.logo)  # Set image pixmap
        rightside.addStretch()
        rightside.addWidget(logolabel, alignment=Qt.AlignCenter)  # Add image to layout and center
        rightside.addStretch()

        # Combine left and right sides
        welcome_layout.addWidget(login_side, 1, alignment=Qt.AlignHCenter)  # Add left side to main layout
        welcome_layout.addLayout(rightside, 1)  # Add right side to main layout

        return welcome_layout  # Return complete layout

    def register_page(self):
        register_layout = QHBoxLayout()  # Main layout

        # Left side (Registration form)
        leftside = QVBoxLayout()  # Vertical layout for registration form
        title = QLabel("Register")  # Title
        title.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        title.setAlignment(Qt.AlignCenter)  # Center

        # Registration form layout
        register_form = QFormLayout()  # Form layout
        label_username = QLabel("User Name")  # Username label
        label_username.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Label
        self.reg_username_input = QLineEdit()  # Input for username
        self.reg_username_input.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Input
        label_password = QLabel("Password")  # Password label
        label_password.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Label
        self.reg_password_input = QLineEdit()  # Input for password
        self.reg_password_input.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")  # Input
        self.reg_password_input.setEchoMode(QLineEdit.Password)  # Hide password

        register_form.addRow(label_username, self.reg_username_input)  # Add username row to form
        register_form.addRow(label_password, self.reg_password_input)  # Add password row to form

        # Register and Back buttons
        register_button = QPushButton("Register")  # Register button
        register_button.clicked.connect(self.handle_register)  # Call handle_register method
        back_button = QPushButton("Back")  # Back button
        back_button.clicked.connect(self.show_login_page)  # Call show_login_page method

        # Warning label for registration errors
        self.register_warning = QLabel("")  # Label for warning
        self.register_warning.setStyleSheet("color: red;")  # Red
        self.register_warning.setAlignment(Qt.AlignCenter)  # Center

        # Assemble left side layout
        leftside.addStretch()  # Top
        leftside.addWidget(title)  # Title
        leftside.addLayout(register_form)  # Add form
        leftside.addWidget(self.register_warning)  # Add warning label
        leftside.addWidget(register_button)  # Add register button
        leftside.addWidget(back_button)  # Add back button
        leftside.addStretch()  # Bottom

        register_side = QWidget()  # Widget for left side
        register_side.setLayout(leftside)  # Layout for widget

        # Right side (Logo image)
        rightside = QVBoxLayout()  # Vertical layout for image
        logolabel = QLabel()  # Label to hold image
        logolabel.setPixmap(self.logo)  # Set image pixmap
        rightside.addStretch()
        rightside.addWidget(logolabel, alignment=Qt.AlignCenter)  # Add image to layout and center
        rightside.addStretch()

        # Combine left and right sides
        register_layout.addWidget(register_side, 1, alignment=Qt.AlignHCenter)  # Add left side to main layout
        register_layout.addLayout(rightside, 1)  # Add right side to main layout

        return register_layout  # Return complete layout

    def handle_login(self):
        username = self.username_input.text().strip()  # Get username
        password = self.password_input.text().strip()  # Get password

        if not username or not password:
            self.login_warning.setText("Please enter both username and password.")
            return

        # Read users from file
        users = self.read_users()

        # Check if username and password are correct
        if username in users and users[username] == password:
            self.page = 2  # Set page to main page
            self.run_gui()  # Refresh GUI
        else:
            self.login_warning.setText("Incorrect Username or Password")  # Show error message

    def handle_register(self):
        username = self.reg_username_input.text().strip()  # Get username
        password = self.reg_password_input.text().strip()  # Get password

        if not username or not password:
            self.register_warning.setText("Please enter both username and password.")
            return

        # Read existing users from file
        users = self.read_users()

        # Check if maximum users reached
        if len(users) >= self.max_users:
            self.register_warning.setText("Maximum users reached")  # Show error message
            return

        # Check if username already exists
        if username in users:
            self.register_warning.setText("Username already exists")  # Show error message
        else:
            self.write_user(username, password)  # Add user to file
            self.register_warning.setStyleSheet("color: green;")
            self.register_warning.setText("Registration successful! Please log in.")
            # Optionally, clear the input fields
            self.reg_username_input.clear()
            self.reg_password_input.clear()

    def show_register_page(self):
        self.page = 1  # Set page to register
        self.run_gui()  # Refresh GUI

    def show_login_page(self):
        self.page = 0  # Set page to login
        self.run_gui()  # Refresh GUI

    def main_page(self):
        main_layout = QVBoxLayout()  # Main layout

        # Title
        title = QLabel("DCM Main Interface")  # Title
        title.setAlignment(Qt.AlignCenter)  # Center
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Pacing modes selection
        mode_label = QLabel("Select Pacing Mode:")  # Label
        self.mode_combo = QComboBox()  # Combo box
        self.mode_combo.addItems(["AOO", "VOO", "AAI", "VVI"])  # Add pacing modes

        # Programmable parameters display
        params_label = QLabel("Programmable Parameters:")  # Label for parameters
        params_label.setStyleSheet("font-weight: bold;")

        self.params_widget = QWidget()  # Label for parameters
        params_layout = QHBoxLayout()
        params_layout.addWidget(self.mode["AOO"])
        self.params_widget.setLayout(params_layout)


        # Communication status
        comm_status_label = QLabel("Communication Status:")  # Label for communication status
        comm_status_label.setStyleSheet("font-weight: bold;")  # Bold text
        self.comm_status = QLabel("Not Connected")  # Placeholder status
        self.comm_status.setStyleSheet("color: red;")  # Red

        # Device identification status
        device_status_label = QLabel("Device Status:")  # Label for device status
        device_status_label.setStyleSheet("font-weight: bold;")  # Bold text
        self.device_status = QLabel("No Device Detected")  # Placeholder status
        self.device_status.setStyleSheet("color: red;")  # Red

        # Assemble main layout
        main_layout.addWidget(title)  # Title
        main_layout.addWidget(mode_label)  # Add pacing mode label
        main_layout.addWidget(self.mode_combo)  # Add pacing mode
        main_layout.addWidget(params_label)  # Add parameters label
        main_layout.addLayout(self.params_widget)  # Add parameters label
        main_layout.addWidget(comm_status_label)  # Add communication status label
        main_layout.addWidget(self.comm_status)  # Add communication status
        main_layout.addWidget(device_status_label)  # Add device status label
        main_layout.addWidget(self.device_status)  # Add device status placeholder

        self.mode_combo.currentTextChanged.connect(self.update_parameters)

        return main_layout  # Return complete layout

    def update_parameters(self):
        selected_mode = self.mode_combo.currentText()
        mode_widget = self.mode.get(selected_mode)
        layout = QHBoxLayout()
        layout.addWidget(mode_widget)

        # Clear previous layout if any
        for i in reversed(range(self.params_widget.layout().count())):
            self.params_widget.layout().itemAt(i).widget().setParent(None)

        self.params_widget.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create application
    dcm = DCM()  # Create instance of DCM class
    dcm.showFullScreen()  # Show application in full-screen
    sys.exit(app.exec())  # Start event loop
