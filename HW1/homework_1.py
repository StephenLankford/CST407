import sys
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from collections import OrderedDict

#########################################################	Global Variables	 #################################################	
user_input = ""
base_table = "abcdefghijklmnopqrstuvwxyz"
valid_input = ["help", "encrypt", "decrypt", "quit"]

#########################################################	Validate Input	 #################################################	
def sanitize_input(raw):

	while (raw in valid_input) != True: #while the user doesn't type something from the valid_input list
		print("Invalid selection. For help, type help.\nEnter selection: ")
		raw = input("\nEnter selection: ")
	
	return raw

#########################################################	Directory	 #################################################	
def action(selection):
	if selection == "encrypt":
		encrypt()
	elif selection == "decrypt":
		user_key = input("Enter a valid key. A key can be a letter, base 10 number, or a sentence: ")
		caesar_cipher_table(user_key)
	elif selection == "help":
		help_screen()
	else:
		print("error! user value was: ", user_input, ", but you somehow got here, bravo.\n")
		#sys.exit("__________fatal error__________"

#########################################################	Caesar	 #################################################	
def caesar_cipher_table(key):
	valid = False
	while valid == False:
		cipher = ""
		valid_num = True
		valid_str = True
		valid_entry = False
		cipher_number = 0
		count = 0
		temp_str = ""
		for element in key:
			count += 1
			valid_entry = True
			if not (element.isdigit()):
				valid_num = False
			if not (element.isalpha()):
				valid_str = False
		if ((count == 1) and (key.isalpha())):
			key = ord(key.upper()) - 65
			valid_str = False
			valid_num = True
			
		if valid_entry == True:
			if (valid_num ^ valid_str):
				if (valid_num):
					cipher_number = int(key) % 26
					temp_str = base_table[0:cipher_number - 1]
					cipher = base_table[cipher_number: ]
					cipher = (cipher + temp_str).upper()
					valid = True
				else:
					cipher = key + base_table
					cipher = ("".join(OrderedDict.fromkeys(cipher))).upper()
					valid = True
		if valid == False:
			print("Invalid key entered. A key can be a letter, a base 10 number, or a sentence.\n")
			key = input("Enter a valid key: ")
	print(cipher)
	return cipher

#########################################################	Encryption	 #################################################			
def encrypt():
	key = input("Enter the encryption key (character, string, or integer): ")

	cipher = caesar_cipher_table(key)

	#open filepicker dialog box
	root = tk.Tk()
	root.withdraw()

	filePath = filedialog.askopenfilename()
	fileSize = Path(file_path).stat().st_size
	toEncrypt = open("file_path", "r")

	endOfFile = True
	finalString = ""

	while(endOfFile):
		char = toEncrypt.read(1)	#read one character at a time
		if char == '':				#no character read
			endOfFile = False		#end of file
		elif (char.isalpha()):						#end of file not detected yet
			change = ord(char.lower)	#find ascii value of lowercase char
			finalString += cipher[change - 97]
		else:
			finalString += char

	ciphertext = open("EncryptedMessage.txt", "w")
	ciphertext.write(finalString)
	ciphertext.close()

#########################################################	Decryption	 #################################################
def decrypt():
	print("Enter a key: ")
	
#########################################################	Help	 #################################################		
def help_screen():
	print("decrypt key can be an decimal integer, letter, or a sentence.")

#########################################################	Main	 #################################################	
print("This program will encrypt and decrypt a file made up of english words.\n\n\
for help, type help.\n\
for encrypting, type encrypt\n\
for decrypting, type decrypt\n\
to quit, type quit.")

while user_input != "quit": #stay in the loop until quit is ran

	raw_input = input("\nEnter selection: ")
	user_input = sanitize_input(raw_input) #make sure the input is valid
	if user_input != "quit":
		action(user_input)