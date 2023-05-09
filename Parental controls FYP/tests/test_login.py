import unittest
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from Login import LoginForm


class TestLoginForm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.login_form = LoginForm(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_labels(self):
        self.assertEqual(
            self.login_form.heading['text'], "Internet Montioring and control")
        self.assertEqual(self.login_form.sign_in_label['text'], "Sign In")
        self.assertEqual(self.login_form.username_label['text'], "Username")
        self.assertEqual(self.login_form.password_label['text'], "Password")

    def test_entry(self):
        self.assertEqual(self.login_form.username_entry.get(), "")
        self.assertEqual(self.login_form.password_entry.get(), "")

    def test_login_success(self):
        self.login_form.username_entry.insert(0, "admin1")
        self.login_form.password_entry.insert(0, "Admin2")
        self.login_form.submit()
        self.assertEqual(self.login_form.attempts_remaining, 3)

    def test_login_failure(self):
        self.login_form.username_entry.insert(0, "invalid_username")
        self.login_form.password_entry.insert(0, "invalid_password")
        self.login_form.submit()
        self.assertEqual(self.login_form.attempts_remaining, 2)

    def test_login_attempts_remaining(self):
        self.login_form.username_entry.insert(0, "")
        self.login_form.password_entry.insert(0, "")
        self.login_form.submit()
        self.assertEqual(self.login_form.attempts_remaining, 2)

    def test_send_password_email(self):
        self.login_form.username_entry.insert(0, "admin1")
        self.login_form.send_password_email()
        messagebox.showinfo(
            "Success", "An email with your password has been sent.")


if __name__ == '__main__':
    unittest.main()
