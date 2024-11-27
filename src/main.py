import os
import sys
import time
import tkinter as tk
from ui.welcome_screen import WelcomeScreen
from ui.calendar_class import Cal
from ui.daily_overview import DailyOverview
from ui.dynamic_sizing import DynamicSizing

# Redirect to a log file for compiled program testing
# Ensure the log file is created if it doesn't exist
log_file = "./src/app.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
sys.stdout = open(log_file, "a")
sys.stderr = sys.stdout
print("\n")
print(time.strftime("%Y-%m-%d %H:%M:%S"))

# Function that defines the continue function
def continue_to_calendar():
    welcome_screen.hide()
    calendar_app.show()
    daily_overview.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("EasyCal")

    # Dynamically size the window upon creation cause its cool
    DynamicSizing.set_window_size(root)

    # Load the custom icon (replace 'path/to/icon.png' with your actual file path)
    root.iconbitmap("./src/icon32.ico")

    # Create welcome screen with continue button
    welcome_screen = WelcomeScreen(root, continue_to_calendar)
    
    # Create a calendar object with an empty list of tasks and events
    calendar_app = Cal(root, 0, 0)

    # Create a DailyOverview object to display today's tasks and events
    daily_overview = DailyOverview(root, calendar_app.tasks, calendar_app.events)
    calendar_app.daily_overview = daily_overview

    # Show only the welcome screen
    calendar_app.hide()
    daily_overview.hide()
    welcome_screen.show()

    root.mainloop()
