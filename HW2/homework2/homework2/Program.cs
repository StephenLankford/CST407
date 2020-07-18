﻿/******************************************************************************************************************
 * Programmers: Hayden Hutsell and Stephen Lankford
 * Assignment: 2 - SDES
 * Date Started: 07/14/2020
 * Updates:     07/14/2020 - work on SDES key gen, started SDES encryption steps
 *              07/14/2020 - FK and switch finished
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

        int[,] s0 = new int[4, 4] { { 1, 0, 3, 2 },
                                    { 3, 2, 1, 0 },
                                    { 0, 2, 1, 3 },
                                    { 3, 1, 3, 2 }  }; //2D 
        int[,] s1 = new int[4, 4] { { 0, 1, 2, 3 },
                                    { 2, 0, 1, 3 },
                                    { 3, 0, 1, 0 },
                                    { 2, 1, 0, 3 }  }; //2D 

        public static void Main(string[] args) 
        {
            //char[] key1 = new char[8];
            //char[] key2 = new char[8];
            string input = "";
            
            bool validInput = false;

            Console.WriteLine("Enter a key: ");
            KeyGen(key1, key2);
            validInput = false;
            
            while(!validInput)
            {
                Console.WriteLine("encrypt, decrypt, or quit: ");
                input = Console.ReadLine();

                if (input.Contains("encrypt") ^ input.Contains("decrypt") && !input.Contains("quit"))
                { 

                }



            }
            

            
          
        }

        public void Encryption(char[] input)   //by reference or by value?
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

            //call FK
            FK(ref left);    //ref needed
            Switch(ref left, ref right);  //ref needed
            FK(ref left);    //inverse IP created
            //next call?
        }

        public void FK(ref char[] l)
        {
            //expansion/permutation
            char[] EP1 = { l[3], l[0], l[1], l[2], l[1], l[2], l[3], l[0] };

            //variables
            char[] P4 = { '0', '0', '0', '0' };
            int[] rowCol0 = { 0, 0 };   //for s0
            int[] rowCol1 = { 0, 0 };   //for s1
            int s0result = 0, s1result = 0;

            for (int i = 0; i < 8; i++) //8-bit subkey added to EP using XOR
            {
                if (key1[i] == EP1[i])
                {
                    EP1[i] = '0';
                }
                else if (key1[i] != EP1[i])
                {
                    EP1[i] = '1';
                }
            }

            //first and fourth bits are the row
            //second and third bits are the column
            //EP1[0] = p0,0, EP1[1] = p0,1, EP1[2] = p0,2, EP1[3] = p0,3, 
            //EP1[4] = p1,0, EP1[5] = p1,1, EP1[6] = p1,2, EP1[7] = p1,3
            for (int i = 0, j = 3; i < 2; i++, j--)
            {
                switch (EP1[i]) //row
                {
                    case '0':
                        switch (EP1[j])
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
                        switch (EP1[j])
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

                switch (EP1[i + 4]) //column
                {
                    case '0':
                        switch (EP1[j + 4])
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
                        switch (EP1[j + 4])
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
            }

            //s box magic
            s0result = s0[rowCol0[0], rowCol0[1]];  //grab sbox 0 value
            s1result = s1[rowCol1[0], rowCol1[1]];  //grab sbox 1 value
            switch (s0result)   //create p4
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

            //finalize P4 aka fK output
            l[0] = P4[1];
            l[1] = P4[3];
            l[2] = P4[2];
            l[3] = P4[0];
        }

        public void Switch(ref char[] l, ref char[] r)
        {
            char[] tempR = { l[0], l[1], l[2], l[3] };
            char[] tempL = { r[0], r[1], r[2], r[3] };

            l[0] = tempL[0];
            l[1] = tempL[1];
            l[2] = tempL[2];
            l[3] = tempL[3];

            r[0] = tempR[0];
            r[1] = tempR[1];
            r[2] = tempR[2];
            r[3] = tempR[3];
        }

        public static void KeyGen(char[] key1, char[] key2)
        {
           string input = "";
            char[] p10 = new char [10];
            //char[] returnKey = new char [16];
            bool validKey = false;

            while (!validKey)
            {
                validKey = true;
                input = Console.ReadLine();
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

                        char[] ls1LSB = {p10[1], p10[2],p10[3],p10[4],p10[0]};
                        char[] ls1MSB = {p10[6], p10[7],p10[8],p10[9],p10[5]};

                        key1 = new char[] { ls1MSB[0], ls1LSB[2], ls1LSB[1], ls1LSB[3], ls1MSB[2], ls1MSB[0], ls1MSB[4],ls1MSB[3] };

                        char[] ls2LSB = { ls1LSB[2], ls1LSB[3],ls1LSB[4],ls1LSB[0],ls1LSB[1] };
                        char[] ls2MSB = { ls1MSB[2], ls1MSB[3],ls1MSB[4],ls1MSB[0],ls1MSB[1] };

                        key2 = new char[] { ls2MSB[0], ls2LSB[2], ls2MSB[1], ls2LSB[3], ls2MSB[2], ls2MSB[0], ls2MSB[4], ls2MSB[3] };
                        //returnKey = {key1, key2}; 
                    }
                }
                else
                {
                    validKey = false;
                    Console.WriteLine("Invalid. Enter a key. A key is 10 bit number containing 1's and 0's.\n");
                }
            }
        }
    }
}