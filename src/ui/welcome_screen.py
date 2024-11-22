# welcome screen class
from PIL import Image, ImageTk
import tkinter as tk
import os
import sys

class WelcomeScreen:
    def __init__(self, root, continue_callback):
        self.root = root
        self.frame = tk.Frame(root)
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
        pil_image = pil_image.resize((150, 150))

        # Convert to Tkinter-compatible image
        self.image = ImageTk.PhotoImage(pil_image)

        # Display image in a label, centered at the top
        image_label = tk.Label(self.frame, image=self.image)
        image_label.pack(pady=(20, 10)) 

        # Empty frame for top padding
        top_padding = tk.Frame(self.frame, height=70)  # Height for top padding
        top_padding.pack()

        # Welcome message and button
        welcome_label = tk.Label(self.frame, text="Welcome to EasyCal!", font="Arial 18 bold")
        welcome_label.pack(pady=20)

        continue_button = tk.Button(
            self.frame, text="Start Your Journey", font=("Helvetica", 16, "bold"), command=continue_callback,
            bg="#1E90FF", fg="white", activebackground="#4682B4", activeforeground="white",
            relief="flat", borderwidth=5, padx=30, pady=15 
        )
        continue_button.pack(pady=10)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()