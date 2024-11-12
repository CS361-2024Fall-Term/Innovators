from datetime import datetime, timedelta

class Event:
    def __init__(self, name, description, start_time, end_time, location):
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location
  

