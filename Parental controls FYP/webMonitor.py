import matplotlib.pyplot as plt
import tkinter as tk
import sqlite3
import tkinter.ttk as ttk
import os
from graphData import show_graphs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
from tkinter import messagebox
import sys
import subprocess
import ctypes
import platform


class WebMonitoring:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        lb = tk.Label(self.frame, text="Web Monitoring",
                      font=("Arial Bold", 30))
        lb.pack()
        self.frame.pack(pady=20)

        conn = sqlite3.connect(
            r'C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        # Execute a SELECT statement to retrieve the data from the url table
        c.execute("SELECT datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), url, visit_count, title FROM urls WHERE visit_count > 0")

        # Fetch all the rows of the result
        rows = c.fetchall()

        # Create a table to display the data
        self.tree = ttk.Treeview(
            self.frame, columns=['Last Visit Time', 'URL', 'visit count', 'title'], show='headings')
        self.tree.pack(fill='both', expand=True)

        self.tree.heading('Last Visit Time', text='Last Visit Time')
        self.tree.heading('URL', text='URL')
        self.tree.heading('visit count', text=' Visit count')
        self.tree.heading('title', text=' Title')

        for row in rows:
            self.tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3]))

        scrollbar = tk.Scrollbar(
            self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # -----------------------------------------------------------------------------
        search_frame = tk.Frame(self.frame)
        search_frame.pack(pady=10, fill='x')

        self.search_entry = tk.Entry(search_frame, width=30, font="Arial, 20")
        self.search_entry.pack(side='left', padx=10)

        self.search_button = tk.Button(
            search_frame, text="Search", font=("Helvetica", 16), command=self.search)
        self.search_button.pack(side='left', padx=10)
        # ===================================================================================

        email_scheduler_frame = tk.Frame(self.frame)
        email_scheduler_frame.pack(pady=10, fill='x')

        self.enable_button = tk.Button(
            email_scheduler_frame, text="Enable Email Sending", command=self.enable_sending)
        self.enable_button.pack(side='left', padx=10)

        self.disable_button = tk.Button(
            email_scheduler_frame, text="Disable Email Sending", command=self.disable_sending)
        self.disable_button.pack(side='left', padx=10)

        # ====================================================================================

        self.test_email_button = tk.Button(
            email_scheduler_frame, text="Test Email Sending", command=self.test_email_sending)
        self.test_email_button.pack(side='left', padx=10)

        # =====================================================================================

        self.ascending_button = tk.Button(
            self.frame, text="Order Ascending", command=self.order_ascending)
        self.ascending_button.pack(side='left', padx=10)

        self.descending_button = tk.Button(
            self.frame, text="Order Descending", command=self.order_descending)
        self.descending_button.pack(side='left', padx=10)

        self.browser_label = tk.Label(
            self.frame, text="Current Browser: Chrome", font=("Helvetica", 12))
        self.browser_label.pack(pady=10)

        info_frame = tk.Frame(self.frame)
        info_frame.pack(pady=10)

        self.switch_button = tk.Button(
            info_frame, text="Switch Browser", font=("Helvetica", 16), command=self.switch_browser)
        self.switch_button.pack(side='left', padx=10)

        self.total_visits_label = tk.Label(
            info_frame, text=f'Total visits: {self.total_visits()}', font=("Helvetica", 12))
        self.total_visits_label.pack(side='left', padx=10)

        self.average_visits_label = tk.Label(
            info_frame, text=f'Average visits per website: {self.average_visits():.2f}', font=("Helvetica", 12))
        self.average_visits_label.pack(side='left', padx=10)

        self.graph_button = tk.Button(
            self.frame, text="Show Graphs", font=("Helvetica", 16), command=self.show_graph_wrapper)
        self.graph_button.pack(side='left', padx=10)

        self.browser = 'chrome'
        self.load_history()

    def order_ascending(self):
        # Connect to the database
        conn = sqlite3.connect(
            r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        # Execute a SELECT statement to retrieve the data from the url table, ordered by the "Last Visit Time" column in ascending order
        c.execute("SELECT datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), url, visit_count, title FROM urls WHERE visit_count > 0 ORDER BY last_visit_time ASC")

        c = conn.cursor()

        # Execute a SELECT statement to retrieve the data from the url table, ordered by the "Last Visit Time" column in ascending order
        c.execute("SELECT datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), url, visit_count, title FROM urls WHERE visit_count > 0 ORDER BY last_visit_time ASC")

        # Fetch all the rows of the result
        rows = c.fetchall()

        # Clear the existing data in the Treeview widget
        self.tree.delete(*self.tree.get_children())

        # Add the data to the Treeview widget
        for row in rows:
            self.tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3]))
        self.load_history()

    def order_descending(self):
        # Connect to the database
        conn = sqlite3.connect(
            r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        c.execute("SELECT datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), url, visit_count, title FROM urls WHERE visit_count > 0 ORDER BY datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') DESC")

        # Fetch all the rows of the result
        rows = c.fetchall()

        # Clear the existing data in the Treeview widget
        self.tree.delete(*self.tree.get_children())

        # Add the data to the Treeview widget
        for row in rows:
            self.tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3]))

    def search(self):
        # Connect to the database
        conn = sqlite3.connect(
            r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        # Get the search term from the search entry widget
        search_term = self.search_entry.get()

        # Execute a SELECT statement to retrieve the data from the url table, filtered by the search term
        c.execute(
            "SELECT datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), url, visit_count, title FROM urls WHERE visit_count > 0 AND (url LIKE ? OR title LIKE ?)", ('%'+search_term+'%', '%'+search_term+'%',))

        rows = c.fetchall()

        # Clear the existing data in the Treeview widget
        self.tree.delete(*self.tree.get_children())

        # Add the data to the Treeview widget
        for row in rows:
            self.tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3]))

        self.tree.columnconfigure(0, weight=1)
        self.tree.columnconfigure(1, weight=3)
        self.tree.rowconfigure(0, weight=1)
        ttk.Style().configure("Treeview", font=('Helvetica', 12),
                              background="#ffffff", foreground="#000000")

    def total_visits(self):
        conn = sqlite3.connect(
            r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        c.execute("SELECT SUM(visit_count) FROM urls WHERE visit_count > 0")
        total_visits = c.fetchone()[0]
        return total_visits
        self.load_history()

    def average_visits(self):
        conn = sqlite3.connect(
            r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        c.execute("SELECT AVG(visit_count) FROM urls WHERE visit_count > 0")
        avg_visits = c.fetchone()[0]
        return avg_visits
        self.load_history()

# ---------------------------------------------------------------------------------------------------------------------------------------------
    def load_history(self):
        if self.browser == 'chrome':
            db_path = r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History'
        else:
            db_path = r'C:\Users\{users}\AppData\Local\Microsoft\Edge\User Data\Default\History'

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), url, visit_count, title FROM urls WHERE visit_count > 0")
        rows = c.fetchall()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3]))

    def switch_browser(self):
        if self.browser == 'chrome':
            self.browser = 'edge'
            self.browser_label.config(text="Current Browser: Edge")
        else:
            self.browser = 'chrome'
            self.browser_label.config(text="Current Browser: Chrome")

        self.load_history()

    def show_graph_wrapper(self):
        show_graphs()

    def enable_sending(self):
        schedule.every(7).days.at("12:00").do(job)
        messagebox.showinfo("Email Scheduler", "Email sending enabled.")

    def disable_sending(self):
        schedule.clear()
        messagebox.showinfo("Email Scheduler", "Email sending disabled.")
# =======================================================================================================

    def test_email_sending(self):
        self.send_email()
        messagebox.showinfo("Email Test", "Test email sent.")

    def send_email(self):
        # Replace the following with your email credentials
        from_email = "@gmail.com"
        password = ""
        to_email = ""

        # Connect to the Chrome history database
        conn = sqlite3.connect(
            r'C:\Users\{users}\AppData\Local\Google\Chrome\User Data\Default\History')
        c = conn.cursor()

        # Execute a SELECT statement to retrieve the top 10 websites by visit_count
        c.execute(
            "SELECT url, visit_count, title FROM urls WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 10")
        top_websites = c.fetchall()

        # Create an HTML table to display the top 10 websites in the email
        table = "<table border='1'><tr><th>URL</th><th>Visit Count</th><th>Title</th></tr>"
        for website in top_websites:
            table += f"<tr><td>{website[0]}</td><td>{website[1]}</td><td>{website[2]}</td></tr>"
        table += "</table>"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "Weekly Report"

        body = f"<h3>Top 10 Visited Websites:</h3>{table}"
        msg.attach(MIMEText(body, 'html'))

        try:
            # Replace with your email provider's SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error: {e}")


def job():
    print("Sending weekly email...")
    send_email()

# ===================================================================================================================================
# disabling incgonito mode


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False


def disable_incognito_mode():
    if platform.system() != "Windows":
        print("This script is designed to work on Windows.")
        return

    # change 0 to renable it
    cmd = "REG ADD HKLM\\SOFTWARE\\Policies\\Google\\Chrome /v IncognitoModeAvailability /t REG_DWORD /d 1"
    try:
        result = subprocess.run(
            cmd, shell=True, text=True, capture_output=True, check=True)
        print("Incognito mode has been successfully disabled.")
    except subprocess.CalledProcessError as e:
        print(
            f"An error occurred while disabling Incognito mode: {e.output}", file=sys.stderr)


if __name__ == "__main__":
    if is_admin():
        disable_incognito_mode()
    else:
        print("Requesting administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)

    def pack(self):
        self.frame.pack()
