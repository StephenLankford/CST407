################################################################################################################################
#	Authors: Hayden Hutsell and Stephen Lankford
#	Title: CST407 - HW1 - Caesar Cipher
#	Date: 06/29/2020
#	Revision History: 06/29/2020 - started caesar crack program
#	Summary: Crack Caesar ciphertext
################################################################################################################################

import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from pathlib import Path
from collections import OrderedDict
from collections import deque
import os

#########################################################	Global Variables	 #################################################	
user_input = ""
valid_input = ["help", "statistical", "quit"]	#add dictionary when implemented
base_table = "abcdefghijklmnopqrstuvwxyz"
letters = "ETAOINSRHDLUCMFYWGPBVKXQJZ"
frequency = [12.02, 9.10, 8.12, 7.68, 7.31, 6.95, 6.28, 6.02, 5.92,
            4.32, 3.98, 2.88, 2.71, 2.61, 2.30, 2.11, 2.09, 2.03, 1.82,
            1.49, 1.11, 0.69, 0.17, 0.11, 0.10, 0.07]	#e-z
frequencySorted  = [8.12, 1.49, 2.71, 4.32, 12.02, 2.3, 2.03, 5.92, 7.31, .1, .69, 3.98,
            2.61, 6.95, 7.68, 1.82, .11, 6.02, 6.28, 9.1, 2.88, 1.11, 2.09, .17, 2.11, .07]	#a-z

#########################################################	Validate Input	 #################################################	
def sanitize_input(raw):

	while (raw in valid_input) != True: #while the user doesn't type something from the valid_input list
		print("Invalid selection. For help, type help.\nEnter selection: ")
		raw = input("\nEnter selection: ")
	
	return raw

#########################################################	Directory	 #################################################	
def action(selection):
	if selection == "dictionary":
		dictionary()
	elif selection == "statistical":
		statistical()
	elif selection == "help":
		help_screen()
	else:
		print("error! user value was: ", user_input, ", but you somehow got here, bravo.\n")
		#sys.exit("__________fatal error__________"

#########################################################	Encryption	 #################################################			
def dictionary():

    #open filepicker dialog box
    filePath = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    toEncrypt = open(filePath, "r")		#open as read only

    finalString = ""

    ciphertext = open("CrackAttack.txt", "w")		#save the encrypted message as a text file in the same location as this program
    filename = ciphertext.name	
    ciphertext.write(finalString)
    ciphertext.close()
    os.system(filename)
#########################################################	Encryption	 #################################################			
def statistical():
    #open filepicker dialog box
    filePath = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    toDecrypt = open(filePath, "r")		#open as read only
    sortedList = sorted(frequency, reverse = True)
    endOfFile = False
    finalString = ""
    statCount = [0] * 26
    differenceCount = [0] * 26
    letterCount = 0
    difference = 0
    #print(statCount)

    while(not endOfFile):
        letter = toDecrypt.read(1)	#read one character at a time
        if letter == '':				#no character read
            endOfFile = True		#end of file
        elif (letter.isalpha()):						#end of file not detected yet
            change = ord(letter.upper())	#find ascii value of uppercase char
            statCount[change - 65] += 1     #count the number of times each letter is seen
            letterCount += 1
    toDecrypt.close()
    for element in range(len(statCount)):
        #print(element)
        statCount[element] = (statCount[element] / letterCount) * 100
    #print(statCount)    
    for element in range(len(statCount)):
        for x in range(len(statCount)):
            difference += abs(statCount[x] - frequencySorted[x]) 
        differenceCount[element] = difference
        statCount = deque(statCount)
        statCount.rotate(-1)
        statCount = list(statCount)
        difference = 0
    #frequencySorted list
    #statCount 26 element array that contains the average occurance of each letter (probably not aligned to the frequencySorted)
    #differenceCount 26 element array [100]
   

    #print(differenceCount)
    key = differenceCount.index(min(differenceCount))
    finalString = decrypt(key, filePath)

    ciphertext = open("CrackAttack.txt", "w")		#save the encrypted message as a text file in the same location as this program
    filename = ciphertext.name	
    ciphertext.write(finalString)
    ciphertext.close()
    os.system(filename)
#########################################################	Decryption	 #################################################
def decrypt(key, filePath):
	cipher = caesar_cipher_table(key)

	#open filepicker dialog box
	#filePath = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
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
	toDecrypt.close()
	return(finalString)
#########################################################	Table	 #################################################	
def caesar_cipher_table(key):
	cipher = ""
	temp_str = ""
	cipher_number = 0
	cipher_number = int(key) % 26
	temp_str = base_table[0:cipher_number]
	cipher = base_table[cipher_number: ]
	cipher = (cipher + temp_str).upper()
			
	print(cipher)
	return cipher
#########################################################	Help	 #################################################		
def help_screen():
	print("The menu options are help, quit, statistical, and dictionary - type your selection and hit 'Enter'.")
	print("When 'dictionary' or 'statistical' are entered, type the key, then a file picker dialog box will appear.")
	print("When a File Open dialog box appears after selecting 'dictionary', navigate to and select the text file to be encrypted.")
	print("When a File Open dialog box appears after selecting 'statistical', navigate to and select the encrypted message to be revealed.")

#########################################################	Main	 #################################################	
print("This program will attempt to crack a caesar cipher.\n\n\
for help, type help.\n\
for dictionary attack, type dictionary *NOT CURRENTLY IMPLEMENTED*\n\
for statistical analysis, type statistical\n\
to quit, type quit.")

while user_input != "quit": #stay in the loop until quit is ran

	raw_input = input("\nEnter selection: ")
	user_input = sanitize_input(raw_input) #make sure the input is valid
	if user_input != "quit":
		action(user_input)