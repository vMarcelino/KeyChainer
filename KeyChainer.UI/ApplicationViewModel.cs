using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;

namespace KeyChainer.UI
{
    public class ApplicationViewModel : BaseViewModel
    {
        public string Text { get; set; }

        public ICommand RecordCommand { get; set; }

        public bool IsRecording { get; set; }
    }
}
