import tkinter as tk
from datetime import datetime

class DailyOverview:
    def __init__(self, root, tasks, events):
        self.root = root
        self.tasks = tasks
        self.events = events

        # Set the frame for daily overview
        self.frame = tk.Frame(root, bd=2, relief="solid")
        self.frame.pack(side="right", fill="both", expand=True)
        self.frame.pack_propagate(False)  # Prevent the frame from resizing

        # Add a label to display today's overview
        self.title_label = tk.Label(self.frame, text="Today's Overview", font=("Arial", 16, "bold"))
        self.title_label.pack(padx=5, pady=5)

        # Load today's tasks and events
        self.update_overview()

    def update_overview(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [task for task in self.tasks if task.start_date.startswith(today)]
        today_events = [event for event in self.events if event.start_time.startswith(today)]

        # Clear the frame before updating with new content
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text=f"Overview for {today}", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        # Add a section for tasks
        if today_tasks:
            tk.Label(self.frame, text="Tasks:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

            for task in today_tasks:
                task_frame = tk.Frame(self.frame, bd=2, relief="solid")
                task_frame.pack(fill="x", padx=10, pady=5)

                # Use grid to align Name and Description in the same row
                tk.Label(task_frame, text="Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
                tk.Label(task_frame, text=task.name, font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=10, pady=5)

                tk.Label(task_frame, text="Description:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
                tk.Label(task_frame, text=task.description, font=("Arial", 12), wraplength=360, justify="left").grid(row=1, column=1, sticky="w", padx=10, pady=5)

        else:
            tk.Label(self.frame, text="No Tasks", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        # Add a section for events
        if today_events:
            tk.Label(self.frame, text="Events:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

            for event in today_events:
                event_frame = tk.Frame(self.frame, bd=2, relief="solid")
                event_frame.pack(fill="x", padx=10, pady=5)

                # Use grid to align Name and Description in the same row
                tk.Label(event_frame, text="Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
                tk.Label(event_frame, text=event.name, font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=10, pady=5)

                tk.Label(event_frame, text="Description:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
                tk.Label(event_frame, text=event.description, font=("Arial", 12), wraplength=360, justify="left").grid(row=1, column=1, sticky="w", padx=10, pady=5)

        else:
            tk.Label(self.frame, text="No Events", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

    # Show the daily overview
    def show(self):
        self.frame.pack(side="right", fill="both", expand=True)

    # Hide the daily overview
    def hide(self):
        self.frame.pack_forget()