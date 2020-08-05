using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

// The Blank Page item template is documented at https://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

namespace Blowfish
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {
        public MainPage()
        {
            this.InitializeComponent();
        }

        private void EncryptClick(object sender, RoutedEventArgs e)
        {
            //TODO: Encrypt program logic here
            //Suggestion: have user enter a key in the main menu for both
            //encryption and decryption.
            //Left side of data to be encrypted = L,
            //Right side = R.
            //TODO: find a way to generate an 18 uint32 array randomly using digits of pi (this is P)
            //TODO: figure out how user can enter data, and how it can be used in this function.
            //f is a function, x being the input to it. The function is on the following line
            //uint32_t h = S[0][x >> 24] + S[1][x >> 16 & 0xff];
            //return (h ^ S[2][x >> 8 & 0xff]) + S[3][x & 0xff]
            for (int ii = 0; ii < 16; ii += 2)
            {
                L ^= P[ii];
                R ^= f(L);
                R ^= P[ii + 1];
                L ^= f(R);
            }
            L ^= P[16];
            R ^= P[17];
            //swap L and R here
        }

        private void DecryptClick(object sender, RoutedEventArgs e)
        {
            //TODO: Decrypt program logic here
            //same issues apply in the encrypt function with the p array, f, and user input
            for (int ii = 0; ii < 16; ii += 2)
            {
                L ^= P[ii + 1];
                R ^= f(L);
                R ^= P[ii];
                L ^= f(R);
            }
            L ^= P[1];
            R ^= P[0];
            //swap L and R
        }

        private void RestartClick(object sender, RoutedEventArgs e)
        {
            //TODO: Restart program logic here
        }

        private void ExitClick(object sender, RoutedEventArgs e)    //exit program code
        {
            Application.Current.Exit();
        }

        private async void HelpClick(object sender, RoutedEventArgs e)  //help menu code
        {
            ContentDialog aboutDialog = new ContentDialog()
            {
                Title = "About Blowfish",
                Content = "Authors: Hayden Hutsell and Stephen Lankford, Summer 2020",
                CloseButtonText = "Ok"
            };
            await aboutDialog.ShowAsync();
        }
    }
}
