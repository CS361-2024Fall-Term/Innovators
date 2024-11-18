# calendar class
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
from datetime import datetime
from models import tasks, event
import json

class Cal:
    # Use the getters and setters
    task_num = 0
    event_num = 0

    # Initalizer
    def __init__(self, root, tasks, events):
        self.root = root
        self.tasks = tasks if isinstance(tasks, list) else []  # Ensure tasks is a list
        self.events = events
        self.frame = tk.Frame(root)

        # Retrieve tasks/events from file
        self.load_tasks_from_file()
        self.load_events_from_file()
        
        # Set up device screen size
        self.screen_width, self.screen_height = self._get_screen_size()
        self._set_window_size()

        # Calendar padding sizes
        padx_percent = 0.015
        pady_percent = 0.019
        padx = int(self.screen_width * padx_percent)
        pady = int(self.screen_height * pady_percent)

        # Create and customize the calendar widget within `self.frame`
        self.cal = Calendar(
            self.frame,
            selectmode="day",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            font="Arial 14",
            background="lightblue",
            foreground="black",
            selectbackground="darkblue",
            selectforeground="white",
            headersbackground="lightgray",
            headersforeground="black",
            daywidth=5,
            dayheight=5
        )
        self.cal.pack(padx=padx, pady=pady, anchor='nw')
        
        # Set up other UI components in `self.frame`
        self._setup_widgets()
        self.show_date()

    # Helper function for the
    def _get_screen_size(self):
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    # Window sizing
    def _set_window_size(self):
        # Center the window
        self.root.withdraw()
        
        window_width = int(self.screen_width * 0.5)
        window_height = int(self.screen_height * 0.5)
        
        position_right = int(self.screen_width / 2 - window_width / 2)
        position_down = int(self.screen_height / 2 - window_height / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        self.root.deiconify()

    # Button setup for the calendar
    def _setup_widgets(self):
        # Button to save the selected date within `self.frame`
        save_date_button = tk.Button(self.frame, text="Get Date", command=self.save_selected_date, font="Arial 12")
        save_date_button.pack(padx=10, pady=5, anchor='nw')

        create_task_button = tk.Button(self.frame, text="Add Task", command=self.open_task_creation_form, font="Arial 12")
        create_task_button.pack(padx=10, pady=5, anchor='nw')

        create_event_button = tk.Button(self.frame, text="Add Event", command=self.open_event_creation_form, font="Arial 12")
        create_event_button.pack(padx=10, pady=5, anchor='nw')

        self.selected_date_label = tk.Label(self.frame, text="Date:", font="Arial 12 bold")
        self.selected_date_label.pack(padx=10, pady=5, anchor='nw')

        self.date_label = tk.Label(self.frame, text="", font="Arial 12 bold")
        self.date_label.pack(padx=10, pady=5, anchor='nw')

    # Show current date
    def show_date(self):
        current_date = datetime.now().strftime("%m/%d/%y")
        self.date_label.config(text=f"Current Date: {current_date}")

    # Example for date selection
    def save_selected_date(self):
        selected_date = self.cal.get_date()
        self.selected_date_label.config(text=f"Date: {selected_date}")

    def open_task_creation_form(self):
        # Pop up a new window for task input
        task_window = tk.Toplevel(self.root)
        task_window.title("Create New Task")

        # Task input fields
        tk.Label(task_window, text="Task Name:").pack()
        name_entry = tk.Entry(task_window)
        name_entry.pack()

        tk.Label(task_window, text="Description:").pack()
        description_entry = tk.Entry(task_window)
        description_entry.pack()

        tk.Label(task_window, text="Priority (High, Medium, Low):").pack()
        priority_entry = ttk.Combobox(task_window, values=["High", "Medium", "Low"])
        priority_entry.set("Medium")  # Set a default value
        priority_entry.pack()

        tk.Label(task_window, text="Start Date (YYYY-MM-DD):").pack()
        start_date_entry = tk.Entry(task_window)
        start_date_entry.pack()

        tk.Label(task_window, text="Due Date (YYYY-MM-DD):").pack()
        due_date_entry = tk.Entry(task_window)
        due_date_entry.pack()

        # Submit button
        submit_button = tk.Button(task_window, text="Add Task", 
                                command=lambda: self.add_task(
                                    name_entry.get(),
                                    description_entry.get(),
                                    priority_entry.get(),
                                    start_date_entry.get(),
                                    due_date_entry.get(),
                                    task_window
                                ))
        submit_button.pack()
        
        # Increase number of tasks
        Cal.task_num += 1

    def open_event_creation_form(self):
        # Pop up a new window for task input
        event_window = tk.Toplevel(self.root)
        event_window.title("Create New Event")

        # Event input fields
        tk.Label(event_window, text="Event Name:").pack()
        name_entry = tk.Entry(event_window)
        name_entry.pack()

        tk.Label(event_window, text="Description:").pack()
        description_entry = tk.Entry(event_window)
        description_entry.pack()

        tk.Label(event_window, text="Start Time (YYYY-MM-DD):").pack()
        start_time_entry = tk.Entry(event_window)
        start_time_entry.pack()

        tk.Label(event_window, text="End Time (YYYY-MM-DD):").pack()
        end_time_entry = tk.Entry(event_window)
        end_time_entry.pack()

        tk.Label(event_window, text="Location").pack()
        location_entry = tk.Entry(event_window)
        location_entry.pack()

        # Submit button
        submit_button = tk.Button(event_window, text="Add Event", 
                                command=lambda: self.add_event(
                                    name_entry.get(),
                                    description_entry.get(),
                                    start_time_entry.get(),
                                    end_time_entry.get(),
                                    location_entry.get(),
                                    event_window
                                ))
        submit_button.pack()
        
        Cal.event_num += 1

    def add_task(self, name, description, priority, start_date, due_date, task_window):
        # Create task object
        new_task = tasks.Tasks(name, description, priority, None, None, "General", start_date, due_date, "not started", "N/A")

        # Add the new task to the tasks
        self.tasks.append(new_task) 

        # Save the task to JSON file (to be able to retrieve it later)
        self.save_tasks_to_file()

        # Informing the user of the succeess 
        print(f"Task '{name}' added with start date {start_date} and due date {due_date}.")

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.update_overview()

        # Refresh the calendar
        self.show_date() 

        # At the end, close the window
        task_window.destroy()

    def add_event(self, name, description, start_time, end_time, location, event_window):
        # Create event object
        new_event = event.Event(name, description, start_time, end_time, location)

        # Add the new event to the events
        self.events.append(new_event)

        # Save the events to the JSON file to save data
        self.save_events_to_file()

        # Inform the user of the success
        print(f"Event '{name}' added with start time {start_time} and end time {end_time}.")

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.update_overview()

        # Refresh the calendar display
        self.show_date()

        # Close the creation window
        event_window.destroy()


    def save_tasks_to_file(self, filename="src/tasks.json"):
        # Save all tasks to a JSON file
        # Convert each task to a dictionary
        tasks_data = [task.__dict__ for task in self.tasks]
        
        # Write data to a JSON file
        with open(filename, 'w') as f:
            json.dump(tasks_data, f)
        print("Tasks saved to file: {filename}")

    def load_tasks_from_file(self, filename="src/tasks.json"):
        # Load tasks from a JSON file
        try:
            with open(filename, 'r') as f:
                tasks_data = json.load(f)
            
            # Convert each dictionary back to a Tasks object
            self.tasks = [tasks.Tasks(**task_data) for task_data in tasks_data]  # Corrected here
            self.set_task_num(len(self.tasks))
            print(f"{len(self.tasks)} tasks loaded from file.")
        except FileNotFoundError:
            print("No saved tasks file found; starting with an empty list.")
            self.events = []
        except json.JSONDecodeError:
            print("The file contains invalid JSON. Starting with an empty list.")
            self.events = []

    def save_events_to_file(self, filename="src/events.json"):
        # Save all events to a JSON file
        # Convert each event to a dictionary
        events_data = [event.__dict__ for event in self.events]
        
        # Write data to a JSON file
        with open(filename, 'w') as f:
            json.dump(events_data, f)
        print("Events saved to file: {filename}")

    def load_events_from_file(self, filename="src/events.json"):
        # Load events from a JSON file
        try:
            with open(filename, 'r') as f:
                events_data = json.load(f)
            
            # Convert each dictionary back to a Events object
            self.events = [event.Event(**event_data) for event_data in events_data]  # Corrected here
            self.set_event_num(len(self.events))
            print(f"{len(self.events)} events loaded from file.")
        except FileNotFoundError:
            print("No saved events file found; starting with an empty list.")
            self.events = []
        except json.JSONDecodeError:
            print("The file contains invalid JSON. Starting with an empty list.")
            self.events = []

    def get_task_num(self):
        return self.task_num

    def get_event_num(self):
        return self.event_num
    
    def set_task_num(self, new_task_num):
        self.task_num = new_task_num

    def set_event_num(self, new_event_num):
        self.event_num = new_event_num

    # Show calendar
    def show(self):
        self.frame.pack(fill="both", expand=True)

    # Hide calendar
    def hide(self):
        self.frame.pack_forget()
