# Handles Login and Registration


def handle_login(dcm):
    username, password = dcm.username.text(), dcm.password.text()
    print(username, password)
    if True: #do the check here
        dcm.page = 2
    else:
        dcm.login_warning.setText("In correct Username/Password")
        dcm.page = 0

    dcm.page = 0
