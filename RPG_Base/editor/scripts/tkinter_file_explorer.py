# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *
import os

# import filedialog module
from tkinter import filedialog

# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askdirectory(initialdir = f"{os.path.dirname(__file__)}",
										title = "Select a Folder",
                                        )
    print(filename)
	
	# Change label contents
	#label_file_explorer.configure(text="File Opened: "+filename)
	
browseFiles()