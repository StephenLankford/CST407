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
        }

        private void DecryptClick(object sender, RoutedEventArgs e)
        {
            //TODO: Decrypt program logic here
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
