using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace homework2
{
    class Program
    {
        static void Main(string[] args)
        {
            string input = "";
            char[] key1 = new char [10];
            bool validKey = false;

            while (!validKey)
            {
                validKey = true;
                input = Console.ReadLine();

                bool isParsable = Int32.TryParse(input, out int keyTemp);

                if (isParsable && input.Length == 10) //is the input a: 10 character string
                {                                       //that have only numbers
                    key1 = input.ToCharArray();
                    for (int ii = 0; ii < 10; ii++)
                    {
                        if (!key1[ii].Equals('1') && !key1[ii].Equals('0'))
                        {
                            validKey = false;
                        }
                    }
                    if (validKey == true)
                    {
                        
                        key1[0] = input[2];
                        key1[1] = input[4];
                        key1[2] = input[1];
                        key1[3] = input[6];
                        key1[4] = input[3];
                        key1[5] = input[9];
                        key1[6] = input[0];
                        key1[7] = input[8];
                        key1[8] = input[7];
                        key1[9] = input[5];
                    }
                }
                else
                {
                    validKey = false;
                    System.Console.WriteLine("Invalid\n");
                }
            }

            System.Console.WriteLine(key1);
        }
    }
}
