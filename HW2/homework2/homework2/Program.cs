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
            FK(ref left, ref right);    //by ref or by value?
        }

        public void FK(ref char[] l, ref char[] r)
        {
            //TODO
            char[] EP1 = { l[3], l[0], l[1], l[2], l[1], l[2], l[3], l[0] };

            for (int i = 0; i < 8; i++)
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

            char[,] s0 = new char[4,4] { { EP1[1], EP1[0], EP1[3], EP1[2] },
                                         { EP1[3], EP1[2], EP1[1], EP1[0] },
                                         { EP1[0], EP1[2], EP1[1], EP1[3] },
                                         { EP1[3], EP1[1], EP1[3], EP1[2] }  }; //2D should be numbers not the index of EP1 eg 1,0,3,2
            char[,] s1 = new char[4,4] { { EP1[4], EP1[5], EP1[6], EP1[7] },
                                         { EP1[6], EP1[4], EP1[5], EP1[7] },
                                         { EP1[7], EP1[4], EP1[5], EP1[4] },
                                         { EP1[6], EP1[5], EP1[4], EP1[7] }  }; //2D should be numbers not the index of EP1 eg 1,0,3,2

            Switch(ref l, ref r);
        }

        public void Switch(ref char[] l, ref char[] r)
        {
            //TODO
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
                {                                       //that have only numbers
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

                        key1 = new char[] { ls1MSB[0], ls1LSB[2], ls1LSB[1], ls1LSB[3], ls1MSB[2], ls1MSB[0], ls1MSB[4],ls1MSB[3]};

                        char[] ls2LSB = { ls1LSB[2], ls1LSB[3],ls1LSB[4],ls1LSB[0],ls1LSB[1]};
                        char[] ls2MSB = {ls1MSB[2], ls1MSB[3],ls1MSB[4],ls1MSB[0],ls1MSB[1]};

                        key2 = new char[] {ls2MSB[0], ls2LSB[2], ls2MSB[1], ls2LSB[3], ls2MSB[2], ls2MSB[0], ls2MSB[4], ls2MSB[3]};
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
