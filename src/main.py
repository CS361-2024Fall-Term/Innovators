import tkinter as tk
from ui.welcome_screen import WelcomeScreen
from ui.calendar_class import Cal

# Function that defines the continue function
def continue_to_calendar():
    welcome_screen.hide()
    calendar_app.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("EasyCal")

    # Create welcome screen with continue button
    welcome_screen = WelcomeScreen(root, continue_to_calendar)
    
    # Create a calendar object with an empty list of tasks and events
    calendar_app = Cal(root, 0, 0)

    # Show only the welcome screen
    calendar_app.hide()
    welcome_screen.show()

    root.mainloop()
