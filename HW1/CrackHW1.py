################################################################################################################################
#	Authors: Hayden Hutsell and Stephen Lankford
#	Title: CST407 - HW1 - Caesar Cipher
#	Date: 06/29/2020
#	Revision History: 06/29/2020 - started caesar crack program
#					  07/05/2020 - finished statistical attack
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
#	These are our global variables that are used in the program.
#	User input starts blank
#	valid_input is the valid options a user can type
#	base table is simply a list from a-z
#	letters is a list ordered from most common to least common letter occurrance. Used as a reference
#	Frequency is a list of the average occurance of all letters ordered from most to least common
#	FrequencySorted is a list of the the average occurance of all letters order from A-Z
##################################################################################################################################		
user_input = ""
valid_input = ["help", "statistical", "quit"]	#add dictionary when implemented
base_table = "abcdefghijklmnopqrstuvwxyz"
#letters = "ETAOINSRHDLUCMFYWGPBVKXQJZ"	#most common letters in order from left to right - Cornell
frequency = [12.02, 9.10, 8.12, 7.68, 7.31, 6.95, 6.28, 6.02, 5.92,
            4.32, 3.98, 2.88, 2.71, 2.61, 2.30, 2.11, 2.09, 2.03, 1.82,
            1.49, 1.11, 0.69, 0.17, 0.11, 0.10, 0.07]	#this list is the average occurance of all letters ordered from most to least common
frequencySorted  = [8.12, 1.49, 2.71, 4.32, 12.02, 2.3, 2.03, 5.92, 7.31, .1, .69, 3.98,
            2.61, 6.95, 7.68, 1.82, .11, 6.02, 6.28, 9.1, 2.88, 1.11, 2.09, .17, 2.11, .07]	#this list is the average occurance of all letters order from A-Z

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
	if selection == "statistical":
		statistical()	#stat chosen, call statistical analysis function
	elif selection == "help":
		help_screen()	#help chosen, call help function to display help instructions
	else:
		print("error! user value was: ", user_input, ", but you somehow got here, bravo.\n")
		#sys.exit("__________fatal error__________"

#########################################################	Statistical	 #################################################
#	This function attempts to decrypt a file that is encrypted with a caesar cipher table that is rotated by a number x
#	This means this does not work with files encrypted with a string, or a letter at the beginning of the string (CABDEF...)
#	asks the user for the file to decrypt
#	counts the occurance of encrypted letters
#	Creates a list that contains the average occurance of each letter
#	Rotates the list, creating another list containing the differences between the frequencySorted list and the statCount list
#	The most likely key is the position of the smallest value in the differences list. 
#	A decryption is performed with the most likely key, and the decryption result is written to a file.
#	the file is opened in the user's default text editor.
##########################################################################################################################			
def statistical():
    #open filepicker dialog box
    filePath = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    toDecrypt = open(filePath, "r")		#open as read only
    endOfFile = False
    finalString = ""	#final string of text to be output to file
    statCount = [0] * 26	#for counting number of each letters occurrence in ciphertext (list of 26 elements containing 0)
    differenceCount = [0] * 26	#for counting the difference in the frequency averages (list of 26 elements containing 0)
    letterCount = 0	#count letters in entire file for creating averages
    difference = 0	#variable for finding key based on difference between averages
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
    for element in range(len(statCount)):	#create averages between the number of times a ciphertext character is counted
        #print(element)						#and the number of ciphertext characters in the entire file
        statCount[element] = (statCount[element] / letterCount) * 100
    #print(statCount)    
    for element in range(len(statCount)):	#test each key for the difference between frequencies
        for x in range(len(statCount)):		#find difference between frequency of letter and times it was counted in the file
            difference += abs(statCount[x] - frequencySorted[x]) #ensure the difference is positive, as we find a min later
        differenceCount[element] = difference	#record the difference
        statCount = deque(statCount) #convert the statcount list into another type with the rotate function (a list like object, doubly ended queue)
        statCount.rotate(-1) #rotate left once
        statCount = list(statCount) #convert back into a list
        difference = 0 #reset the difference counter
    #frequencySorted list
    #statCount 26 element array that contains the average occurance of each letter (probably not aligned to the frequencySorted)
    #differenceCount 26 element array [100]
   
    key = differenceCount.index(min(differenceCount)) #key is the position of the smallest element
    finalString = decrypt(key, filePath)	#decrypt the file with the most likely key, passing the file path to the decrypt function.

    ciphertext = open("CrackAttack.txt", "w")		#save the encrypted message as a text file in the same location as this program
    filename = ciphertext.name	
    ciphertext.write(finalString) #write the decryption result to the file
    ciphertext.close() #close the file
    os.system(filename) #open the file in the default text editor
#########################################################	Decryption	 #################################################
#	This function reads in text from a file, and decrypts it with the key that it was passed, and returns the decrypted string
#	Takes a key and a file path
#	opens the file, reads in the text, and decrypts all english letters with the passed key.
#	returns the decryption result as a string
##########################################################################################################################
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
			finalString += base_table[cipher.index(letter.upper())]	#get the index number of the letter in the cipher table
															#aka the index of the plaintext letter in the base table or regular alphabet
		else:
			finalString += letter							#letter is not an alpha character, not required to encrypt
	toDecrypt.close() #close the file
	return(finalString)
#########################################################	Table	 #################################################
#	This function creates a caesar cipher table given a numberical key.
#	Prints the table, and returns the table to the caller
##########################################################################################################################		
def caesar_cipher_table(key):
	cipher = "" #empty string to build cipher table
	temp_str = ""
	cipher_number = 0 #ensure cipher_number will be an int
	cipher_number = int(key) % 26 		#base table is a list containing letters from A-Z
	temp_str = base_table[0:cipher_number]	#make a temp string from 0 to the cipher number
	cipher = base_table[cipher_number: ]	#set the cipher equal to the key to the end of the list
	cipher = (cipher + temp_str).upper()	#set the cipher equal to the cipher + the temp string to create a rotated list of letters
			
	print(cipher)
	return cipher
#########################################################	Help	 #################################################
#	Describes what each menu option does, as well as general program functionality
######################################################################################################################	
def help_screen():
	print("The menu options are help, quit, and statistical - type your selection and hit 'Enter'.")
	print("When 'statistical' is entered, type the key, then a file picker dialog box will appear.")
	print("When a File Open dialog box appears after selecting 'statistical', navigate to and select the encrypted message to be revealed.")

#########################################################	Main	 #################################################	
print("This program will attempt to crack a caesar cipher.\n\n\
for help, type help.\n\
for statistical analysis, type statistical\n\
to quit, type quit.")

while user_input != "quit": #stay in the loop until quit is ran

	raw_input = input("\nEnter selection: ")
	user_input = sanitize_input(raw_input) #make sure the input is valid
	if user_input != "quit":
		action(user_input)