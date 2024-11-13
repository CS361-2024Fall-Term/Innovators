# calendar class
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

class Cal:
    taskNum = 0
    eventNum = 0

    # Initalizer
    def __init__(self, root, tasks, events):
        self.root = root
        self.frame = tk.Frame(root)
        
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
        
        window_width = int(self.screen_width * 0.8)
        window_height = int(self.screen_height * 0.8)
        
        position_right = int(self.screen_width / 2 - window_width / 2)
        position_down = int(self.screen_height / 2 - window_height / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        self.root.deiconify()

    # Button setup for the calendar
    # Need to add buttons for add tasks and events
    def _setup_widgets(self):
        # Button to save the selected date within `self.frame`
        save_date_button = tk.Button(self.frame, text="Get Date", command=self.save_selected_date, font="Arial 12")
        save_date_button.pack(padx=10, pady=5, anchor='nw')

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

    # Add a new task
    def add_task(self, task):
        # Call task creation
        self.tasks.append(task)
        Cal.taskNum += 1

    # Add a new event
    def add_event(self, event):
        # Call event creation
        self.events.append(event)
        Cal.eventNum += 1

    # Show calendar
    def show(self):
        self.frame.pack(fill="both", expand=True)

    # Hide calendar
    def hide(self):
        self.frame.pack_forget()