import tkinter as tk
from tkinter import ttk
import db

current_session = {'id':None,'name':None}

LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (main_page, account_page):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(main_page)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage


	
class main_page(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		navbar = tk.Frame(self, bg="black", height=100)
		navbar.pack(side="top", fill="x")
		welcome_msg = ttk.Label(
			navbar, text="Bank of C2C",
	        font=("Arial", 16),
	        background="black",
	        foreground="white"
	    )
		welcome_msg.pack(side="left", pady=10,padx=10)
		account_btn = ttk.Button(navbar, text="Account",command=lambda: controller.show_frame(account_page))
		account_btn.pack(side="left", pady=10,padx=10)
		
		self.style = ttk.Style()
		self.style.theme_use("alt")
		self.style.configure("TButton", font=("Verdana", 14), background="black", foreground="white")
    
		
class account_page(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		navbar = tk.Frame(self, bg="black", height=100)
		navbar.pack(side="top", fill="x")
		welcome_msg = ttk.Label(
			navbar, text="Bank of C2C",
	        font=("Arial", 16),
	        background="black",
	        foreground="white"
	    )
		welcome_msg.pack(side="top")
		

# Driver Code
app = tkinterApp()
app.mainloop()
