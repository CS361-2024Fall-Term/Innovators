# welcome screen class
from PIL import Image, ImageTk
import tkinter as tk
import os
import sys
import json
from config.profile import Profile

class WelcomeScreen:
    def __init__(self, root, continue_callback, open_profile):
        self.root = root
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        # Determine the base path depending on the runtime context
        if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:  # If running from the source code
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the dynamic image path
        image_path = os.path.join(base_path, 'image.png')

        # Load the image
        pil_image = Image.open(image_path)

        # Resize the image to desired dimensions, e.g., 150x150 pixels
        pil_image = pil_image.resize((350, 263))

        # Convert to Tkinter-compatible image
        self.image = ImageTk.PhotoImage(pil_image)

        # Display image in a label, centered at the top
        image_label = tk.Label(self.frame, image=self.image, bg="white", borderwidth=0, highlightthickness=0)
        image_label.pack(pady=(40, 10))

        # checkf or profile json
        self.profile_json_path = os.path.expanduser("~/config/user_info.json")
        self.is_profile_complete = self.check_profile_status()

        # Empty frame for top padding
        top_padding = tk.Frame(self.frame, height=50, bg="white")  # Height for top padding
        top_padding.pack()


        continue_button = tk.Button(
            self.frame, text=self.welcome_message(), font=("Helvetica", 16, "bold"), command=lambda: self.next_screen(continue_callback,open_profile ),
            bg="#2F39CF", fg="white", activebackground="#010CA5", activeforeground="white",
            relief="flat", borderwidth=5, padx=30, pady=15 
        )

        continue_button.pack(pady=10)

    def welcome_message(self):
        profile_json = "./config/user_info.json"
        message = ""
        try: 
            file_size = os.path.getsize(profile_json)
            if(file_size <= 38):
                message = "Start Your Journey"
            else:
                print(f"file is {file_size} bytes")
                message = "Continue Your Journey"
        except FileNotFoundError as e:
            print("profile.json not found")
        return message
    
    def check_profile_status(self):

        # Check if the profile json file exists and contains correct data.

        try:
            if os.path.exists(self.profile_json_path):
                with open(self.profile_json_path, 'r') as f:
                    data = json.load(f)
                    # Consider the profile complete if all keys are present and non-empty
                    return all(data.get(key) for key in ["name", "credits", "DOB"])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error checking profile status: {e}")
        return False

    def next_screen(self, calendar, profile):

        profile_json = "./config/user_info.json"
        message = ""
        try: 
            file_size = os.path.getsize(profile_json)
            if(file_size <= 38):
                profile()
            else:
                print(f"file is {file_size} bytes")
                calendar()
        except FileNotFoundError as e:
            print("profile.json not found")
        return message
    

    

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()