# welcome screen class
from PIL import Image, ImageTk
import tkinter as tk
import os
import sys
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

        # Empty frame for top padding
        top_padding = tk.Frame(self.frame, height=50, bg="white")  # Height for top padding
        top_padding.pack()


        continue_button = tk.Button(
            self.frame, text="Start Your Journey", font=("Helvetica", 16, "bold"), command=lambda: self.next_screen(continue_callback,open_profile ),
            bg="#2F39CF", fg="white", activebackground="#010CA5", activeforeground="white",
            relief="flat", borderwidth=5, padx=30, pady=15 
        )
        continue_button.pack(pady=10)

    def next_screen(self, calendar, profile):
        profile_json = "./src/config/user_info.json"
        try: 
            file_size = os.path.getsize(profile_json)
            if(file_size <= 38):
                profile()
            else:
                print(f"file is {file_size} bytes")
                calendar()
        except FileNotFoundError as e:
            print("profile.json not found")

    

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()