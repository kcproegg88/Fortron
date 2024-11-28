from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtCore import Qt


class LoginPage(QWidget):
    def __init__(self, dcm):
        super().__init__()

        self.dcm = dcm
        self.layout = QHBoxLayout()
        self.left_side()
        self.right_side()
        self.layout.addLayout(self.left_side_layout, 1)
        self.layout.addLayout(self.right_side_layout, 1)
        self.setLayout(self.layout)

    def left_side(self):
        """Creates the Login Side for the Login Page"""
        self.left_side_layout = QVBoxLayout()
        title = QLabel("Login")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #2D3E50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)

        # Login form layout
        login_layout = QFormLayout()  # Form layout for inputs

        label_username = QLabel("User Name")  # Username label
        label_username.setStyleSheet("font-size: 18px; color: #2D3E50;")  # Label 
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #2D3E50; border-radius: 5px;") # Input

        label_password = QLabel("Password")  # Password label
        label_password.setStyleSheet("font-size: 18px; color: #2D3E50;")  # Label
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #2D3E50; border-radius: 5px;") # Input
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password

        login_layout.addRow(label_username, self.username_input)  # Add username row
        login_layout.addRow(label_password, self.password_input)  # Add password row

        # Login and Register buttons
        login_button = QPushButton("Login")  # Login button
        login_button.setStyleSheet("background-color: #3CB371; color: white; font-size: 18px; font-weight: bold; padding: 10px; border: none; border-radius: 5px;")
        login_button.clicked.connect(self.handle_login)  # Call handle_login method

        register_button = QPushButton("Register")  # Register button
        register_button.setStyleSheet("background-color: #4682B4; color: white; font-size: 18px; font-weight: bold; padding: 10px; border: none; border-radius: 5px;")
        register_button.clicked.connect(self.show_register_page)  # Call show_register_page method

        # Warning label for login errors
        self.login_warning = QLabel("")  # Label
        self.login_warning.setStyleSheet("color: red; font-size: 14px;")  # Red
        self.login_warning.setAlignment(Qt.AlignCenter)  # Center

        # Assemble left side layout
        self.left_side_layout.addStretch()  # Top
        self.left_side_layout.addWidget(title)  # Title
        self.left_side_layout.addLayout(login_layout)  # Add form
        self.left_side_layout.addWidget(self.login_warning)  # Add warning label
        self.left_side_layout.addWidget(login_button)  # Add login button
        self.left_side_layout.addWidget(register_button)  # Add register button
        self.left_side_layout.addStretch()  # Bottom

    def right_side(self):
        """Creates the Image side of the Login Page"""
        self.right_side_layout = QVBoxLayout()  # Vertical layout for image
        logo_label = QLabel()  # Label to hold image
        logo_label.setPixmap(self.dcm.logo)  # Set image pixmap
        logo_label.setStyleSheet("border: 3px solid #2D3E50; border-radius: 10px;")  # Add border around image
        self.right_side_layout.addStretch()
        self.right_side_layout.addWidget(logo_label, alignment=Qt.AlignCenter)  # Add image to layout and center
        self.right_side_layout.addStretch()

    def handle_login(self):
        """Checks if the Login is Valid and sets warning messages"""
        username = self.username_input.text().strip()  # Get username
        password = self.password_input.text().strip()  # Get password

        if not username or not password:
            self.login_warning.setText("Please enter both username and password.")
            return

        self.username_input.clear()  # Clear the input fields
        self.password_input.clear()

        if username in self.dcm.users and self.dcm.users[username] == password:
            self.login_warning.setText("")
            self.dcm.page = 2
            self.dcm.user = username
            for mode in range(len(self.dcm.pacemaker_modes)):
                self.dcm.user_data[list(self.dcm.pacemaker_modes)[mode]] = self.dcm.data[username][mode]
            self.dcm.update_modes()
            self.dcm.run_gui()
        else:
            self.login_warning.setText("Incorrect Username or Password")  # Show error message

    def show_register_page(self):
        """Sets Page to Register Page"""
        self.login_warning.setText("")
        self.dcm.page = 1
        self.dcm.run_gui()


class RegisterPage(LoginPage):
    def __init__(self, dcm):
        super().__init__(dcm)

    def left_side(self):
        """Input Side of Register Page"""
        self.left_side_layout = QVBoxLayout()
        title = QLabel("Register")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #2D3E50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)

        # Registration form layout
        register_form = QFormLayout()  # Form layout
        label_username = QLabel("User Name")  # Username label
        label_username.setStyleSheet("font-size: 18px; color: #2D3E50;")  # Label
        self.reg_username_input = QLineEdit()  # Input
        self.reg_username_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #2D3E50; border-radius: 5px;")

        label_password = QLabel("Password")  # Password label
        label_password.setStyleSheet("font-size: 18px; color: #2D3E50;")  # Label
        self.reg_password_input = QLineEdit()  # Input for password
        self.reg_password_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #2D3E50; border-radius: 5px;")
        self.reg_password_input.setEchoMode(QLineEdit.Password)  # Hide 

        label_key = QLabel("Key")  # Key label
        label_key.setStyleSheet("font-size: 18px; color: #2D3E50;")  # Label
        self.reg_key_input = QLineEdit()  # Input for key
        self.reg_key_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #2D3E50; border-radius: 5px;")
        self.reg_key_input.setEchoMode(QLineEdit.Password)  # Hide

        register_form.addRow(label_username, self.reg_username_input)  # Add username row to form
        register_form.addRow(label_password, self.reg_password_input)  # Add password row to form
        register_form.addRow(label_key, self.reg_key_input)  # Add password row to form

        # Register and Back buttons
        register_button = QPushButton("Register")  # Register button
        register_button.setStyleSheet("background-color: #3CB371; color: white; font-size: 18px; font-weight: bold; padding: 10px; border: none; border-radius: 5px;")
        register_button.clicked.connect(self.handle_register)  # Call handle_register method

        back_button = QPushButton("Back")  # Back button 
        back_button.setStyleSheet("background-color: #4682B4; color: white; font-size: 18px; font-weight: bold; padding: 10px; border: none; border-radius: 5px;")
        back_button.clicked.connect(self.show_login_page)  # Call show_login_page method

        # Warning label for registration errors
        self.register_warning = QLabel("")  # Label for warning
        self.register_warning.setStyleSheet("color: red; font-size: 14px;")  # Red
        self.register_warning.setAlignment(Qt.AlignCenter)  # Center

        # Assemble left side layout
        self.left_side_layout.addStretch()  # Top
        self.left_side_layout.addWidget(title)  # Title
        self.left_side_layout.addLayout(register_form)  # Add form
        self.left_side_layout.addWidget(self.register_warning)  # Add warning label
        self.left_side_layout.addWidget(register_button)  # Add register button
        self.left_side_layout.addWidget(back_button)  # Add back button
        self.left_side_layout.addStretch()  # Bottom
        
    def handle_register(self):
        """Checks Username and Key and sets Warning Messages"""
        username = self.reg_username_input.text().strip()  # Get username
        password = self.reg_password_input.text().strip()  # Get password
        key = self.reg_key_input.text().strip()  # Get key

        if not username or not password:
            self.register_warning.setText("Please enter both username and password.")
            return

        if key != self.dcm.key:
            self.register_warning.setText("Incorrect Key")
            return

        if len(self.dcm.users) >= self.dcm.max_users:
            self.register_warning.setText("Maximum users reached")  # Show error message
            return

        if username in self.dcm.users:
            self.register_warning.setText("Username already exists")  # Show error message
        else:
            self.dcm.write_user(username, password, [" ".join(map(str, i)) for i in self.dcm.default_data.values()])  # Add user to file
            self.register_warning.setStyleSheet("color: green;")
            self.register_warning.setText("Registration successful! Please log in.")
            self.reg_username_input.clear()
            self.reg_password_input.clear()
            self.reg_key_input.clear()

    def show_login_page(self):
        """Changes Page to Login Page"""
        self.reg_username_input.clear()
        self.reg_password_input.clear()
        self.reg_key_input.clear()
        self.register_warning.setText("")
        self.dcm.page = 0
        self.dcm.run_gui()
        