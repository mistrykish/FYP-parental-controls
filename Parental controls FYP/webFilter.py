import tkinter as tk
#import tkinter.ttk as ttk
from tkinter import ttk
import sqlite3
import datetime
import os
import threading
import schedule
import time
import re
import tkinter.messagebox as messagebox


class WebFiltering:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        lb = tk.Label(self.frame, text="Web Filtering",
                      font=("Arial Bold", 30))
        lb.pack(pady=20)

        self.scheduled_jobs = []

        # Treeview widget
        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("websites", "timestamp", "schedule")
        self.tree.column("websites", width=100, anchor="center")
        self.tree.column("timestamp", width=100, anchor="center")
        self.tree.column("schedule", width=150, anchor="center")
        self.tree.heading("websites", text="Websites")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("schedule", text="Schedule")

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM websites')
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        self.tree.pack(pady=20)

        # User input field
        input_label = tk.Label(
            self.frame, text="Enter website:", font=("Arial", 14))
        input_label.pack(pady=10)
        self.input_field = tk.Entry(self.frame, font=("Arial", 14))
        self.input_field.pack()

        tk.Label(self.frame, text="e.g www.google.com or google.com",
                 font=("Arial", 12)).pack(pady=5)

        # Block and Unblock buttons
        self.block_button = tk.Button(self.frame, text="Block", font=(
            "Arial", 14), command=self.block_website)
        self.block_button.pack(pady=10)

        self.unblock_button = tk.Button(self.frame, text="Unblock", font=(
            "Arial", 14), command=self.unblock_website)
        self.unblock_button.pack(pady=10)

        # Dropdown menu for selecting the day to block
        self.day_var = tk.StringVar(self.frame)
        self.day_var.set("Select Day")

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
            "Arial", 14), command=self.schedule_block)
        self.schedule_button.pack(pady=20)

        self.check_scheduled_tasks()
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
   # handling the user input via validation

    def is_valid_url(self, url):
        regex = re.compile(
            r'^(?:www\.)?'  # optional www.
            # domain
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def is_valid_time(self, time_str):
        regex = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        return re.match(regex, time_str) is not None

    def update_treeview(self):
        # Clear the Treeview widget
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Update the Treeview widget with the latest data from the SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM websites')
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    def block_website(self, schedule=None):

        website = self.input_field.get()

        if not self.is_valid_url(website):
            tk.messagebox.showerror(
                "Error", "Please enter a valid website URL.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT * FROM websites WHERE websiteName=? AND (schedule=? OR schedule IS NULL)''', (website, schedule))
        row = cursor.fetchone()

        if row:
            conn.close()
            tk.messagebox.showerror("Error", "The website is already blocked.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            '''INSERT INTO websites(websiteName, timestamp, schedule) VALUES(?, ?, ?)''', (website, timestamp, schedule))
        conn.commit()
        conn.close()

        # Modify the host file to block the website
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts_path, "a") as host_file:
            host_file.write("\n127.0.0.1 " + website)
            print("im from blocking")
        os.system("ipconfig /flushdns")

        self.update_treeview()

    def unblock_website(self):
        # Get the website to unblock from the selected row

        selected_items = self.tree.selection()

        if not selected_items:
            tk.messagebox.showinfo("Info", "There's no website to unblock.")
            return

        item = self.tree.selection()[0]
        website = self.tree.item(item, "values")[0]
        timestamp = self.tree.item(item, "values")[1]

        result = tk.messagebox.askyesno(
            "Unblock Website", f"Are you sure you want to unblock {website}?")

        # Unblock the website
        if result:
            self.unblock(website, timestamp)
            self.update_treeview()

    def unblock(self, website, timestamp, schedule=None):
        # Read the contents of the host file into a list of lines

        print(website + timestamp)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        if schedule == None:

            cursor.execute(
                "DELETE FROM websites WHERE websiteName = ? AND timestamp = ?", (website, timestamp))
            conn.commit()
            conn.close()
        else:
            cursor.execute(
                "DELETE FROM websites WHERE websiteName = ? AND schedule = ?", (website, schedule))
            conn.commit()
            conn.close()

        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts_path, "r") as host_file:
            print("im from unblocking ")
            lines = host_file.readlines()

        # Find the line that contains the website to unblock and delete it
        for i, line in enumerate(lines):
            if website in line:
                del lines[i]
                break

        # Write the modified list of lines back to the host file
        with open(hosts_path, "w") as host_file:
            host_file.writelines(lines)

        # Flush the DNS cache to apply the changes
        os.system("ipconfig /flushdns")

    def schedule_block(self):
        website = self.input_field.get()
        day = self.day_var.get()
        start_time = self.start_time.get()
        end_time = self.end_time.get()

        if not self.is_valid_url(website):
            tk.messagebox.showerror(
                "Error", "Please enter a valid website URL.")
            return

        if day == "Select Day" or not start_time or not end_time:
            tk.messagebox.showerror(
                "Error", "Please select a day and specify start and end times.")
            return

        if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
            tk.messagebox.showerror(
                "Error", "Please enter valid start and end times in the format HH:MM.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT * FROM websites WHERE websiteName=? AND (schedule IS NULL OR schedule<>'')''', (website,))
        row = cursor.fetchone()

        if row:
            conn.close()
            tk.messagebox.showerror(
                "Error", "The website is already blocked or scheduled.")
            return

        start_hour, start_minute = start_time.split(':')
        end_hour, end_minute = end_time.split(':')

        def job():
            print("im in job atm")
            schedule_info = f"{day} {start_time} to {end_time}"
            self.block_website(schedule=schedule_info)
            print(f"Blocking {website}")

        def end_job():
            schedule_info = f"{day} {start_time} to {end_time}"
            self.unblock(website, '', schedule=schedule_info)
            self.update_treeview()

        job_id = f"{day}_{start_time}_{end_time}_{website}"
        if job_id not in self.scheduled_jobs:
            schedule.every().day.at(
                f"{start_hour}:{start_minute}").do(job)
            schedule.every().day.at(
                f"{end_hour}:{end_minute}").do(end_job)

            self.scheduled_jobs.append(job_id)

            # Add .start() here
            # threading.Thread(target=self.scheduler_thread).start()
            schedule.run_pending()
            messagebox.showinfo(
                "Success", f"{website} has been scheduled to be blocked on {day} from {start_time} to {end_time}.")

    def check_scheduled_tasks(self):
        schedule.run_pending()
        self.frame.after(1000, self.check_scheduled_tasks)

    def scheduler_thread(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
