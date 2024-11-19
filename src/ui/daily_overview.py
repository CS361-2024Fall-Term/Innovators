import tkinter as tk
from datetime import datetime

class DailyOverview:
    def __init__(self, root, tasks, events):
        # Initialization of Daily Overview class

        self.root = root
        self.tasks = tasks
        self.events = events

        # Set the frame for daily overview
        self.frame = tk.Frame(root)
        self.frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Add a label to display today's overview
        self.title_label = tk.Label(self.frame, text="Today's Overview", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=5)

        # Create a text box for displaying tasks and events
        self.text_box = tk.Text(self.frame, height=20, width=40, state="disabled", font=("Arial", 12))
        self.text_box.pack(padx=5, pady=5)

        # Load today's tasks and events
        self.update_overview()

    # Update the daily overview with tasks and events for the current date
    def update_overview(self):

        # Det today's date in YYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")

        # FIlter tasks and events for today
        today_tasks = [task for task in self.tasks if task.start_date == task.due_date == today]
        today_events = [event for revent in self.events if event.start_time.startswith(today)]

        # Prepare the overview text
        overview_text = f"Date: {today}\n\n"

        if today_tasks:
            overview_text += "Tasks:\n"
            for task in today_tasks:
                overview_text += f"- {task.name}: {task.description} (Priority: {task.priority})\n"
        else:
            overview_text += "\n"

        if today_events:
            overview_text += "Events:\n"
            for event in today_events:
                    overview_text += f"- {event.name}: {event.description} (Location: {event.location})\n"
        else:
            overview_text += "No events for today.\n"


        # Update the text box
        self.text_box.config(state="normal")
        self.text_box.delete(1.0, "end")
        self.text_box.insert("end", overview_text)
        self.text_box.config(state="disabled")

    
    # Show the daily overview
    def show(self):
        self.frame.pack(fill="both", expand=True)

    # Hide the daily overview
    def hide(self):
        self.frame.pack_forget()
