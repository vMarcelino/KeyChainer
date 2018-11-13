
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:42:45 2018

@author: Victor Marcelino
"""

import pythoncom
pythoncom.CoInitialize()

import clr
ref = clr.AddReference('KeyChainer.UI')
ref2 = clr.AddReference('MaterialDesignThemes.Wpf')
ref3 = clr.AddReference('MaterialDesignColors')
from KeyChainer.UI import MainWindow, ApplicationViewModel, RelayCommand, AppInitializer
from System import Action, Object, Array, String
from System.Windows import Application
from System.Threading import SynchronizationContext, SendOrPostCallback
from System.Windows.Threading import DispatcherSynchronizationContext
from System.Collections.ObjectModel import ObservableCollection

import command

from functools import wraps

import threading
import time 

print('imported')

class LogicThread(threading.Thread):
    def __init__(self, vm, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.vm = vm
        self.daemon = True
        self._running = True
        self.vm.RecordCommand = RelayCommand(Action(self.RecordCommand))
        self.vm.SaveCommand = RelayCommand(Action(self.SaveCommand))
        self.vm.AddCommand = RelayCommand(Action(self.AddCommand))
        self.vm.BrowseCommand = RelayCommand(Action(self.BrowseCommand))
        self.vm.DeleteCommand = RelayCommand(Action(self.DeleteCommand))
        self.vm.SelectionChanged = Action[int](self.SelectionChanged)
        self.update_list()

        # generate random string for space scaping
        import random, string
        self.space_escaping = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        

    def run(self):
        print(threading.currentThread().getName())
        print('THREAD START')


    def RecordCommand(self):
        if self.vm.IsRecording:
            self.vm.IsRecording = False
        else:
            self.vm.IsRecording = True
            self.vm.RecordedKeychain = ""


    def SaveCommand(self):
        parent.commands[self.vm.SelectedIndex] = command.Command(self.vm.RecordedKeychain, self.vm.ProgramPath, [x.replace(self.space_escaping, ' ') for x in self.vm.Arguments.replace('\ ', self.space_escaping).split(' ')] ) 
        parent.reader.dump_commands(parent.commands)
        self.update_list()


    def AddCommand(self):
        parent.commands.append(command.Command(self.vm.RecordedKeychain, self.vm.ProgramPath, [x.replace(self.space_escaping, ' ') for x in self.vm.Arguments.replace('\ ', self.space_escaping).split(' ')] ) )
        parent.reader.dump_commands(parent.commands)
        self.update_list()


    def DeleteCommand(self):
        del parent.commands[self.vm.SelectedIndex]
        self.update_list()


    def BrowseCommand(self):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(file_path)
        self.vm.ProgramPath = file_path


    def SelectionChanged(self, index):
        cmd = parent.commands[index]
        print(cmd)
        self.vm.RecordedKeychain = cmd.activation_chain
        self.vm.ProgramPath = cmd.program.program_path
        self.vm.Arguments = ' '.join([x.replace(' ', r'\ ') for x in cmd.program.arguments])


    def update_list(self):
        self.vm.CommandStrings = ObservableCollection[String]()
        for c in parent.commands:
            arg = ' '.join([x.replace(' ', r'\ ') for x in c.program.arguments])
            self.vm.CommandStrings.Add(f"{c.activation_chain} -> {c.program.program_path} {arg}")


    def stop(self):
        self._running = False



class UIThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        global _running
        _running = False
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        print('thread created')


    def run(self):
        global context
        print('starting ui loop')
        context = DispatcherSynchronizationContext()    
        print('context:', context)
        # start UI loop
        context.Send(SendOrPostCallback(self._initialize), None)
        print('done')
        
    def _initialize(self, state):
        print('init')
        global main_window, logic_thread, application, _running
        print('coinitializing')
        pythoncom.CoInitialize()
        print('coinitialized')
        main_window = MainWindow()
        main_window.DataContext = ApplicationViewModel()
        logic_thread = LogicThread(main_window.DataContext)
        logic_thread.start()
        application = Application()
        main_window.Hide()
        print('ai opened')
        _running = True
        application.Run()



def run_on_ui_thread(func):
    from inspect import signature
    arg_count = len(signature(func).parameters)
    if arg_count == 0:
        print('has no arg, converting')
        def decorator2(state):
            func()

        return run_on_ui_thread(decorator2)

    elif arg_count == 1:
        print('has one arg, decorating')
        @wraps(func)
        def decorator(arg=None):
            context.Send(SendOrPostCallback(func), arg)
        
        return decorator

    else:
        raise Exception('Must have at most one argument')


@run_on_ui_thread
def hide_window():
    main_window.Hide()
       

@run_on_ui_thread
def show_window():
    main_window.Show()


@run_on_ui_thread
def close_window():
    main_window.Close()


def on_key_down(key_name):
    if logic_thread.vm.IsRecording:
        logic_thread.vm.RecordedKeychain += key_name
        print('Recorded Keychain:', logic_thread.vm.RecordedKeychain)

def initialize(_parent):
    global parent, ui_thread
    parent = _parent
    ui_thread = UIThread()
    ui_thread.start()
    print('done')


parent = None
context = None
_running = False
logic_thread = None
main_window = None
application = None
ui_thread = None




        