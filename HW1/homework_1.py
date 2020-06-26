import sys
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from collections import OrderedDict
import os

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
		decrypt()
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
					temp_str = base_table[0:cipher_number]
					cipher = base_table[cipher_number: ]
					cipher = (cipher + temp_str).upper()
					valid = True
				else:
					cipher = key + base_table
					cipher = ("".join(OrderedDict.fromkeys(cipher))).upper() # joins characters together with "", puts them in an ordered dictionary using the cipher, uppercases it
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
	fileSize = Path(filePath).stat().st_size
	toEncrypt = open(filePath, "r")

	endOfFile = False
	finalString = ""

	while(not endOfFile):
		letter = toEncrypt.read(1)	#read one character at a time
		if letter == '':				#no character read
			endOfFile = True		#end of file
		elif (letter.isalpha()):						#end of file not detected yet
			change = ord(letter.upper())	#find ascii value of lowercase char
			#print(change - 65)
			#print(finalString)
			finalString += cipher[change - 65]
		else:
			finalString += letter
	
	ciphertext = open("EncryptedMessage.txt", "w")
	filename = ciphertext.name
	ciphertext.write(finalString)
	ciphertext.close()
	os.system(filename)
	
#########################################################	Decryption	 #################################################
def decrypt():
	key = input("Enter the encryption key (character, string, or integer): ")

	cipher = caesar_cipher_table(key)

	#open filepicker dialog box
	root = tk.Tk()
	root.withdraw()

	filePath = filedialog.askopenfilename()
	fileSize = Path(filePath).stat().st_size
	toDecrypt = open(filePath, "r")

	endOfFile = False
	finalString = ""

	while(not endOfFile):
		letter = toDecrypt.read(1)	#read one character at a time
		if letter == '':				#no character read
			endOfFile = True		#end of file
		elif (letter.isalpha()):						#end of file not detected yet
			change = ord(letter.lower())	#find ascii value of lowercase char
			#print(change - 65)
			#print(finalString)
			finalString += base_table[cipher[change - 97]]
		else:
			finalString += letter
	
	ciphertext = open("DecryptedMessage.txt", "w")
	filename = ciphertext.name
	ciphertext.write(finalString)
	ciphertext.close()
	os.system(filename)
	
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