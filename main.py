import tkinter as tk
from tkinter import messagebox
from plyer import notification
import time
import threading

class TaskReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Reminder")

        
        self.tasks = []

        
        self.task_label = tk.Label(self.root, text="Task:")
        self.task_label.pack(pady=5)

        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack(pady=5)

        self.time_label = tk.Label(self.root, text="Reminder Time (HH:MM):")
        self.time_label.pack(pady=5)

        self.time_entry = tk.Entry(self.root, width=50)
        self.time_entry.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Reminders", command=self.start_reminders)
        self.start_button.pack(pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        reminder_time = self.time_entry.get().strip()
        if task and reminder_time:
            self.tasks.append((task, reminder_time))
            self.task_listbox.insert(tk.END, f"{task} at {reminder_time}")
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter both task and reminder time.")

    def start_reminders(self):
        threading.Thread(target=self.check_reminders, daemon=True).start()

    def check_reminders(self):
        while True:
            current_time = time.strftime("%H:%M")
            for task, reminder_time in self.tasks:
                if current_time == reminder_time:
                    notification.notify(
                        title="Task Reminder",
                        message=task,
                        app_name="Task Reminder",
                        timeout=10
                    )
                    self.tasks.remove((task, reminder_time))
                    self.task_listbox.delete(0, tk.END)
                    for t, rt in self.tasks:
                        self.task_listbox.insert(tk.END, f"{t} at {rt}")
            time.sleep(60)  # Check every minute

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskReminderApp(root)
    app.run()
