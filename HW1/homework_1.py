################################################################################################################################
#	Authors: Hayden Hutsell and Stephen Lankford
#	Title: CST407 - HW1 - Caesar Cipher
#	Date: 06/23/2020
#	Revision History: 06/29/2020 - added some documentation, fixed and made file open more efficient, fixed decrypt function
#	Summary: Caesar Cipher Encrypt and Decrypt program. Asks for user input in the menu, then requires user input of cipher key,
#			 then plaintext file selection.
################################################################################################################################

import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from pathlib import Path
from collections import OrderedDict
import os

#########################################################	Global Variables	 #################################################	
#	these are our global variables.
#	User input defaults to empty.
#	base_table is alphabet a-z.
#	valid_input is the menu options a user can enter.
##################################################################################################################################
user_input = ""
base_table = "abcdefghijklmnopqrstuvwxyz"
valid_input = ["help", "encrypt", "decrypt", "quit"]

#########################################################	Validate Input	 #################################################
#	This function ensures the input from the user is valid. The user stays in this loop until a valid menu option is selected.
#	This function takes a string of characters, and returns the validated string of characters.
##############################################################################################################################	
def sanitize_input(raw):

	while (raw in valid_input) != True: #while the user doesn't type something from the valid_input list
		print("Invalid selection. For help, type help.\nEnter selection: ")
		raw = input("\nEnter selection: ")
	
	return raw

#########################################################	Directory	 #################################################
#	This function calls other functions depending on what the user entered. 
#	It is passed a string, and depending on the string calls another function to perform the action the user requested
##########################################################################################################################	
def action(selection):
	if selection == "encrypt":
		encrypt()
	elif selection == "decrypt":
		decrypt()
	elif selection == "help":
		help_screen()
	else:
		print("error! user value was: ", user_input, ", but you somehow got here, bravo.\n")
		sys.exit("__________fatal error__________")

#########################################################	Caesar	 #################################################
# 	This function converts a key and returns the caesar cipher table for the encrypt or decrypt functions.
#	Takes a key (letter, number, string of characters)
#	Validates the key, won't leave until a valid key is entered
#	Prints the table, and returns the table to the function that called it.
######################################################################################################################
def caesar_cipher_table(key):
	valid = False
	while valid == False:
		cipher = "" #empty string to build cipher table
		valid_num = True
		valid_str = True
		valid_entry = False
		cipher_number = 0
		temp_str = ""
		for element in key: #go through the key that was passed
			valid_entry = True #got to the loop, so its not an empty key
			if not (element.isdigit()): #if it isn't a digit, can't be a valid number
				valid_num = False
			if not (element.isalpha()): #if it isn't a letter, can't be a valid string
				valid_str = False
			
		if valid_entry == True: #if the string wasn't empty
			if (valid_num ^ valid_str): #and only one is true
				if (valid_num): #if its a number
					cipher_number = int(key) % 26					#base table is a list containing letters from A-Z
					temp_str = base_table[0:cipher_number] #make a temp string from 0 to the cipher number
					cipher = base_table[cipher_number: ] #set the cipher equal to the key to the end of the list
					cipher = (cipher + temp_str).upper() #set the cipher equal to the cipher + the temp string to create a rotated list of letters
					valid = True #valid input, don't need to keep the loop going
				else:
					cipher = key + base_table #set the cipher equal to the key + the base table. The key can be a letter or a string of letters.
					cipher = ("".join(OrderedDict.fromkeys(cipher))).upper() # joins characters together with "", puts them in an ordered dictionary using the cipher, uppercases it
					valid = True												#ordered dictionary means no repeats, so all repeats removed after the first occurrance.
		if valid == False:
			print("Invalid key entered. A key can be a letter, a base 10 number, or a sentence.\n") #didn't get a valid input. ask for another key.
			key = input("Enter a valid key: ")
	print(cipher) #print the cipher table for the user.
	return cipher #return the cipher table to be used by the calling function

#########################################################	Encryption	 #################################################
#	Encrypts a file based on the key that was entered by the user.
#	Asks the user for a key, calls caesar_cipher_table, and encrypts the file given the key.
#	File output is upper case
#	Only english letters are converted, all other characters are ignored.
#	Opens the file for the user to see.
##########################################################################################################################			
def encrypt():
	key = input("Enter the encryption key (character, string, or integer): ")

	cipher = caesar_cipher_table(key)

	#open filepicker dialog box
	filePath = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
	toEncrypt = open(filePath, "r")		#open as read only

	endOfFile = False
	finalString = ""

	while(not endOfFile):
		letter = toEncrypt.read(1)	#read one character at a time
		if letter == '':				#no character read
			endOfFile = True		#end of file
		elif (letter.isalpha()):						#end of file not detected yet
			change = ord(letter.upper())	#find ascii value of lowercase char
			# print(change - 65)
			# print(finalString)
			finalString += cipher[change - 65]	#convert plaintext to ciphertext based on ascii mod 26
		else:
			finalString += letter #just add the letter to the string if its not important to us (EOF, non alphabetical character)
	
	ciphertext = open("EncryptedMessage.txt", "w")		#save the encrypted message as a text file in the same location as this program
	filename = ciphertext.name	
	ciphertext.write(finalString) 
	ciphertext.close()
	os.system(filename) #open the file in default text editor
	
#########################################################	Decryption	 #################################################
#	Decrypts a file based on the key that was entered by the user.
#	Asks the user for a key, calls caesar_cipher_table, and decrypts the file given the key.
#	File output is lower case
#	Only english letters are converted, all other characters are ignored.
#	Opens the file for the user to see.
##########################################################################################################################
def decrypt():
	key = input("Enter the encryption key (character, string, or integer): ")

	cipher = caesar_cipher_table(key)

	#open filepicker dialog box
	filePath = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
	toDecrypt = open(filePath, "r")		#open as read only

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
			finalString += base_table[cipher.index(letter)]	#get the index number of the letter in the cipher table
															#aka the index of the plaintext letter in the base table or regular alphabet
		else:
			finalString += letter							#letter is not an alpha character, not required to encrypt
	
	ciphertext = open("DecryptedMessage.txt", "w")			#save the decrypted message as a text file in the same location as this program
	filename = ciphertext.name
	ciphertext.write(finalString)
	ciphertext.close()
	os.system(filename) #open the file in default text editor
	
#########################################################	Help	 #################################################
#	Describes what each menu option does, as well as general program functionality
######################################################################################################################		
def help_screen():
	print("The menu options are help, quit, encrypt, and decrypt - type your selection and hit 'Enter'.")
	print("When 'encrypt' or 'decrypt' are entered, type the key, then a file picker dialog box will appear.")
	print("The encrypt/decrypt key can be a decimal integer, letter, or a sentence.")
	print("When a File Open dialog box appears after selecting 'Encrypt', navigate to and select the text file to be encrypted.")
	print("When a File Open dialog box appears after selecting 'Decrypt', navigate to and select the encrypted message to be revealed.")

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