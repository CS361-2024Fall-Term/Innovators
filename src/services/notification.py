from datetime import datetime, timedelta

class NotificationService:
    def __init__(self, alert, feedback):
        self.alert = alert
        self.feedback = feedback