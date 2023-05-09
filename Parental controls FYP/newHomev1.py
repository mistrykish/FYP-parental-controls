import tkinter as tk
from webMonitor import WebMonitoring
from webFilter import WebFiltering
from ScreenTiming import Screen
from passChange import PasswordChange
from ttkbootstrap import Style
from tkinter import PhotoImage


class NewUI:

    def __init__(self, master, username):
        self.root = master
        self.root.geometry("500x400")
        self.root.title("Parental controls")
        self.username = username

        self.options_frame = tk.Frame(self.root, bg="#707070")
        self.options_frame.pack(side=tk.LEFT)
        self.options_frame.pack_propagate(False)
        self.options_frame.configure(width=100, height=500)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

    def home_page(self):
        self.delete_pages()
        webMon = WebMonitoring(self.main_frame)
        webMon.pack()

    def menu_page(self):
        self.delete_pages()
        webFil = WebFiltering(self.main_frame)
        webFil.pack()

    def screen_page(self):
        self.delete_pages()
        screening = Screen(self.main_frame)
        screening.pack()

    def adduser_page(self):
        self.delete_pages()
        pswrdChange = PasswordChange(self.main_frame)
        pswrdChange.pack()

    def hide_indicate(self):
        self.home_indicate.config(bg="#FFFFFF")
        self.menu_indicate.config(bg="#FFFFFF")
        self.screen_indicate.config(bg="#FFFFFF")
        self.adduser_indicate.config(bg="#FFFFFF")

    def delete_pages(self):
        if self.main_frame:
            for frame in self.main_frame.winfo_children():
                frame.destroy()

    def indicate(self, lb, page):
        self.hide_indicate()
        lb.config(bg="#adadad")
        self.delete_pages()
        page()

    def logout(self):
        self.root.destroy()

    def run(self):

        self.username_label = tk.Label(
            self.main_frame, text=f"Welcome, {self.username}", font=("Bold", 16))
        self.username_label.pack(pady=10)

        main_frame_width = 500
        main_frame_height = 400

        x = (main_frame_width // 2) - \
            (self.username_label.winfo_reqwidth() // 2)
        y = (main_frame_height // 2) - \
            (self.username_label.winfo_reqheight() // 2)

        self.username_label.place(x=x, y=y)

        image_file = "images\history.png"
        image = PhotoImage(file=image_file)

        self.home_indicate = tk.Label(
            self.options_frame, text="Home", image=image, font=("Bold", 16), bg="#707070")
        self.home_indicate.pack(pady=(50, 10))
        # Keep a reference to the image object to prevent garbage collection
        self.home_indicate.image = image

        image_file2 = "images\webfilter.png"
        image2 = PhotoImage(file=image_file2)
        self.menu_indicate = tk.Label(
            self.options_frame, text="Web Filtering", image=image2, font=("Bold", 16), bg="#707070")
        self.menu_indicate.pack(pady=10)
        self.menu_indicate.image = image2

        image_file4 = "images\screen.png"
        image4 = PhotoImage(file=image_file4)
        self.screen_indicate = tk.Label(
            self.options_frame, text="Screen", image=image4, font=("Bold", 16), bg="#707070")
        self.screen_indicate.pack(pady=10)
        self.screen_indicate.image = image4

        image_file5 = "images\lock.png"
        image5 = PhotoImage(file=image_file5)
        self.adduser_indicate = tk.Label(
            self.options_frame, text="add", image=image5, font=("Bold", 16))
        self.adduser_indicate.pack(pady=10)
        self.adduser_indicate.image = image5

        image_file6 = "images\logout.png"
        image6 = PhotoImage(file=image_file6)
        self.logout_indicate = tk.Label(
            self.options_frame, text="Logout", image=image6, font=("Bold", 16), bg="#707070")
        self.logout_indicate.pack(pady=10)
        self.logout_indicate.image = image6

        # Bind the home button to the home page method
        self.home_indicate.bind(
            "<Button-1>", lambda event: self.indicate(self.home_indicate, self.home_page))

        # Bind the menu button to the menu page method
        self.menu_indicate.bind(
            "<Button-1>", lambda event: self.indicate(self.menu_indicate, self.menu_page))

        # Bind the about button to the about page method
        self.screen_indicate.bind(
            "<Button-1>", lambda event: self.indicate(self.screen_indicate, self.screen_page))

        self.adduser_indicate.bind(
            "<Button-1>", lambda event: self.indicate(self.adduser_indicate, self.adduser_page))

        self.logout_indicate.bind("<Button-1>", lambda event: self.logout())


# if __name__ == '__main__':
#     root = tk.Tk()
#     style = Style(theme="flatly")
#     app = NewUI(root)
#     app.run()
#     root.mainloop()
