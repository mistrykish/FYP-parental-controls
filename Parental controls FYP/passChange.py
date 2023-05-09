import tkinter as tk
from tkinter import ttk
import sqlite3
import re


import tkinter as tk
from tkinter import messagebox
import sqlite3
import re


class PasswordChange:

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    def __init__(self, master):

        self.frame = tk.Frame(master)
        lb = tk.Label(self.frame, text="Change password",
                      font=("Arial Bold", 30))
        lb.pack(pady=20)
        self.frame.pack(pady=20)

        self.pattern = "[A-Za-z]"
        self.current_password_label = tk.Label(
            self.frame, text="Current Password:")
        self.current_password_label.pack()
        self.current_password_entry = tk.Entry(self.frame, show="*")
        self.current_password_entry.pack()

        self.new_password_label = tk.Label(self.frame, text="New Password:")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.frame, show="*")
        self.new_password_entry.pack()

        self.retype_password_label = tk.Label(
            self.frame, text="Retype Password:")
        self.retype_password_label.pack()
        self.retype_password_entry = tk.Entry(self.frame, show="*")
        self.retype_password_entry.pack()

        self.change_password_button = tk.Button(
            self.frame, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=10)

    def change_password(self):
        # Get the current and new passwords from the form
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        retyped_password = self.retype_password_entry.get()

        # Validate that the new password and retyped password match
        if new_password != retyped_password:
            messagebox.showerror(
                "Error", "The new password and retyped password do not match")
            return

        # Validate the strength of the new password
        if not self.validate_password(new_password):
            messagebox.showerror(
                "Error", "The new password is not strong enough")
            return

        # Validate that the current password is correct
        user = self.check_password(current_password)
        if not user:
            messagebox.showerror(
                "Error", "The current password is incorrect")
            return

        # Update the password in the database
        self.update_password(new_password, current_password)
        messagebox.showinfo(
            "Success", "The password has been successfully changed")

    def validate_password(self, password):
        # Use the regular expression pattern to check if the password is strong enough
        return bool(re.match(self.pattern, password))

    def check_password(self, password):
        # Check if the current password is correct
        PasswordChange.cursor.execute(
            "SELECT * FROM ADMIN WHERE password=?", (password,))
        return PasswordChange.cursor.fetchone()

    def update_password(self, new_password, current_password):
        # Update the password in the database
        PasswordChange.cursor.execute(
            "UPDATE ADMIN SET password=? WHERE password=?", (new_password, current_password))
        PasswordChange.conn.commit()
