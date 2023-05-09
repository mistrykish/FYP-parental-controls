import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import schedule
import sched
import time
from datetime import datetime, timedelta
import threading
import pytz
import sqlite3
import ctypes
import re


class Screen:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        lb = tk.Label(self.frame, text="Screen Timeout",
                      font=("Arial Bold", 30))
        lb.pack(pady=20)

        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("day", "start_time", "end_time")
        self.tree.column("day", width=100, anchor="center")
        self.tree.column("start_time", width=100, anchor="center")
        self.tree.column("end_time", width=100, anchor="center")
        self.tree.heading("day", text="Day")
        self.tree.heading("start_time", text="Start Time")
        self.tree.heading("end_time", text="End Time")
        self.tree.pack(pady=20)

        self.update_treeview()

        # Dropdown menu for selecting the day
        day_label = tk.Label(
            self.frame, text="Select Day:", font=("Arial", 14))
        day_label.pack(pady=10)

        self.day_var = tk.StringVar(self.frame)
        self.day_dropdown = ttk.Combobox(self.frame, textvariable=self.day_var, values=[
                                         "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_dropdown.set("Select Day")
        self.day_dropdown.pack()

        # Input fields for start and end time
        start_time_label = tk.Label(
            self.frame, text="Start Time (HH:MM):", font=("Arial", 14))
        start_time_label.pack(pady=10)
        self.start_time = tk.Entry(self.frame, font=("Arial", 14))
        self.start_time.pack()

        end_time_label = tk.Label(
            self.frame, text="End Time (HH:MM):", font=("Arial", 14))
        end_time_label.pack(pady=10)
        self.end_time = tk.Entry(self.frame, font=("Arial", 14))
        self.end_time.pack()

        # Schedule button
        self.schedule_button = tk.Button(self.frame, text="Schedule", font=(
            "Arial", 14), command=self.schedule_screen_timeout)
        self.schedule_button.pack(pady=20)

        self.remove_button = tk.Button(self.frame, text="Remove", font=(
            "Arial", 14), command=self.remove_schedule)
        self.remove_button.pack(pady=10)

    def update_treeview(self):
        # Clear the Treeview widget
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Update the Treeview widget with the latest data from the SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM timeouts')
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    def is_valid_time(self, time_str):
        # Check if the input matches the expected format (HH:MM)
        match = re.match(r'^([0-9]{1,2}):([0-9]{2})$', time_str)
        if not match:
            return False

        hour, minute = map(int, match.groups())

        # Check if the hour and minute values are within the valid range
        return 0 <= hour <= 23 and 0 <= minute <= 59

    def schedule_screen_timeout(self):
        day = self.day_var.get()
        start_time = self.start_time.get()
        end_time = self.end_time.get()

        if day == "Select Day" or not start_time or not end_time:
            tk.messagebox.showerror(
                "Error", "Please select a day and specify start and end times.")
            return

        if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
            tk.messagebox.showerror(
                "Error", "Invalid time format. Please use the format HH:MM.")
        else:

            start_hour, start_minute = start_time.split(':')
            end_hour, end_minute = end_time.split(':')

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # Check if the entry is unique
            cursor.execute(
                "SELECT * FROM timeouts WHERE day = ? AND start_time = ? AND end_time = ?",
                (day, start_time, end_time))
            entry_exists = cursor.fetchone()

            if entry_exists:
                tk.messagebox.showerror(
                    "Error", "Duplicate entry. This schedule is already in the database.")
            else:
                cursor.execute(
                    '''INSERT INTO timeouts(day, start_time, end_time) VALUES(?, ?, ?)''',
                    (day, start_time, end_time))
                conn.commit()

                self.schedule_timeout(start_hour, start_minute)
                self.schedule_end(end_hour, end_minute,
                                  day, start_time, end_time)
                threading.Thread(target=self.scheduler_thread).start()
                self.update_treeview()

            conn.close()

    def remove_schedule(self):
        selected_items = self.tree.selection()

        if not selected_items:
            tk.messagebox.showerror(
                "Error", "No schedule is selected. Please select a schedule to remove.")
            return

        item = selected_items[0]
        day = self.tree.item(item, "values")[0]
        start_time = self.tree.item(item, "values")[1]
        end_time = self.tree.item(item, "values")[2]

        result = tk.messagebox.askyesno(
            "Remove Schedule", f"Are you sure you want to remove the schedule for {day} from {start_time} to {end_time}?")

        if result:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM timeouts WHERE day = ? AND start_time = ? AND end_time = ?", (day, start_time, end_time))
            conn.commit()
            conn.close()
            self.update_treeview()

    def show_screen_timeout(self):
        self.timeout_window = tk.Toplevel()
        self.timeout_window.attributes("-fullscreen", True)
        self.timeout_window.attributes("-topmost", True)
        self.timeout_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.timeout_window = ctypes.windll.user32.BlockInput(True)
        timeout_label = tk.Label(self.timeout_window, text="Time's up! Please step away from the computer",
                                 font=("Arial", 20), wraplength=350)
        timeout_label.pack(pady=20)

    def on_closing(self):
        self.close_window()

        # Unblock the Windows key
        keyboard.unblock_key('left windows')
        keyboard.unblock_key('right windows')

    def close_window(self):
        if self.timeout_window:
            self.timeout_window.destroy()

    def schedule_timeout(self, start_hour, start_minute):
        schedule.every().day.at(
            f"{start_hour}:{start_minute}").do(self.show_screen_timeout)

    def schedule_end(self, end_hour, end_minute, day, start_time, end_time):
        schedule.every().day.at(
            f"{end_hour}:{end_minute}").do(self.remove_entry, day, start_time, end_time)

    def remove_entry(self, day, start_time, end_time):
        self.close_window()

    # Remove the entry from the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM timeouts WHERE day = ? AND start_time = ? AND end_time = ?", (day, start_time, end_time))
        conn.commit()
        conn.close()

    # Update the Treeview
        self.update_treeview()

    def do_nothing(self):
        pass

    def scheduler_thread(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
