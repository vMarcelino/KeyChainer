using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
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
        public static SynchronizationContext uiContext;

        [STAThread]
        public static void Open()
        {
            uiContext = SynchronizationContext.Current;
            uiContext = new SynchronizationContext();


            Console.Write("\tSync Context: ");
            if (uiContext == null)
                Console.WriteLine("None");
            else
                Console.WriteLine(uiContext);

            Action<object> a = (o) => { };
            uiContext.Post(new SendOrPostCallback(a), null);

            //app = new Application();

        }

        public static void sync(SynchronizationContext c, Action<object> a)
        {
            c.Send(new SendOrPostCallback(a), null);
        }
    }
}
