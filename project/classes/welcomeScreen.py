# welcome screen class
import tkinter as tk

class WelcomeScreen:
    def __init__(self, root, continue_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # Empty frame for top padding
        top_padding = tk.Frame(self.frame, height=170)  # Height for top padding
        top_padding.pack()

        # Welcome message and button
        welcome_label = tk.Label(self.frame, text="Welcome to EasyCal!", font="Arial 18 bold")
        welcome_label.pack(pady=20)

        continue_button = tk.Button(self.frame, text="Continue", font="Arial 14", command=continue_callback)
        continue_button.pack(pady=10)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()