
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

# ai = AppInitializer()
# ai.Open()

import threading
import time 

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
        self._running = False
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.application = None
        self.mw = None
        self.context = None


    def run(self):
        # set sync context
        self.context = DispatcherSynchronizationContext()

        # allow use of context
        self._running = True

        # start UI loop
        self.context.Send(SendOrPostCallback(self._initialize), None)


    def run_as_ui_thread(self, func):
        self.context.Send(SendOrPostCallback(func), None)

    def show_window(self):
        self.context.Send(SendOrPostCallback(self._show_window), None)
   
       
    def _show_window(self, state):
        self.mw.Show()

        
    def hide_window(self):
        self.context.Send(SendOrPostCallback(self._hide_window), None)
   
       
    def _hide_window(self, state):
        #SynchronizationContext.SetSynchronizationContext(self.context)
        self.mw.Hide()


    def close_window(self):
        self.context.Send(SendOrPostCallback(self._close_window), None)


    def _close_window(self):
        self.mw.Close()


    def _initialize(self, state):
        pythoncom.CoInitialize()
        print('coinitialized')
        self.mw = MainWindow()
        self.mw.DataContext = ApplicationViewModel()
        self.t = LogicThread(self.mw.DataContext)
        self.t.start()
        self.application = Application()
        self.mw.Hide()
        print('ai opened')
        self.application.Run()









        