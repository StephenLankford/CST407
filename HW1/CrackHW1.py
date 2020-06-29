################################################################################################################################
#	Authors: Hayden Hutsell and Stephen Lankford
#	Title: CST407 - HW1 - Caesar Cipher
#	Date: 06/29/2020
#	Revision History: 06/29/2020 - started caesar crack program
#	Summary: Crack Caesar ciphertext
################################################################################################################################

#########################################################	Global Variables	 #################################################	
user_input = ""
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

#########################################################	Help	 #################################################		
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