# calendar class
import tkinter as tk
import os
import json
import logging
from tkcalendar import Calendar
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from models import tasks, event
from config.preferences import Preferences
from config.profile import Profile

class Cal:
    # Use the getters and setters
    task_num = 0
    event_num = 0

    # Initalizer
    def __init__(self, root, tasks, events, pref, open_preferences, profile, open_profile):
        self.root = root
        self.tasks = tasks if isinstance(tasks, list) else []  # Ensure tasks is a list
        self.events = events if isinstance(events, list) else []  # Ensure events is a list
        self.pref = pref
        self.open_preferences = open_preferences
        self.profile = profile
        self.open_profile = open_profile

        # Main calendar frame
        self.frame = tk.Frame(root)     # bg="lightblue"
        self.frame.pack(side="left", fill="both", expand=True)

        # Retrieve tasks/events from file
        self.load_tasks_from_file()
        self.load_events_from_file()

        # Create and customize the calendar widget within `self.frame`
        self.cal = Calendar(
            self.frame,
            selectmode="day",
            firstweekday="sunday",
            showothermonthdays=False,
            showweeknumbers=False,
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
            daywidth=10,
            dayheight=10
        )
        self.cal.pack(padx=10, pady=10, anchor='nw')
        
        # Set up other UI components in `self.frame`
        self._setup_widgets()
        self.show_date()

    # Button setup for the calendar
    def _setup_widgets(self):
        # Sub-frame for buttons (inside self.frame)
        self.crud_frame = tk.Frame(self.frame)
        self.crud_frame.pack(anchor="nw", padx=5, pady=5)

        # Button frame for search buttons
        self.search_frame = tk.Frame(self.frame)
        self.search_frame.pack(anchor='nw', padx=5, pady=5)

        # Button to create a task
        create_task_button = tk.Button(self.crud_frame, text="Add Task", command=self.open_task_creation_form, font="Arial 12")
        create_task_button.pack(side="left", padx=5)

        # Button to create an event
        create_event_button = tk.Button(self.crud_frame, text="Add Event", command=self.open_event_creation_form, font="Arial 12")
        create_event_button.pack(side="left", padx=5)

        # Button to open preferences
        preferences_button = tk.Button(self.crud_frame, text="Preferences", command=self.open_preferences, font="Arial 12")
        preferences_button.pack(side="left", padx=5)

        # Button to open profile
        profile_button = tk.Button(self.crud_frame, text="Profile", command=self.open_profile, font="Arial 12")
        profile_button.pack(side="left", padx=5)

        # Button to list all tasks/events
        list_button = tk.Button(self.search_frame, text="Get All", command=self.get_all, font="Arial 12")
        list_button.pack(side="left", padx=5)

        # Button to list tasks/events for selected date
        list_button = tk.Button(self.search_frame, text="Search by Date", command=self.filter_by_date, font="Arial 12")
        list_button.pack(side="left", padx=5)

        # Button to list tasks/events for selected category
        list_button = tk.Button(self.search_frame, text="Search by Category", command=self.filter_by_category_helper, font="Arial 12")
        list_button.pack(side="left", padx=5)

        # Button to search for tasks/events by name
        list_button = tk.Button(self.search_frame, text="Search by Name", command=self.search_by_name_helper, font="Arial 12")
        list_button.pack(side="left", padx=5)

        # Overdue Tasks Button
        overdue_tasks = self.check_overdue_tasks()
        if overdue_tasks:
            overdue_button = tk.Button(
                self.crud_frame,
                text="Overdue Tasks",
                command=self.show_overdue_tasks,
                font="Arial 12"
            )
            overdue_button.pack(side="left", padx=5)
    
    def show_tasks(self, window, task_list):
        # Create a canvas and a scrollbar
        container = tk.Frame(window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add a frame inside the canvas
        task_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=task_frame, anchor="nw")

        # Add tasks to the frame
        current_date = datetime.now().date()
        for task in task_list:
            single_task_frame = tk.Frame(task_frame, bd=2, relief="solid")
            single_task_frame.pack(fill="x", padx=10, pady=5)

            # Display task details
            tk.Label(single_task_frame, text=f"Name: {task.name}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(single_task_frame, text=f"Description: {task.description}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(single_task_frame, text=f"Priority: {task.priority}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(single_task_frame, text=f"Category: {task.category}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(single_task_frame, text=f"Start Date: {task.start_date}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(single_task_frame, text=f"Due Date: {task.due_date}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

            # Check if the task is overdue
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
            if due_date < current_date:
                tk.Label(single_task_frame, text="OVERDUE", font=("Arial", 12, "bold"), fg="red").pack(anchor="w", padx=10, pady=5)

            # Edit button for each task
            if due_date > current_date:
                edit_button = tk.Button(single_task_frame, text="Edit", command=lambda task=task: self.edit_task_form(task))
                edit_button.pack(side="right")

            # Delete button for each task
            delete_button = tk.Button(single_task_frame, text="Delete", command=lambda task=task: self.delete_task_check(task))
            delete_button.pack(side="left")

            # Reschedule button for each task only if overdue
            if due_date < current_date:
                reschedule_button = tk.Button(single_task_frame, text="Reschedule", command=lambda task=task: self.reschedule_task(task))
                reschedule_button.pack(side="right")

        # # Make the scrollable area responsive to mouse wheel scrolling
        # def on_mouse_wheel(event):
        #     canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    def show_events(self, window, event_list):
        # Create a canvas and a scrollbar
        container = tk.Frame(window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add a frame inside the canvas
        event_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=event_frame, anchor="nw")
        
        # Add event details inside the scrollable frame
        for event in event_list:
            event_item_frame = tk.Frame(event_frame, bd=2, relief="solid")
            event_item_frame.pack(fill="x", padx=10, pady=5)

            # Display event details
            tk.Label(event_item_frame, text=f"Name: {event.name}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(event_item_frame, text=f"Description: {event.description}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(event_item_frame, text=f"Start Date: {event.start_time}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            tk.Label(event_item_frame, text=f"End Date: {event.end_time}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

            # Edit button for each event
            edit_button = tk.Button(event_item_frame, text="Edit", command=lambda event=event: self.edit_event_form(event))
            edit_button.pack(side="right")

            # Delete button for each event
            delete_button = tk.Button(event_item_frame, text="Delete", command=lambda event=event: self.delete_event_check(event))
            delete_button.pack(side="left")
        
        # # Make the scrollable area responsive to mouse wheel scrolling
        # def on_mouse_wheel(event):
        #     canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Show current date
    def show_date(self):
        current_date = datetime.now().strftime("%m/%d/%y %H:%M:%S")
        # self.date_label.config(text=f"Current Date: {current_date}")

    def filter_by_category_helper(self):
        # Need to create a window that has a single select
        retrieve_category = tk.Toplevel(self.root)
        retrieve_category.title("Select Category")

        # Entry Field
        tk.Label(retrieve_category, text="Category (School, Work, Personal, Other):").pack()
        category_entry = ttk.Combobox(retrieve_category, values=["School", "Work", "Personal", "Other"])
        category_entry.set("School")  # Set a default value
        category_entry.pack()

        # Submit button
        submit_button = tk.Button(retrieve_category, text="Filter", 
                                command=lambda: self.filter_by_category(
                                    retrieve_category,
                                    category_entry.get()
                                    ))
        submit_button.pack() 

    def search_by_name_helper(self):
        # Need to create a window that has a single select
        get_name = tk.Toplevel(self.root)
        get_name.title("Enter name")

        # Entry Field
        tk.Label(get_name, text="Name:").pack()
        name_entry = tk.Entry(get_name)
        name_entry.pack()

        # Submit button
        submit_button = tk.Button(get_name, text="Search", 
                                command=lambda: self.search_by_name(
                                    get_name,
                                    name_entry.get()
                                    ))
        submit_button.pack() 

    # Filter by task category
    def get_all(self):
        self.load_tasks_from_file()

        # Pop up a new window 
        task_window = tk.Toplevel(self.root)
        task_window.title("All Tasks/Events")

        day_tasks = [task for task in self.tasks]
        day_events = [event for event in self.events]

        # Add a frame for each task
        if day_tasks:
            tk.Label(task_window, text="Tasks:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_tasks(task_window, day_tasks)
        else:
            tk.Label(task_window, text="No tasks.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        # Add a frame for each event
        if day_events:
            tk.Label(task_window, text="Events:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_events(task_window, day_events)
        else:
            tk.Label(task_window, text="No events.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

    # Filter by task category
    def filter_by_category(self, retrieve_category, selected_category):
        self.load_tasks_from_file()
        retrieve_category.destroy()

        # Pop up a new window 
        task_window = tk.Toplevel(self.root)
        task_window.title(selected_category + " Related Tasks:")


        day_tasks = [
            task for task in self.tasks 
                if task.category == selected_category
        ]

        # Add a frame for each task
        if day_tasks:
            tk.Label(task_window, text="Tasks:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_tasks(task_window, day_tasks)
        else:
            tk.Label(task_window, text="No tasks for this category.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

    #logic behind search by name
    def search_by_name(self, get_name, name_entry):
        self.load_tasks_from_file()
        self.load_events_from_file()
        get_name.destroy()

        # Pop up a new window 
        task_window = tk.Toplevel(self.root)
        task_window.title(name_entry)

        # Add Tasks and Events to the lists based on if they have the correct name
        matching_tasks = []
        for task in self.tasks:
            if (task.name == name_entry):
                matching_tasks.append(task)
            
        matching_events = []
        for event in self.events:
            if (event.name == name_entry):
                matching_events.append(event)

        # Add a frame for each task
        if matching_tasks:
            tk.Label(task_window, text="Tasks:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_tasks(task_window, matching_tasks)
        else:
            tk.Label(task_window, text="No tasks with this name.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        # Add a frame for each event
        if matching_events:
            tk.Label(task_window, text="Events:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_events(task_window, matching_events)
        else:
            tk.Label(task_window, text="No events with this name.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)


    def filter_by_date(self):
        self.load_tasks_from_file()
        selected_date = self.cal.get_date()

        # Pop up a new window 
        task_window = tk.Toplevel(self.root)
        task_window.title(selected_date)

        # Convert selected_date from calendar to correct format
        target_date = datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")
        target_date = datetime.strptime(target_date, "%Y-%m-%d")

        # Add Tasks and Events to the lists based on if they are in the range
        day_tasks = []
        for task in self.tasks:
            start_date = datetime.strptime(task.start_date, "%Y-%m-%d")
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
            if (start_date <= target_date <= due_date):
                day_tasks.append(task)
            
        day_events = []
        for event in self.events:
            start_time = datetime.strptime(event.start_time, "%Y-%m-%d")
            end_time = datetime.strptime(event.end_time, "%Y-%m-%d")
            if (start_time <= target_date <= end_time):
                day_events.append(event)

        # Add a frame for each task
        if day_tasks:
            tk.Label(task_window, text="Tasks:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_tasks(task_window, day_tasks)
        else:
            tk.Label(task_window, text="No tasks for this date.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        # Add a frame for each event
        if day_events:
            tk.Label(task_window, text="Events:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            self.show_events(task_window, day_events)
        else:
            tk.Label(task_window, text="No events for this date.", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

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

        tk.Label(task_window, text="Category (School, Work, Personal, Other):").pack()
        category_entry = ttk.Combobox(task_window, values=["School", "Work", "Personal", "Other"])
        category_entry.set("School")  # Set a default value
        category_entry.pack()

        tk.Label(task_window, text="Start Date (YYYY-MM-DD):").pack()
        start_date_entry = tk.Entry(task_window)
        start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # default start date is today's date
        start_date_entry.pack()

        tk.Label(task_window, text="Due Date (YYYY-MM-DD):").pack()
        due_date_entry = tk.Entry(task_window)
        due_date_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')) # default due date if after 24 hours?
        due_date_entry.pack()

        # tk.Label(task_window, text="Start Time (HH-MM):").pack()
        # start_date_entry = tk.Entry(task_window)
        # start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M')) # default start date is today's date
        # start_date_entry.pack()

        # tk.Label(task_window, text="Due Time (HH-MM):").pack()
        # due_date_entry = tk.Entry(task_window)
        # due_date_entry.insert(0, (datetime.now()).strftime('%Y-%m-%d %H:%M')) # default due date if after 24 hours?
        # due_date_entry.pack()

        # Submit button
        submit_button = tk.Button(task_window, text="Add Task", 
                                command=lambda: self.add_task(
                                    name_entry.get(),
                                    description_entry.get(),
                                    priority_entry.get(),
                                    category_entry.get(),
                                    start_date_entry.get(),
                                    due_date_entry.get(),
                                    task_window
                                ))
        submit_button.pack()
        
        # Increase number of tasks
        Cal.task_num += 1

    def edit_task_form(self, task):
        # Pop up a new window for task input
        task_window = tk.Toplevel(self.root)
        task_window.title("Edit Task")

        #pre-populated entry fields with existing task/event info
        tk.Label(task_window, text="Task Name:").pack()
        name_entry = tk.Entry(task_window)
        name_entry.pack()
        name_entry.insert(0, task.name)

        tk.Label(task_window, text="Description:").pack()
        description_entry = tk.Entry(task_window)
        description_entry.pack()
        description_entry.insert(0, task.description)

        tk.Label(task_window, text="Priority (High, Medium, Low):").pack()
        priority_entry = ttk.Combobox(task_window, values=["High", "Medium", "Low"])
        priority_entry.set(task.priority)  
        priority_entry.pack()

        # Removed the time aspect of these 
        tk.Label(task_window, text="Start Date (YYYY-MM-DD):").pack()
        start_date_entry = tk.Entry(task_window)
        # start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # default start date is today's date
        start_date_entry.pack()
        start_date_entry.insert(0, task.start_date)

        tk.Label(task_window, text="Due Date (YYYY-MM-DD):").pack()
        due_date_entry = tk.Entry(task_window)
        # due_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # default start date is today's date
        due_date_entry.pack()
        due_date_entry.insert(0, task.due_date)

        # Submit button
        submit_button = tk.Button(task_window, text="Submit", 
                                command=lambda: self.edit_task(
                                    task, 
                                    name_entry.get(),
                                    description_entry.get(),
                                    priority_entry.get(),
                                    start_date_entry.get(),
                                    due_date_entry.get(),
                                    task_window
                                ))
        submit_button.pack()
    
    def delete_event_check(self, e):
        # Pop up a new window for check
        window = tk.Toplevel(self.root)
        window.title("Confirmation")

        tk.Label(window,text = "Are you sure you want to delete this event?").pack()

        yes_button = tk.Button(window, text="Yes", command=lambda: self.delete_event(window, e))
        yes_button.pack(side="left")

        no_button = tk.Button(window, text="No", command=lambda: window.destroy())
        no_button.pack(side="right")

    def delete_task_check(self, t):
        # Pop up a new window for check
        window = tk.Toplevel(self.root)
        window.title("Confirmation")

        tk.Label(window,text = "Are you sure you want to delete this task?").pack()

        yes_button = tk.Button(window, text="Yes", command=lambda: self.delete_task(window, t))
        yes_button.pack(side="left")

        no_button = tk.Button(window, text="No", command=lambda: window.destroy())
        no_button.pack(side="right")

    def edit_task_date(self, task, window, start_date, due_date):
        task.set_start_date(start_date)
        task.set_due_date(due_date)

        self.save_tasks_to_file()

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.tasks = self.tasks # Update daily overview
            self.daily_overview.update_overview()

        # Refresh the calendar
        self.show_date() 

        window.destroy()

    def reschedule_task(self, task):
        # Open a new window to update the date of the task
        window = tk.Toplevel(self.root)
        window.title("Reschedule " + task.name)

        tk.Label(window, text="Start Date (YYYY-MM-DD):").pack()
        start_date_entry = tk.Entry(window)
        start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # default start date is today's date
        start_date_entry.pack()

        tk.Label(window, text="Due Date (YYYY-MM-DD):").pack()
        due_date_entry = tk.Entry(window)
        due_date_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')) # default due date if after 24 hours?
        due_date_entry.pack()

        back_button = tk.Button(window, text="Back", command=lambda: window.destroy())
        back_button.pack(side="left")

        confirm_button = tk.Button(window, text="Confirm", command=lambda: self.edit_task_date(task, window, start_date_entry.get(), due_date_entry.get()))
        confirm_button.pack(side="right")

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
        start_time_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # default start date is today's date
        start_time_entry.pack()

        tk.Label(event_window, text="End Time (YYYY-MM-DD):").pack()
        end_time_entry = tk.Entry(event_window)
        end_time_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')) # default start date is today's date
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

    def edit_event_form(self, e):
        # Pop up a new window for task input
        event_window = tk.Toplevel(self.root)
        event_window.title("Edit Event")

        #pre-populated entry fields with existing task/event info
        tk.Label(event_window, text="Event Name:").pack()
        name_entry = tk.Entry(event_window)
        name_entry.pack()
        name_entry.insert(0, e.name)

        tk.Label(event_window, text="Description:").pack()
        description_entry = tk.Entry(event_window)
        description_entry.pack()
        description_entry.insert(0, e.description)


        tk.Label(event_window, text="Start Time (YYYY-MM-DD):").pack()
        start_time_entry = tk.Entry(event_window)
        #start_time_entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M')) # default start date is today's date
        start_time_entry.pack()
        start_time_entry.insert(0, e.start_time)

        tk.Label(event_window, text="End Time (YYYY-MM-DD):").pack()
        end_time_entry = tk.Entry(event_window)
        #end_time_entry.insert(0, datetime.now().strftime('%Y-%m-%d 23:59')) # default start date is today's date
        end_time_entry.pack()
        end_time_entry.insert(0, e.end_time)

        tk.Label(event_window, text="Location:").pack()
        location_entry = tk.Entry(event_window)
        location_entry.pack()
        location_entry.insert(0, e.location)

        # Submit button
        submit_button = tk.Button(event_window, text="Submit", 
                                command=lambda: self.edit_event(
                                    e, 
                                    name_entry.get(),
                                    description_entry.get(),
                                    start_time_entry.get(),
                                    end_time_entry.get(),
                                    location_entry.get(),
                                    event_window
                                ))
        submit_button.pack()


    def add_task(self, name, description, priority, category, start_date, due_date, task_window):
        num = len(self.tasks)
        # Create task object
        new_task = tasks.Tasks(name, description, priority, None, None, category, start_date, due_date, "not started", "N/A")

        # Add the new task to the tasks
        if (num == 0):
            self.tasks.append(new_task)
        else:
            match new_task.priority:
                case "Low":
                    self.tasks.append(new_task)
                case "Medium":
                    if self.tasks[0].priority != "High":
                        self.tasks.insert(0, new_task)
                    else:
                        ins = False
                        for i in range (num):
                            if self.tasks[i].priority != "High":
                                self.tasks.insert(i, new_task)
                                ins = True
                                break
                        if (ins == False):
                            self.tasks.append(new_task)
                case "High":
                    self.tasks.insert(0, new_task)

        # Save the task to JSON file (to be able to retrieve it later)
        self.save_tasks_to_file()

        # Informing the user of the succeess 
        print(f"Task '{name}' added with start date {start_date} and due date {due_date}.")

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.tasks = self.tasks # Update daily overview
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
            self.daily_overview.events = self.events # Update daily overview
            self.daily_overview.update_overview()

        # Refresh the calendar display
        self.show_date()

        # Close the creation window
        event_window.destroy()

    def edit_task(self, task, name, description, priority, start_date, due_date, task_window):
        num = len(self.tasks)

        if (task.priority != priority):
            sort_task = tasks.Tasks(name, description, priority, task.reminder, task.repetitiveness, task.category, start_date, due_date, task.status, task.location)
            self.tasks.remove(task)
            # Sort the new task to the tasks
            match sort_task.priority:
                case "Low":
                    self.tasks.append(sort_task)
                case "Medium":
                    if self.tasks[0].priority != "High":
                        self.tasks.insert(0, sort_task)
                    else:
                        ins = False
                        for i in range (num):
                            if self.tasks[i].priority != "High":
                                self.tasks.insert(i, sort_task)
                                ins = True
                                break
                        if (ins == False):
                            self.tasks.append(sort_task)
                case "High":
                    self.tasks.insert(0, sort_task)
        else:
            task.set_name(name)
            task.set_description(description)
            task.set_priority(priority)
            task.set_start_date(start_date)
            task.set_due_date(due_date)

        self.save_tasks_to_file()

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.tasks = self.tasks # Update daily overview
            self.daily_overview.update_overview()

        # Refresh the calendar
        self.show_date() 

        # At the end, close the window
        task_window.destroy()

    def edit_event(self, e, name, description, start_time, end_time, location, task_window):
        e.set_name(name)
        e.set_description(description)
        e.start_time = start_time
        e.end_time = end_time
        e.set_location(location)

        self.save_events_to_file()

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.events = self.events # Update daily overview
            self.daily_overview.update_overview()

        # Refresh the calendar
        self.show_date() 

        # At the end, close the window
        task_window.destroy()

    

    def delete_event(self, window, event):

        #delete the event
        print(f"Deleteing event with name '{event.name}'.")
        self.events.remove(event)
        Cal.event_num -= 1 

        # Save the events to JSON file (to be able to retrieve it later)
        self.save_events_to_file()

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.events = self.events # Update daily overview
            self.daily_overview.update_overview()

        # Refresh the calendar
        self.show_date() 

        # At the end, close the window
        window.destroy()

    def delete_task(self, window, task):

        #delete the task
        print(f"Deleteing task with name '{task.name}'.")
        self.tasks.remove(task)
        Cal.task_num -= 1 

        # Save the task to JSON file (to be able to retrieve it later)
        self.save_tasks_to_file()

        # Refresh the daily overview
        if hasattr(self, "daily_overview"):
            self.daily_overview.tasks = self.tasks # Update daily overview
            self.daily_overview.update_overview()

        # Refresh the calendar
        self.show_date()

        # At the end, close the window
        window.destroy()

    def save_tasks_to_file(self, filename="./src/tasks.json"):
        # Save all tasks to a JSON file
        # Convert each task to a dictionary
        tasks_data = [task.__dict__ for task in self.tasks]
        
        # Write data to a JSON file
        with open(filename, 'w') as f:
            json.dump(tasks_data, f)
        print(f"Tasks saved to file: {filename}")

    def load_tasks_from_file(self, filename="src/tasks.json"):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, 'r') as f:
                tasks_data = json.load(f)

            # Convert each dictionary back to a Tasks object
            self.tasks = [tasks.Tasks(**task_data) for task_data in tasks_data]  # Replace with your actual Tasks class
            self.set_task_num(len(self.tasks))
            print(f"{len(self.tasks)} tasks loaded from file.")
            #self.daily_overview.update_overview()
        except FileNotFoundError:
            print(f"File '{filename}' not found. Creating a new file.")
            self.tasks = []
            self.save_tasks_to_file(filename)  # Create the file with an empty list
        except json.JSONDecodeError:
            print(f"The file '{filename}' contains invalid JSON. Starting with an empty list.")
            self.tasks = []
            self.save_tasks_to_file(filename)

    def save_events_to_file(self, filename="./src/events.json"):
        # Save all events to a JSON file
        # Convert each event to a dictionary
        events_data = [event.__dict__ for event in self.events]
        
        # Write data to a JSON file
        with open(filename, 'w') as f:
            json.dump(events_data, f)
        print(f"Events saved to file: {filename}")

    def load_events_from_file(self, filename="src/events.json"):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, 'r') as f:
                events_data = json.load(f)

            # Convert each dictionary back to an Event object
            self.events = [event.Event(**event_data) for event_data in events_data]  # Replace with your actual Event class
            self.set_event_num(len(self.events))
            print(f"{len(self.events)} events loaded from file.")
            #self.daily_overview.update_overview()
        except FileNotFoundError:
            print(f"File '{filename}' not found. Creating a new file.")
            self.events = []
            self.save_events_to_file(filename)  # Create the file with an empty list
        except json.JSONDecodeError:
            print(f"The file '{filename}' contains invalid JSON. Starting with an empty list.")
            self.events = []
            self.save_events_to_file(filename)

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
        self.frame.pack(side="left", fill="both", expand=True)

    # Hide calendar
    def hide(self):
        self.frame.pack_forget()

    # Reminder
    def reminder_for_events(self):
        self.load_events_from_file()
        self.load_tasks_from_file()
        now = datetime.now()

        for event in self.events:
            try:
                end_time = datetime.strptime(event.end_time, "%Y-%m-%d %H:%M")
                time_difference = (end_time - now).total_seconds()

                if 0 <= time_difference <= 600:  # check if there is an event within 10 minutes
                    message = f"Reminder: Event '{event.name}' starts in 10 minutes!, HURRY UP, LOSER"
                    logging.info(message)
                    messagebox.showinfo("Event Reminder", message)
            except ValueError as e:
                logging.error(f"ERROR parsing event end time: {e}")
        for task in self.tasks:
            try:
                due_date = datetime.strptime(task.due_date, "%Y-%m-%d %H:%M")
                time_difference = (due_date - now).total_seconds()

                if 0 <= time_difference <= 600:  # check if there is a task within 10 minutes
                    message = f"Reminder: Task '{task.name}' starts in 10 minutes!, HURRY UP, LOSER"
                    logging.info(message)
                    messagebox.showinfo("Event Reminder", message)
            except ValueError as e:
                logging.error(f"ERROR parsing task due date: {e}")


    def check_overdue_tasks(self):
        current_date = datetime.now().date()
        overdue_tasks = [
            task for task in self.tasks
            if datetime.strptime(task.due_date, '%Y-%m-%d').date() < current_date
        ]
        return overdue_tasks
    
    def show_overdue_tasks(self):
        overdue_tasks = self.check_overdue_tasks()
        if overdue_tasks:
            # Create a new window for overdue tasks
            task_window = tk.Toplevel(self.root)
            task_window.title("Overdue Tasks")

            # Add a title label
            tk.Label(task_window, text="Overdue Tasks:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

            # Display each overdue task in a frame
            for task in overdue_tasks:
                task_frame = tk.Frame(task_window, bd=2, relief="solid")
                task_frame.pack(fill="x", padx=10, pady=5)

                tk.Label(task_frame, text=f"Name: {task.name}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
                tk.Label(task_frame, text=f"Description: {task.description}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
                tk.Label(task_frame, text=f"Priority: {task.priority}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
                tk.Label(task_frame, text=f"Category: {task.category}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
                tk.Label(task_frame, text=f"Start Date: {task.start_date}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
                tk.Label(task_frame, text=f"Due Date: {task.due_date}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)

                # Add "OVERDUE" label
                tk.Label(task_frame, text="OVERDUE", font=("Arial", 12, "bold"), fg="red").pack(anchor="w", padx=10, pady=2)

                # Add edit and delete buttons for each task
                tk.Button(task_frame, text="Edit", command=lambda t=task: self.edit_task_form(t)).pack(side="left", padx=5)
                tk.Button(task_frame, text="Delete", command=lambda t=task: self.delete_task_check(t)).pack(side="right", padx=5)

        else:
            # If no overdue tasks, show a message
            tk.Label(self.root, text="No overdue tasks!", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)


