import tkinter as tk
import os
import json
from tkinter import ttk


class Profile:
    def __init__(self, root, continue_to_calendar):
        self.load_from_file()
        self.continue_to_calendar = continue_to_calendar
        #Preferences Frame
        self.frame = tk.Frame(root) 
        self.show()
        #Retrieve preferences from json
        self._setup_widgets()


    def save_to_file(self, filename="./src/config/user_info.json"):
        
        # Write data to a JSON file
        user_info = {
            "name" : self.user_name,
            "credits" : self.credits,
            "DOB" : self.dob
        }
        with open(filename, 'w') as f:
            json.dump(user_info, f)
        print(f"user info saved in: {filename}")

    def load_from_file(self, filename="./src/config/user_info.json"):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Convert each dictionary back to a Tasks object
            self.user_name = data["name"]
            self.credits = data["credits"]
            self.dob = data["DOB"]
        except FileNotFoundError:
            self.font_size = 13
            self.color_theme = "blue"
            self.notifications = False
            self.reminders = False
            self.reminder_time = 13
            print(f"File '{filename}' not found. Creating a new file.")
            self.save_to_file(filename)  # Create the file with an empty list
        except json.JSONDecodeError:
            print(f"The file '{filename}' contains invalid JSON. Starting with an empty list.")


    def _setup_widgets(self):
        # Preferences input fields

        #name
        self.name_label = tk.Label(self.frame, text="Name")
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.insert(0, str(self.user_name))
        self.name_label.pack()
        self.name_entry.pack()
        
        #credits
        self.credits_label = tk.Label(self.frame, text="Credits")
        self.credits_entry = tk.Entry(self.frame)
        self.credits_entry.insert(0, str(self.credits))
        self.credits_label.pack()
        self.credits_entry.pack()

        #dob
        self.dob_label = tk.Label(self.frame, text="Birthday (MM-DD)")
        self.dob_entry = tk.Entry(self.frame)
        self.dob_entry.insert(0, str(self.dob))
        self.dob_label.pack()
        self.dob_entry.pack()

        #Button to save changes
        save_button = tk.Button(self.frame, text="Save & Continue",  
                                command=lambda: self.update_profile(
                                    self.name_entry.get(),
                                    self.credits_entry.get(),
                                    self.dob_entry.get()
                                ), font="Arial 12")
        save_button.pack(side="bottom", padx=5)


    def update_profile(self, name, credits, dob):
        self.user_name = name
        self.credits = credits
        self.dob = dob

        self.save_to_file(filename="./src/config/user_info.json")
        self.continue_to_calendar()

    # Show calendar
    def show(self):
        self.frame.pack(side="left", fill="both", expand=True)

    # Hide calendar
    def hide(self):
        self.frame.pack_forget()