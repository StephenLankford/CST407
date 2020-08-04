/***********************************************************************************************************
* Developers: Hayden Hutsell and Stephen Lankford
* Purpose: Develop RSA program for CST407: Cryptography - Summer 2020
* Date Started: 07/30/2020
* Modifications: 07/30/2020 - Begain program, wrote menu in main, IsPrime(), Encrypt(), and Decrypt().
*                             Started key_generation() and inverseModulus(), documentation
*				 08/01/2020 - fixed bugs and logic errors, documentation, made sure RSA logic met assignment
*							  requirements
***********************************************************************************************************/

// RSA.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

/**************************************************************************************************

	1.    Write  a  C++  program  that  will  generate  three  sets  of  RSA  keys.  Make  sure
	primes  p,  q  and key e are numbers that are greater than 10000

	2.    Write  a  program  that  will  encrypt  or  decrypt  a  plaintext  number  using  RSA.
	Namely,  the program will ask the user to input a number for plaintext, e or d(depending on
	encrypting or decrypting) and n. The ciphertext will be a number. The recovered plaintext
	number will be the same as the original plaintext number. The program MUST use the keys
	generated in part 1 above.

*/

#include <iostream> //for cout, cin, endl
#include <numeric>  //for gcd
#include <cstdlib>  //for rand and srand
#include <ctime>    //for time
#include <cmath>    //for pow

using namespace std;    //for cout, cin, endl, gcd

//bool IsPrime(int);  //determines whether p and q are prime numbers
//void key_generation(int, int);  //generates key and calls either Encrypt() or Decrypt() based on user input
//unsigned long long Encrypt(int, int, int); //returns C (encrypted message)
//unsigned long long Decrypt(int, int, int); //returns M (decrypted message)
//void inverseModulus(int, int, int*, int*);	//euclidian algorithm
//unsigned long long Message(int, int, int, int);	//get user input, including message to be encrypted/decrypted

int main()
{
	unsigned long long a = 50011, b = 2479891, c = 302108907;
	unsigned long long C = 1;

	//cout << pow(50011.0, 2479891.0) % 302108907 << endl;

	for (unsigned long long i = 0; i < b; i++)
	{
		C = (C * a) % c;		//C = M^e mod N
	}

	cout << C << endl;

	return 0;
}

//int main()
//{
//	int input = -1, p = 0, q = 0;
//	int e = 5, d = 5;
//	bool again = true;
//	char answer;
//	unsigned long long output = 0;
//
//	cout << "Welcome to the RSA Encrypt/Decrypt Program!\n\n";
//
//	do
//	{   //loop until p is greater than 10000 and prime
//		cout << "Enter a 'p' value: ";
//		cin >> p;
//		cout << endl;
//
//		if (!IsPrime(p))
//		{
//			cout << "Not a prime number greater than 10,000\n";
//			p = 0;
//		}
//
//	} while (p <= 0);
//
//	do
//	{   //loop until q is greater than 10000 and prime
//		cout << "Enter a 'q' value: ";
//		cin >> q;
//		cout << endl;
//		if (!IsPrime(q))
//		{
//			cout << "Not a prime number greater than 10,000\n";
//			q = 0;
//		}
//
//	} while (q <= 0);
//
//	int N = p * q;
//	int totient = (p - 1) * (q - 1); //euler's totient function
//	srand((unsigned int)time(0));
//	key_generation(N, totient);   //calls the keygen function which returns
//										//encrypted or decrypted message
//	key_generation(N, totient);	//generate three key sets
//	key_generation(N, totient);
//
//	while (again)
//	{
//		do
//		{   //main menu
//			cout << "RSA Encrypt/Decrypt Program\n";
//			cout << "Please select an option from the menu below.\n";
//			cout << "1. Encrypt\n";
//			cout << "2. Decrypt\n";
//			cout << "3. Quit\n";
//			cout << "Selection: ";
//			cin >> input;
//
//			if (input == 3)
//			{
//				return 0;   //3 was selected from menu, quit game
//			}
//
//			if (input != 1 && input != 2)
//			{
//				cout << "Incorrect menu selection. Try again!\n" << endl;
//			}
//		} while (input != 1 && input != 2);	//loop until correct menu selection
//
//		output = Message(input, N, e, d);	//get encrypted or decrypted message
//
//		if (output == -1)	//output message
//		{
//			cout << "Error! Run program again!\n\n";
//		}
//		else
//		{
//			if (input == 1)
//			{
//				cout << "Encrypted message is: " << output << endl;
//			}
//			else
//			{
//				cout << "Decrypted message is: " << output << endl;
//			}
//		}
//
//		cout << "Would you like to run the program again? Any key for Yes or N for No: ";
//		cin >> answer;
//		answer = toupper(answer); //uppercase it
//		if (answer == 'N')
//		{
//			again = false;
//		}
//	}
//	return 0;
//}
//
////returns true if int is prime, false if it is not
///**********************************************************************
//* Purpose: Determines if the given number is prime or not
//*
//* Precondition:
//*     called at various points in the program when a prime number is needed
//*
//* Postcondition:
//*      returns true or false if the number is prime
//************************************************************************/
//bool IsPrime(int prime)
//{
//	if (prime <= 0) //number is less than 10000, dont bother evaluating for prime
//	{
//		return false;
//	}
//
//	for (int i = 2; i < prime; i++)  //returns false if number is found to not be prime at any time
//	{
//		if (prime % i == 0)
//		{
//			return false;
//		}
//	}
//	return true;    //number is prime
//}
//
//int gcd(int a, int b) {
//	if (b == 0)
//		return a;
//	return gcd(b, a % b);
//}
//
///**********************************************************************
//* Purpose: Generates the 3 keys, d, e, and N.
//*
//* Precondition:
//*     runs after p and q are entered by user in main
//*
//* Postcondition:
//*      prints the 3 keys to the console.
//************************************************************************/
//void key_generation(int N, int totient)
//{
//	long e = 5, d = 5;
//	int x = 0, y = 0;
//
//	//do
//	//{
//	//	e = (rand() % (totient - 1)) + 2; //random number generated off of seed set in main (based on the current time).
//	//} while (!((gcd(totient, e) == 1) && IsPrime(e) && e > 1)); //generate a random number e that 1<e<totient and prime, and coprime with totient
//
//	inverseModulus(e, totient, &x, &y);	//begin recursive euclidian algorithm
//
//	//d = ((x % totient) + totient) % totient; //if the number is negative
//	cout << "KEY RESULTS\n________________\ne = " << e << "\nd = " << d << "\nN = " << N << "\n\n"; //print the keys
//}
///**********************************************************************
//* Purpose: Handles the user encrypting and decrypting various messages
//*
//* Precondition:
//*     runs after the 3 sets of keys are generated
//*
//* Postcondition:
//*      Encrypts or decrypts depending on user input.
//************************************************************************/
//unsigned long long Message(int input, int N, int e, int d)
//{
//	int message = 0;
//	unsigned long long C = 0, M = 0;
//
//	if (input == 1) //encrypt, prompt user for input
//	{
//		cout << "Enter e: ";
//		cin >> e;
//		cout << "Enter N: ";
//		cin >> N;
//
//		do
//		{
//			cout << "Please enter a number to encrypt (less than " << N << "): ";
//			cin >> message;
//
//			if (message >= N)
//			{
//				cout << "Message (" << message << ") was greater than N (" << N << "). Try again.\n";
//			}
//		} while (message >= N);	//make sure message meets requirements
//
//		C = Encrypt(message, e, N);
//		return C;   //returns encrypted message to main()
//	}
//	else if (input == 2)    //decrypt, prompt user for input
//	{
//		cout << "Enter d: ";
//		cin >> d;
//		cout << "Enter N: ";
//		cin >> N;
//		do
//		{
//			cout << "Please enter a number to decrypt (less than " << N << "): ";
//			cin >> message;
//
//			if (message >= N)
//			{
//				cout << "Message (" << message << ") was greater than N (" << N << "). Try again.\n";
//			}
//		} while (message >= N);	//make sure message meets requirements
//
//		M = Decrypt(message, d, N);
//		return M;   //returns decrypted message to main()
//	}
//	else
//	{
//		return -1;  //some error occurred
//	}
//}
//
////encrypts the message entered by the user, returns it to key gen
///**********************************************************************
//* Purpose: The RSA encrypt algorithm (memory efficient method)
//*
//* Precondition:
//*     Called from message to encrypt given plaintext C
//*
//* Postcondition:
//*      returns the ciphertext number
//************************************************************************/
//unsigned long long Encrypt(int M, int e, int N)
//{
//	//return ((unsigned long long)pow(M, e) % N);
//	//return C;
//
//	int base = M, exponent = e, modulus = N;
//	unsigned long long C = 1;
//
//	for (int i = 0; i < exponent; i++)
//	{
//		C = (C * base) % modulus;		//C = M^e mod N
//	}
//
//	return C;
//}
//
////decrypts the message entered by the user, returns it to key gen
///**********************************************************************
//* Purpose: The RSA decrypt algorithm (memory efficient method)
//*
//* Precondition:
//*     Called from message to decrypt given ciphertext C
//*
//* Postcondition:
//*      returns the plaintext number
//************************************************************************/
//unsigned long long Decrypt(int C, int d, int N)
//{
//	int base = C, exponent = d, modulus = N;
//	unsigned long long M = 1;
//
//	for (int i = 0; i < exponent; i++)
//	{
//		M = (M * base) % modulus;		//M = C^d mod N
//	}
//
//	return M;
//}
///**********************************************************************
//* Purpose: This emulates the extended euclidian algorithm.
//*
//* Precondition:
//*     Called from generate keys, used in finding the private 'd' key.
//*
//* Postcondition:
//*      the pointer b1 is the Bezout coefficient to use to solve the inv mod equation
//*
//************************************************************************/
//void inverseModulus(int e, int N, int* b1, int* b2) //inverse modulus: ax congruent to 1 modulus totient(N), find x (b1 in this case)
//{
//	if (e == 0) //reached last step in euclid algorithm
//	{
//		*b1 = 0;
//		*b2 = 1;
//		return;
//	}
//	int temp1 = 0; //so there is a place to store the result
//	int temp2 = 0;
//
//	//int eRecursive = N % e;
//
//	inverseModulus(N % e, e, &temp1, &temp2); //recursive call. mimicing euclid steps. Finding GCD before reversing and going back up.
//
//	*b1 = temp2 - (N / e) * temp1; //this is the important part. the last call before returning to keygen will find the bezout coefficients.
//	*b2 = temp1;
//
//	//b1 needs to be modded with N to find result when this function returns.
//
//}