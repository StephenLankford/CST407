import sys
user_input = ""
valid_input = ["help", "encrypt", "decrypt", "quit"]
print("This program will encrypt and decrypt a file made up of english words.\n\n\
for help, type help.\n\
for encrypting, type encrypt\n\
for decrypting, type decrypt\n\
to quit, type quit.")
while user_input != "quit":

	raw_input = input("\nEnter selection: ")
	user_input = sanitize_input(raw_input)

def sanitize_input(raw):

	while (raw in valid_input) != True:
		print("Invalid selection. For help, type help.\nEnter selection: ")
		raw = input("\nEnter selection: ")
	
	return raw
	
#def user_choice(user_input):

#open filepicker dialog box
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()