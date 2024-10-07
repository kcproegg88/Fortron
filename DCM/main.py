from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sys

class LoginApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginApp, self).__init__()
        uic.loadUi("login.ui", self)
        
        # Connect buttons to their respective functions
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)
        
        self.show()

    def login(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        # Load credentials from text file
        try:
            with open("users.txt", "r") as file:
                users = [line.strip().split(",") for line in file.readlines()]
                
            for user, passw in users:
                if user == username and passw == password:
                    QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
                    return
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No registered users. Please register first.")

    def register(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        # Append new credentials to text file
        if username and password:
            with open("users.txt", "a") as file:
                file.write(f"{username},{password}\n")
            QMessageBox.information(self, "Registration Successful", f"User {username} registered successfully!")
        else:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    sys.exit(app.exec_())