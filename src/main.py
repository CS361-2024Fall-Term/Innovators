import tkinter as tk
from ui.welcome_screen import WelcomeScreen
from ui.calendar_class import Cal
from ui.daily_overview import DailyOverview

# Function that defines the continue function
def continue_to_calendar():
    welcome_screen.hide()
    calendar_app.show()
    daily_overview.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("EasyCal")

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
