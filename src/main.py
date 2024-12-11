import schedule
import json
import tkinter as tk
import threading
import time
from ui.welcome_screen import WelcomeScreen
from ui.calendar_class import Cal
from ui.daily_overview import DailyOverview
from ui.dynamic_sizing import DynamicSizing
from config.preferences import Preferences
from config.profile import Profile

def run_scheduler():
    print("Scheduler thread started.")  # debugging
    while True:
        schedule.run_pending()
        time.sleep(1)


# Redirect to a log file for compiled program testing
# Ensure the log file is created if it doesn't exist
# log_file = "./src/app.log"
# os.makedirs(os.path.dirname(log_file), exist_ok=True)
# sys.stdout = open(log_file, "a")
# sys.stderr = sys.stdout
# print("\n")
# print(time.strftime("%Y-%m-%d %H:%M:%S"))


# Function that defines the continue function
def continue_to_calendar():
    welcome_screen.hide()
    pref.hide()
    profile.hide()
    calendar_app.show()
    daily_overview.show()

    
def open_preferences():
    pref.show()
    # Hide the daily overview
    daily_overview.hide()
    calendar_app.hide()

def load_initial_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def open_profile():
    profile.show()
    # Hide the daily overview and calendar
    daily_overview.hide()
    calendar_app.hide()
    welcome_screen.hide()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("EasyCal")

    # Dynamically size the window upon creation cause its cool
    DynamicSizing.set_window_size(root)

    # Load the custom icon (replace 'path/to/icon.png' with your actual file path)
    root.iconbitmap("./icon32.ico")
    
    # Create welcome screen with continue button
    welcome_screen = WelcomeScreen(root, continue_to_calendar, open_profile)
    
    #Create preferences
    pref = Preferences(root, continue_to_calendar)

    tasks = load_initial_data("./src/tasks.json")
    events = load_initial_data("./src/events.json")

    #Create profile
    profile = Profile(root, continue_to_calendar)

    # Create a calendar object with an empty list of tasks and events
    calendar_app = Cal(root, tasks, events, pref, open_preferences, profile, open_profile)

    # Create a DailyOverview object to display today's tasks and events
    daily_overview = DailyOverview(root, calendar_app.tasks, calendar_app.events, calendar_app.profile)
    calendar_app.daily_overview = daily_overview

    schedule.every(60).seconds.do(calendar_app.reminder_for_events) # will run every 9 minutes
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Show only the welcome screen
    calendar_app.hide()
    daily_overview.hide()
    pref.hide()
    profile.hide()
    welcome_screen.show()

    root.mainloop()
