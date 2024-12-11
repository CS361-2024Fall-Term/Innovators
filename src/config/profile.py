import tkinter as tk
import os
import json
from tkinter import ttk


class Profile:
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
    DEFAULT_JSON_PATH = os.path.join(BASE_DIR, "user_info.json")

    def __init__(self, root, continue_to_calendar):
        # Initialize attributes with default values
        self.user_name = "Guest"
        self.credits = 0
        self.dob = "01-01"

        # Load from file or set defaults
        self.load_from_file()

        self.continue_to_calendar = continue_to_calendar
        self.frame = tk.Frame(root)
        self.show()
        self._setup_widgets()

    def save_to_file(self, filename=DEFAULT_JSON_PATH):
        # Write data to a JSON file
        user_info = {
            "name": self.user_name,
            "credits": self.credits,
            "DOB": self.dob,
        }

        with open(filename, 'w') as f:
            json.dump(user_info, f)
        print(f"user info saved in: {filename}")

    def load_from_file(self, filename=DEFAULT_JSON_PATH):
        dir_path = os.path.dirname(filename)
        print(f"Ensuring directory exists for: {dir_path}")
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Convert each dictionary back to an object
            self.user_name = data.get("name", "Guest")
            self.credits = data.get("credits", 0)
            self.dob = data.get("DOB", "01-01")
        except FileNotFoundError:
            print(f"File '{filename}' not found. Creating a new file.")
            self.save_to_file(filename)
        except json.JSONDecodeError:
            print(f"The file '{filename}' contains invalid JSON. Starting with defaults.")
            self.save_to_file(filename)


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

        self.save_to_file(filename=self.DEFAULT_JSON_PATH)
        self.continue_to_calendar()
    
    def get_name(self):
        self.load_from_file()
        return self.user_name
    
    def get_credits(self):
        self.load_from_file()
        return self.credits
    
    def get_bday(self):
        self.load_from_file()
        return self.dob

    # Show calendar
    def show(self):
        self.frame.pack(side="left", fill="both", expand=True)

    # Hide calendar
    def hide(self):
        self.frame.pack_forget()