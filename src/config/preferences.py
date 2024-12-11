import tkinter as tk
import os
import json
from tkinter import ttk


class Preferences:
    def __init__(self, root, continue_to_calendar):
        self.load_from_file()
        self.continue_to_calendar = continue_to_calendar
        #Preferences Frame
        self.frame = tk.Frame(root) 
        self.show()
        #Retrieve preferences from json
        self._setup_widgets()


    def save_to_file(self, filename):
        
        # Write data to a JSON file
        pref_dict = {
            "font_size" : self.font_size,
            "color_theme" : self.color_theme,
            "notifications" : self.notifications,
            "reminders" : self.reminders,
            "reminder_time" : self.reminder_time,
            "school_category_color" : self.school_category_color,
            "work_category_color" : self.work_category_color,
            "personal_category_color" : self.personal_category_color
        }
        with open(filename, 'w') as f:
            json.dump(pref_dict, f)
        print(f"Tasks saved to file: {filename}")

    def color(self, category):
        match category:
            case "School":
                return self.school_category_color
            case "Work":
                return self.work_category_color
            case "Personal":
                return self.personal_category_color
            case _:
                return "black"

    # def __del__(self):
    #     self.save_to_file("src/config/preferences.json")

    def load_from_file(self, filename="./config/preferences.json"):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Convert each dictionary back to a Tasks object
            self.font_size = data["font_size"]
            self.color_theme = data["color_theme"]
            self.notifications = data["notifications"]
            self.reminders = data["reminders"]
            self.reminder_time = data["reminder_time"]
            self.school_category_color = data["school_category_color"]
            self.work_category_color = data["work_category_color"]
            self.personal_category_color = data["personal_category_color"]
        except FileNotFoundError:
            self.font_size = 13
            self.color_theme = "blue"
            self.notifications = False
            self.reminders = False
            self.reminder_time = 13,
            self.school_category_color = "green",
            self.work_category_color = "purple" ,
            self.personal_category_color = "yellow",
            # print(f"File '{filename}' not found. Creating a new file.")
            self.save_to_file(filename)  # Create the file with an empty list
        except json.JSONDecodeError:
            print(f"The file '{filename}' contains invalid JSON. Starting with an empty list.")


    def _setup_widgets(self):
        # Preferences input fields

        #font_size
        self.font_label = tk.Label(self.frame, text="Font_Size")
        self.font_size_entry = tk.Entry(self.frame)
        self.font_size_entry.insert(0, str(self.font_size))
        self.font_label.pack()
        self.font_size_entry.pack()

        self.color_theme_label = tk.Label(self.frame, text="Color_Theme")
        self.color_theme_entry = tk.Entry(self.frame)
        self.color_theme_entry.insert(0, str(self.color_theme))
        self.color_theme_label.pack()
        self.color_theme_entry.pack()

        self.notifications_label = tk.Label(self.frame, text="notifications")
        self.notifications_entry = tk.Entry(self.frame)
        self.notifications_entry.insert(0, str(self.notifications))
        self.notifications_label.pack()
        self.notifications_entry.pack()

        self.reminders_label = tk.Label(self.frame, text="reminders")
        self.reminders_entry = tk.Entry(self.frame)
        self.reminders_entry.insert(0, str(self.reminders))
        self.reminders_label.pack()
        self.reminders_entry.pack()

        self.reminder_time_label = tk.Label(self.frame, text="reminder_time")
        self.reminder_time_entry = tk.Entry(self.frame)
        self.reminder_time_entry.insert(0, str(self.reminder_time))
        self.reminder_time_label.pack()
        self.reminder_time_entry.pack()

        # Entry Field
        tk.Label(self.frame, text="School Category Color").pack()
        self.school_category_color_entry = ttk.Combobox(self.frame, values=["red", "blue", "green", "yellow", "orange"])
        self.school_category_color_entry.set(self.school_category_color)  # Set a default value
        self.school_category_color_entry.pack()
        
        # Entry Field
        tk.Label(self.frame, text="Work Category Color").pack()
        self.work_category_color_entry = ttk.Combobox(self.frame, values=["red", "blue", "green", "yellow", "orange"])
        self.work_category_color_entry.set(self.work_category_color)  # Set a default value
        self.work_category_color_entry.pack()

        # Entry Field
        tk.Label(self.frame, text="Personal Category Color").pack()
        self.personal_category_color_entry = ttk.Combobox(self.frame, values=["red", "blue", "green", "yellow", "orange"])
        self.personal_category_color_entry.set(self.personal_category_color)  # Set a default value
        self.personal_category_color_entry.pack()

        #Button to save changes
        save_button = tk.Button(self.frame, text="Save Changes",  
                                command=lambda: self.update_pref(
                                    self.font_size_entry.get(),
                                    self.color_theme_entry.get(),
                                    self.notifications_entry.get(),
                                    self.reminders_entry.get(),
                                    self.reminder_time_entry.get(),
                                    self.school_category_color_entry.get(),
                                    self.work_category_color_entry.get(),
                                    self.personal_category_color_entry.get(),
                                ), font="Arial 12")
        save_button.pack(side="right", padx=5)


        #Button to return to calendar
        preferences_button = tk.Button(self.frame, text="Return To Calendar", command=self.continue_to_calendar, font="Arial 12")
        preferences_button.pack(side="left", padx=5)


    def update_pref(self, font_size, color_theme, notifications, reminders, reminder_time, school_category_color, work_category_color, personal_category_color):
        self.font_size =font_size
        self.color_theme = color_theme
        self.notifications = notifications
        self.reminders = reminders
        self.reminder_time = reminder_time
        self.school_category_color = school_category_color
        self.work_category_color = work_category_color
        self.personal_category_color = personal_category_color

        self.save_to_file(filename="./config/preferences.json")

    # Show calendar
    def show(self):
        self.frame.pack(side="left", fill="both", expand=True)

    # Hide calendar
    def hide(self):
        self.frame.pack_forget()