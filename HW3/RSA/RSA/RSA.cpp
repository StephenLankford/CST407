/***********************************************************************************************************
* Developers: Hayden Hutsell and Stephen Lankford
* Purpose: Develop RSA program for CST407: Cryptography - Summer 2020
* Date Started: 07/30/2020
* Modifications: 07/30/2020 - Begain program, wrote menu in main, IsPrime(), Encrypt(), and Decrypt(). 
*                             Started key_generation() and inverseModulus()
***********************************************************************************************************/

// RSA.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

/*
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

bool IsPrime(int);  //determines whether p and q are prime numbers
int key_generation(int, int, int);  //generates key and calls either Encrypt() or Decrypt() based on user input
int Encrypt(int, int, int); //returns C (encrypted message)
int Decrypt(int, int, int); //returns M (decrypted message)

int main()
{
    int input = -1, p = 0, q = 0, N = 0, output = 0;
    bool again = true;
    char answer;

    while (again)
    {
        do
        {   //main menu
            cout << "Welcome to the RSA Encrypt/Decrypt Program!\n";
            cout << "Please select and option from the menu below.\n";
            cout << "1. Encrypt\n";
            cout << "2. Decrypt\n";
            cout << "3. Quit\n";
            cout << "Selection: ";
            cin >> input;

            if (input == 3)
            {
                return 0;   //3 was selected from menu, quit game
            }

            if (input < 1 || input > 2)
            {
                cout << "Incorrect menu selection. Try again!\n\n";
            }
        } while (input < 1 || input > 2);

        do
        {   //loop until p is greater than 10000 and prime
            cout << "Enter a 'p' value: ";
            cin >> p;
            cout << endl;
            if (!IsPrime(p))
            {
                cout << "Not a prime number greater than 10,000\n";
                p = 0;
            }

        } while (p <= 10000);

        do
        {   //loop until q is greater than 10000 and prime
            cout << "Enter a 'q' value: ";
            cin >> q;
            cout << endl;
            if (!IsPrime(q))
            {
                cout << "Not a prime number greater than 10,000\n";
                q = 0;
            }

        } while (q <= 10000);

        output = key_generation(p, q, input);   //calls the keygen function which returns
                                                //encrypted or decrypted message
        if (output == -1)
        {
            cout << "Error! Run program again!\n\n";
        }
        else
        {
            if (input == 1)
            {
                cout << "Encrypted message is: " << output << endl;
            }
            else
            {
                cout << "Decrypted message is: " << output << endl;
            }
        }

        cout << "Would you like to run the program again? Any key for Yes or N for No: ";
        cin >> answer;
        answer = toupper(answer);
        if (answer == 'N')
        {
            again = false;
        }
    }
    return 0;
}

//returns true if int is prime, false if it is not
bool IsPrime(int prime)
{
    if (prime <= 10000) //number is less than 10000, dont bother evaluating for prime
    {
        return false;
    }

    for (int i = 2; i < prime; i++)  //returns false if number is found to not be prime at any time
    {
        if (prime % i == 0)
        {
            return false;
        }
    }
    return true;    //number is prime
}

int key_generation(int p, int q, int input)
{
    int N = p * q;
    int e = 0, d = 0, C = 0, M = 0, message = 0;
    int totient = (p - 1) * (q - 1); //euler's totient function

    srand(time(0)); //set random seed, static cast 0 to unsigned cuz srand is fussy

    do
    {
        e = (rand() % (totient - 1)) + 2;
    } while ((gcd(e, totient) != 1) && IsPrime(e)); //generate a random number that 1<e<totient and prime

    //TODO: inver
    //pow();
    
    do
    {   //loop until the message to be encrypted or decrypted is less than N
        cout << "Please enter a number to encrypt (less than N): ";
        cin >> message;
        if (message >= N)
        {
            cout << "Incorrect entry - follow the instructions and try again!\n\n";
        }
    } while (message > N);  
    

    if (input == 1) //encrypt
    {
        C = Encrypt(M, e, N);
        return C;   //returns encrypted message to main()
    }
    else if (input == 2)    //decrypt
    {
        M = Decrypt(C, d, N);
        return M;   //returns decrypted message to main()
    }
    else
    {
        return -1;  //some error occurred
    }
}

//encrypts the message entered by the user, returns it to key gen
int Encrypt(int M, int e, int N)
{
    return ((int)pow(M, e) % N);
}

//decrypts the message entered by the user, returns it to key gen
int Decrypt(int C, int d, int N)
{
    return ((int)pow(C, d) % N);
}

void inverseModulus (int e, int N, int *b1, int *b2)
{
    if (e == 0) //reached last step in euclid algorithm
    {
        *b1 = 0;
        *b2 = 0;
    }
    int temp1 = 0;
    int temp2 = 0;
    
    //int eRecursive = ;

    inverseModulus(N % e, e, &temp1, &temp2); //recursive call. mimicing euclid steps
    
    *b1 = temp2 - (N/e) * temp1;
    *b2 = temp1;
    
    //b1 needs to be modded with N to find result when this function returns.

}