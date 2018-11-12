
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:42:45 2018

@author: Victor Marcelino
"""

import pythoncom
pythoncom.CoInitialize()

import clr
ref = clr.AddReference('KeyChainer.UI')
from KeyChainer.UI import MainWindow, ApplicationViewModel, RelayCommand, AppInitializer
from System import Action, Object
from System.Windows import Application
from System.Threading import SynchronizationContext, SendOrPostCallback
from System.Windows.Threading import DispatcherSynchronizationContext

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
        

    def run(self):
        print(threading.currentThread().getName())
        print('THREAD START')


    def RecordCommand(self):
        self.vm.IsRecording = not self.vm.IsRecording


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



print('classes defined')

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


context = None
_running = False
logic_thread = None
main_window = None
application = None
print('creating thread')
ui_thread = UIThread()
print('starting thread')
ui_thread.start()
print('done')




        