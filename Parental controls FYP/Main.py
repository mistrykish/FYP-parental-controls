# main.py
import tkinter as tk
from Login import LoginForm

# Create the main window
window = tk.Tk()
window.title("Login")

# Create the login form
login_form = LoginForm(window)


# Run the event loop
window.mainloop()
