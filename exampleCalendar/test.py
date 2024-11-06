import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

def show_date():
    # Display the current date in a label
    current_date = datetime.now().strftime("%Y-%m-%d")
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

# Set up the main application window
root = tk.Tk()
root.title("Modern Calendar Display with Time and Selected Date")
root.geometry("400x500")

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
