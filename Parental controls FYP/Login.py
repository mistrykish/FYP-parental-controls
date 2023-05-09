
import sqlite3
import customtkinter as ck
from tkinter import messagebox
from newHomev1 import NewUI
from tkinter import *
from PIL import ImageTk, Image
from ttkbootstrap import Style
import tkinter as tk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class LoginForm:
    def __init__(self, window):

        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')

        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#040405',
                               width=950, height=600)
        self.lgn_frame.place(x=480, y=240)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "Parental Controls"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=90, y=30, width=500, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('images\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(
            self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('images\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(
            self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                   font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="Black", fg="white",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="white",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground='#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(
            self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(
            self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # Set the number of remaining login attempts to 3
        self.attempts_remaining = 3

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(
            self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)

        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.submit)
        self.login.place(x=20, y=10)
        # ========================================================================
        # ============================Forgot password=============================
        # ========================================================================
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT,
                                    activebackground="#040405", borderwidth=0, background="#040405", cursor="hand2", command=self.send_password_email)
        self.forgot_button.place(x=630, y=510)
        # =========== Sign Up ==================================================

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#4f4e4d", fg="white",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(
            self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(
            self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage(file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage(file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def submit(self):
        # Connect to the database
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # Retrieve the username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username or password is empty
        if not username or not password:
            # Decrease the number of remaining attempts and display a message
            self.attempts_remaining -= 1
            if self.attempts_remaining > 0:
                messagebox.showerror(
                    "Error", f"Username and password cannot be empty. {self.attempts_remaining} attempts remaining.")
            else:
                messagebox.showerror(
                    "Error", "You have run out of login attempts. The application will now close.")
                self.window.destroy()
            return

        # Check if the username and password match a record in the database
        c.execute("SELECT * FROM ADMIN WHERE username=? AND password=?",
                  (username, password))
        result = c.fetchone()
        if result:
            # Login successful, redirect to homepage
            messagebox.showinfo("Success", "Login Successful")
            conn.close()
            self.window.destroy()
            root = tk.Tk()
            style = Style(theme="flatly")
            new_ui = NewUI(root, username)
            new_ui.run()
            root.mainloop()

        else:
            # Login failed, display an error message and decrease the number of remaining attempts
            self.attempts_remaining -= 1
            if self.attempts_remaining > 0:
                messagebox.showerror(
                    "Error", f"Invalid username or password. {self.attempts_remaining} attempts remaining.")
            else:
                messagebox.showerror(
                    "Error", "You have run out of login attempts. The application will now close.")
                self.window.destroy()
            conn.close()

    def send_password_email(self):
        # Connect to the database
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # Retrieve the username
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Error", "Please enter your username.")
            return

        c.execute("SELECT password FROM ADMIN WHERE username=?", (username,))
        result = c.fetchone()
        if result:
            password = result[0]
        else:
            messagebox.showerror("Error", "Invalid username.")
            return

        # Send an email with the password
        from_email = ""  # Replace with your email address
        to_email = ""
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = "Forgot Password"

        body = f"Hello {username},\n\nYour password is: {password}\n\nBest regards,\nYour Team"
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(from_email, "")  # add password
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            messagebox.showinfo(
                "Success", "An email with your password has been sent.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while sending the email: {e}")

        conn.close()
