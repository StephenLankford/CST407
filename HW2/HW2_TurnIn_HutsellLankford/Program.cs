/******************************************************************************************************************
 * Programmers: Hayden Hutsell and Stephen Lankford
 * Assignment: 2 - SDES (https://oit.instructure.com/courses/7105/files/1195299?module_item_id=419476)
 * Date Started: 07/14/2020
 * Updates:     07/14/2020 - work on SDES key gen, started SDES encryption steps
 *              07/17/2020 - FK and switch finished, documentation
 *              07/19/2020 - added decrypt functionality, more documentation
 * ***************************************************************************************************************/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace homework2
{
    public class Program
    {
        //variables
        public static char[] key1 = new char[8];
        public static char[] key2 = new char[8];
        public static char[] userTxtArray = new char[8];
        //public static bool encryptFlag = true;    //true if encrypting, false if decrypting

        static int[,] s0 = new int[4, 4] { { 1, 0, 3, 2 },
                                    { 3, 2, 1, 0 },
                                    { 0, 2, 1, 3 },
                                    { 3, 1, 3, 2 }  }; //2D These are the S boxes for the Fk function
        static int[,] s1 = new int[4, 4] { { 0, 1, 2, 3 },
                                    { 2, 0, 1, 3 },
                                    { 3, 0, 1, 0 },
                                    { 2, 1, 0, 3 }  }; //2D 
        /**********************************************************************
        * Purpose: Main
        *
        * Precondition:
        *     Program is started
        *
        * Postcondition:
        *      Takes user input for the 10 bit key and performs encryption, 
        *      decryption, or exits the program.
        *
        ************************************************************************/
        public static void Main(string[] args)
        {
            string input = "";

            bool quit = false; //used to determine when the program quits

            Console.WriteLine("Welcome to SDES! Encrypt/Decrypt an 8-bit character!");
            Console.WriteLine();

            //Console.Write("Enter a key: ");
            //KeyGen(); //generate the 10bit key
            quit = false;

            while (!quit)   //console menu
            {
                Console.Write("Type one of the following options - encrypt, decrypt, or quit: ");
                input = Console.ReadLine();
                Console.WriteLine();

                if (input.Contains("encrypt"))
                {
                    Console.Write("Enter a key: ");
                    KeyGen(); //generate the 10bit key

                    Console.Write("Type a binary 8 bit number to convert: ");
                    userTxtArray = ValidateNum();
                    Encryption(userTxtArray);
                }
                else if (input.Contains("decrypt"))
                {
                    Console.Write("Enter a key: ");
                    KeyGen(); //generate the 10bit key

                    Console.Write("Type a binary 8 bit number to convert: ");
                    userTxtArray = ValidateNum();
                    Decryption(userTxtArray);
                }
                else if (input.Contains("quit"))
                {
                    quit = true;
                }
                else
                {
                    Console.WriteLine("Invalid selection!!");
                    Console.WriteLine();
                }
            }
        }
        /**********************************************************************
        * Purpose: Encryption. Calls the various functions to encrypt the given 
        *           8 bit plain text.    
        *
        * Precondition:
        *     passed 8 bit plain text.
        *
        * Postcondition:
        *      prints the 8 bit cipher text.
        *
        ************************************************************************/
        public static void Encryption(char[] input)   //by reference or by value?
        {
            char[] left = { input[0], input[1], input[2], input[3] };   //left most 4 bits of plaintext
            char[] right = { input[4], input[5], input[6], input[7] };  //right most 4 bits of plaintext

            //IP
            left[0] = input[1];
            left[1] = input[5];
            left[2] = input[2];
            left[3] = input[0];
            right[0] = input[3];
            right[1] = input[7];
            right[2] = input[4];
            right[3] = input[6];

            FK(ref left, ref right, true);    //ref needed, key 1 used first for encrypt
            FK(ref right, ref left, false);    //inverse IP created, key 2 used second for encrypt

            //next call?
            Console.Write("Result: ");
            Console.WriteLine(IPinverse(right, left));
            Console.WriteLine();
        }
        /**********************************************************************
        * Purpose: Decryption. Calls the various functions to decrypt the given 
        *           8 bit cipher text.    
        *
        * Precondition:
        *     passed 8 bit cipher text.
        *
        * Postcondition:
        *      prints the 8 bit plain text.
        *
        ************************************************************************/
        public static void Decryption(char[] input)   //by reference or by value?
        {
            char[] left = { input[0], input[1], input[2], input[3] };   //left most 4 bits of plaintext
            char[] right = { input[4], input[5], input[6], input[7] };  //right most 4 bits of plaintext

            //IP
            left[0] = input[1];
            left[1] = input[5];
            left[2] = input[2];
            left[3] = input[0];
            right[0] = input[3];
            right[1] = input[7];
            right[2] = input[4];
            right[3] = input[6];

            FK(ref left, ref right, false);    //ref needed, use key 2 first for decrypt
            FK(ref right, ref left, true);    //inverse IP created, use key 1 second for decrypt

            //next call?
            Console.Write("Result: ");
            Console.WriteLine(IPinverse(right, left));
            Console.WriteLine();
        }
        public static char[] IPinverse(char[] l, char[] m)
        {
            char[] inverseIP = new char[8] { l[3], l[0], l[2], m[0], m[2], l[1], m[3], m[1] };
            return inverseIP;
        }
        /**********************************************************************
        * Purpose: This is the FK function in the SDES algorithm.    
        *
        * Precondition:
        *     passed the 8 bits and an encrypt flag. The encrypt flag determines 
        *       if key1 or key2 is used for the intial add.
        *
        * Postcondition:
        *      alters the 8 bits (since the lsb and msb are passed by reference, no return)
        *
        ************************************************************************/
        public static void FK(ref char[] l, ref char[] r, bool encryptFlag)
        {
            //expansion/permutation
            char[] EP1 = { r[3], r[0], r[1], r[2], r[1], r[2], r[3], r[0] };

            //variables
            char[] P4 = { '0', '0', '0', '0' };
            int[] rowCol0 = { 0, 0 };   //coordinate for s0
            int[] rowCol1 = { 0, 0 };   //coordinate for s1
            int s0result = 0, s1result = 0; //outputs of sboxes for use in P4

            //if encrypt is selected then key 1 is used first, then key 2
            //if decrypt is selected then key 2 is used first, then key 1
            if (encryptFlag)
            {
                for (int i = 0; i < 8; i++) //8-bit subkey added to EP using XOR
                {
                    if (key1[i] == EP1[i])
                    {
                        EP1[i] = '0';
                    }
                    else
                    {
                        EP1[i] = '1';
                    }
                }
            }
            else
            {
                for (int i = 0; i < 8; i++) //8-bit subkey added to EP using XOR
                {
                    if (key2[i] == EP1[i])
                    {
                        EP1[i] = '0';
                    }
                    else
                    {
                        EP1[i] = '1';
                    }
                }
            }

            //first and fourth bits are the row
            //second and third bits are the column
            //EP1[0] = p0,0, EP1[1] = p0,1, EP1[2] = p0,2, EP1[3] = p0,3, 
            //EP1[4] = p1,0, EP1[5] = p1,1, EP1[6] = p1,2, EP1[7] = p1,3

            switch (EP1[0]) //row
            {
                case '0':
                    switch (EP1[3])
                    {
                        case '0':
                            //first row
                            rowCol0[0] = 0;
                            break;
                        case '1':
                            //second row
                            rowCol0[0] = 1;
                            break;
                    }
                    break;
                case '1':
                    switch (EP1[3])
                    {
                        case '0':
                            //third row
                            rowCol0[0] = 2;
                            break;
                        case '1':
                            //fourth row
                            rowCol0[0] = 3;
                            break;
                    }
                    break;
            }

            switch (EP1[1]) //column
            {
                case '0':
                    switch (EP1[2])
                    {
                        case '0':
                            //first column
                            rowCol0[1] = 0;
                            break;
                        case '1':
                            //second column
                            rowCol0[1] = 1;
                            break;
                    }
                    break;
                case '1':
                    switch (EP1[2])
                    {
                        case '0':
                            //third column
                            rowCol0[1] = 2;
                            break;
                        case '1':
                            //fourth column
                            rowCol0[1] = 3;
                            break;
                    }
                    break;
            }
            //need to repeat for other input
            switch (EP1[4]) //row
            {
                case '0':
                    switch (EP1[7])
                    {
                        case '0':
                            //first row
                            rowCol1[0] = 0;
                            break;
                        case '1':
                            //second row
                            rowCol1[0] = 1;
                            break;
                    }
                    break;
                case '1':
                    switch (EP1[7])
                    {
                        case '0':
                            //third row
                            rowCol1[0] = 2;
                            break;
                        case '1':
                            //fourth row
                            rowCol1[0] = 3;
                            break;
                    }
                    break;
            }

            switch (EP1[5]) //column
            {
                case '0':
                    switch (EP1[6])
                    {
                        case '0':
                            //first column
                            rowCol1[1] = 0;
                            break;
                        case '1':
                            //second column
                            rowCol1[1] = 1;
                            break;
                    }
                    break;
                case '1':
                    switch (EP1[6])
                    {
                        case '0':
                            //third column
                            rowCol1[1] = 2;
                            break;
                        case '1':
                            //fourth column
                            rowCol1[1] = 3;
                            break;
                    }
                    break;
            }

            //s box magic
            s0result = s0[rowCol0[0], rowCol0[1]];  //grab sbox 0 value
            s1result = s1[rowCol1[0], rowCol1[1]];  //grab sbox 1 value

            switch (s0result)   //generate p4 input
            {
                case 0:
                    P4[0] = '0';
                    P4[1] = '0';
                    break;
                case 1:
                    P4[0] = '0';
                    P4[1] = '1';
                    break;
                case 2:
                    P4[0] = '1';
                    P4[1] = '0';
                    break;
                case 3:
                    P4[0] = '1';
                    P4[1] = '1';
                    break;
            }

            switch (s1result)   //create p4
            {
                case 0:
                    P4[2] = '0';
                    P4[3] = '0';
                    break;
                case 1:
                    P4[2] = '0';
                    P4[3] = '1';
                    break;
                case 2:
                    P4[2] = '1';
                    P4[3] = '0';
                    break;
                case 3:
                    P4[2] = '1';
                    P4[3] = '1';
                    break;
            }

            // permutate (actual p4)
            char[] temp = new char[4];
            temp[0] = P4[1];
            temp[1] = P4[3];
            temp[2] = P4[2];
            temp[3] = P4[0];

            for (int ii = 0; ii < 4; ii++) //add msbits to p4 result
            {
                if (l[ii] == temp[ii])
                {
                    l[ii] = '0';
                }
                else
                {
                    l[ii] = '1';
                }
            }

        }
        /**********************************************************************
        * Purpose: generates key 1 and key 2 from a user defined 10 bit key. 
        *
        * Precondition:
        *     none
        *
        * Postcondition:
        *      generates key 1 and 2 following the SDES algorithm.
        *
        ************************************************************************/
        public static void KeyGen()
        {
            string input = "";
            char[] p10 = new char[10];
            //char[] returnKey = new char [16];
            bool validKey = false;

            while (!validKey) //stays in the loop until the user enters a valid 10 bit key
            {
                validKey = true;
                input = Console.ReadLine();
                Console.WriteLine();
                bool isParsable = int.TryParse(input, out _);

                if (isParsable && input.Length == 10) //is the input a: 10 character string
                {                                       //that has only numbers
                    p10 = input.ToCharArray();
                    for (int ii = 0; ii < 10; ii++)
                    {
                        if (!p10[ii].Equals('1') && !p10[ii].Equals('0'))
                        {
                            validKey = false;
                        }
                    }
                    if (validKey == true)
                    {
                        p10[0] = input[2];
                        p10[1] = input[4];
                        p10[2] = input[1];
                        p10[3] = input[6];
                        p10[4] = input[3];

                        p10[5] = input[9];
                        p10[6] = input[0];
                        p10[7] = input[8];
                        p10[8] = input[7];
                        p10[9] = input[5]; //p10

                        char[] ls1LSB = { p10[1], p10[2], p10[3], p10[4], p10[0] };
                        char[] ls1MSB = { p10[6], p10[7], p10[8], p10[9], p10[5] }; //LS-1's

                        key1 = new char[] { ls1MSB[0], ls1LSB[2], ls1MSB[1], ls1LSB[3], ls1MSB[2], ls1LSB[4], ls1MSB[4], ls1MSB[3] }; //P8

                        char[] ls2LSB = { ls1LSB[2], ls1LSB[3], ls1LSB[4], ls1LSB[0], ls1LSB[1] };
                        char[] ls2MSB = { ls1MSB[2], ls1MSB[3], ls1MSB[4], ls1MSB[0], ls1MSB[1] }; //LS-2's

                        key2 = new char[] { ls2MSB[0], ls2LSB[2], ls2MSB[1], ls2LSB[3], ls2MSB[2], ls2MSB[0], ls2MSB[4], ls2MSB[3] }; //P8
                        //Console.WriteLine();
                        Console.Write("KEY 1: ");
                        Console.WriteLine(key1);
                        Console.Write("KEY 2: ");
                        Console.WriteLine(key2);
                        Console.WriteLine();
                    }
                }
                else
                {
                    validKey = false;
                    Console.Write("Invalid. Enter a key. A key is 10-bit number containing 1's and 0's: ");
                }
            }
        }
        /**********************************************************************
        * Purpose: Validates the user defined 8 bit number
        *
        * Precondition:
        *     none
        *
        * Postcondition:
        *   returns the valid 8 bit number inputted by the user.
        *
        ************************************************************************/
        public static char[] ValidateNum()
        {
            string input = "";
            //char[] returnKey = new char [16];
            char[] num = new char[8];
            bool validNum = false;

            while (!validNum)
            {
                validNum = true;
                input = Console.ReadLine(); //read in 8bits
                Console.WriteLine();
                bool isParsable = int.TryParse(input, out _);

                if (isParsable && input.Length == 8) //is the input a: 8 character string
                {                                       //that has only numbers
                    num = input.ToCharArray();
                    for (int ii = 0; ii < 8; ii++)
                    {
                        if (!num[ii].Equals('1') && !num[ii].Equals('0')) //if it isn't a 1 and it isn't a 0, num isn't valid.
                        {
                            validNum = false;
                        }
                    }
                    if (validNum == false)
                    {
                        //validNum = false;
                        Console.WriteLine("Invalid. Enter an 8 bit binary number containing 1's and 0's.");
                    }
                }
                else
                {
                    validNum = false;
                    Console.WriteLine("Invalid. Enter an 8 bit binary number containing 1's and 0's.");
                }
            }
            return num; //return the num if its valid
        }
    }
}
