class Tasks:
    def __init__(self, name, description, priority, reminder, repetitiveness, category, start_date, due_date, status, location):
        self.name = name
        self.description = description
        self.priority = priority
        self.reminder = reminder
        self.repetitiveness = repetitiveness
        self.category = category
        self.start_date = start_date
        self.due_date = due_date
        self.status = status
        self.location = location

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_priority(self, priority):
        self.priority = priority

    def set_reminder(self, reminder):
        self.reminder = reminder

    def set_repetitiveness(self, repetitiveness):
        self.repetitiveness = repetitiveness 
    
    def set_status(self, status):
        self.status = status

    def status_completed(self):
        self.status = "completed"

    def status_in_progress(self):
        self.status = "in progress"

    def status_not_started(self):
        self.status = "not started"

    def status_deleted(self):
        self.status = "deleted"

    def set_locaiton(self, location):
        self.location = location

    