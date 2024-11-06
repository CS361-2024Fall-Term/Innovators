import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

def show_date():
    # Display the current date in a label
    current_date = datetime.now().strftime("%m/%d/%y")
    date_label.config(text=f"Current Date: {current_date}")

def update_time():
    # Display the current time in the format HH:MM:SS
    current_time = datetime.now().strftime("%H:%M:%S")
    time_label.config(text=f"Current Time: {current_time}")
    # Call update_time again after 1000 milliseconds (1 second)
    root.after(1000, update_time)

def save_selected_date():
    # Save the selected date from the calendar widget
    global selected_date
    selected_date = cal.get_date()  # This gets the selected date as a string (format: 'MM/DD/YYYY')
    selected_date_label.config(text=f"Date: {selected_date}")

# Initial root window to get screen size
root = tk.Tk()
root.withdraw()  # Hide the root window initially

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate window size (for example, 80% of the screen size)
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Calculate position to center the window
position_right = int(screen_width / 2 - window_width / 2)
position_down = int(screen_height / 2 - window_height / 2)

root.destroy()  # Close the hidden root window

# Set up the main application window
root = tk.Tk()
root.title("EasyCal")
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

# Create and customize the calendar widget
cal = Calendar(
    root,
    selectmode="day",
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
    font="Arial 14",
    background="lightblue",
    foreground="black",
    selectbackground="darkblue",
    selectforeground="white",
    headersbackground="lightgray",
    headersforeground="black",
    daywidth=5,
    dayheight=5
)
cal.pack(pady=20)

# Button to save the selected date
save_date_button = tk.Button(root, text="Get Date", command=save_selected_date, font="Arial 12")
save_date_button.pack(pady=10)

# Label to display the selected date
selected_date_label = tk.Label(root, text="Date:", font="Arial 12 bold")
selected_date_label.pack(pady=10)

# Label to display the current date
date_label = tk.Label(root, text="", font="Arial 12 bold")
date_label.pack(pady=10)

# Label to display the current time
time_label = tk.Label(root, text="", font="Arial 12 bold")
time_label.pack(pady=10)

# Display the current date and start the real-time clock
show_date()
update_time()

# Run the application
root.mainloop()
