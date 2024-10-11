class User:
    def __init__(self, username, password, phone_number):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.preferences = {}
        self.task = []
        self.events = []
