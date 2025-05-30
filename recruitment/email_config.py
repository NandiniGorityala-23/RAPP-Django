class EmailConfig():
    '''For accessing default email settings data from database'''

    def __init__(self):
        self.EMAIL_HOST = 'smtp.gmail.com'
        self.EMAIL_HOST_USER = 'recruitmentapp'
        self.EMAIL_HOST_PASSWORD = 'msys@123'
        self.EMAIL_PORT = 587
        self.FROM_MAIL = 'recruitementapp@gmail.com'
        self.ENABLE_AUTHENTICATION = True
        self.USE_SSL_TL = True


if __name__ == '__main__':
    pass