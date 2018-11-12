using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;

namespace KeyChainer.UI
{
    public class ApplicationViewModel : BaseViewModel
    {
        public string RecordedKeychain { get; set; }

        public string Arguments { get; set; } = "";

        public string ProgramPath { get; set; }

        public ObservableCollection<String> CommandStrings { get; set; } = new ObservableCollection<String>();

        public string SelectedItem
        {
            get => _selectedItem;
            set
            {
                _selectedItem = value;
                Console.WriteLine(value);
                Console.WriteLine(SelectionChanged == null ? "selchng is null" : "selchang is NOT null");
                SelectionChanged?.Invoke(CommandStrings.IndexOf(value));
            }
        }

        public Action<int> SelectionChanged;

        private string _selectedItem;

        public int SelectedIndex => CommandStrings.IndexOf(SelectedItem);

        public ICommand RecordCommand { get; set; }

        public ICommand SaveCommand { get; set; }

        public bool IsRecording { get; set; }
    }
}