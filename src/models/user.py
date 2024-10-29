class User:
    def __init__(self, username, password, phone_number):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.preferences = {}
        self.tasks = []
        self.events = []

    def authentication_password(self, password): 
        return self.password == password
    
    # will work on it later
    def username_available(self, username):
        pass
    
    def change_password(self, old_password, new_password): 
        if self.authentication(old_password):
            self.password = new_password
            return True
        return False
    
    # we need key and value to be able to find the preference and update
    # like {"color" : "Black"}
    def set_preferences(self, key, value):
        self.preferences[key] = value

    # to get the existing preferences
    def get_preferences(self, key, value):
        return self.preferences.get(key, None)
    
    def set_task(self, task):
        self.tasks.append(task)

    def get_task(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None
    
    def set_event(self, event):
        self.tasks.append(event)

    # send a notification for a task
    def set_notification(self, tasks, reminder_time_now):
        tasks.reminder(reminder_time_now)

    def send_a_notification(self):
        print(f"Hey {self.username}, this is a reminder for your {self.task}")

