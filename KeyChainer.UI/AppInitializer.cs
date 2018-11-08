using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace KeyChainer.UI
{
    public class AppInitializer
    {
        public static Application app;
        public static IAsyncResult result;
        public static Action<MainWindow> caller;
        public static MainWindow mw;
        public static ApplicationViewModel vm;

        [STAThread]
        public static void Open()
        {
            caller = (c) => 
            {
                app = new Application();
                app.Run(c);
            };
            mw = new MainWindow();
            mw.DataContext = vm = new ApplicationViewModel() { Text = "vatata" };
            result = caller.BeginInvoke(mw, null, null);
        }
        public static void Close()
        {
            caller.EndInvoke(result);
        }
    }
}
