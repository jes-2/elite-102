from tkinter import *
import db

window = Tk()

Tk.wm_title(window, "GUI")

mainframe = Frame(window)

login_frame = Frame(window)
login_button = Button(login_frame, text="Login", command=lambda: login())
login_notify = Label(login_frame, text="Please enter your credentials")
login_field_id = Entry(login_frame)

def login(id,psw):
    if db.idExists(id):
        if db.user_info[id]['psw'] == psw:
            return
        else:
            return

window.mainloop()