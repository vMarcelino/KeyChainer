
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:42:45 2018

@author: Victor Marcelino
"""

import pythoncom
pythoncom.CoInitialize()

import clr
ref = clr.AddReference('KeyChainer.UI')
from KeyChainer.UI import MainWindow, ApplicationViewModel, RelayCommand
from System import Action
from System.Windows import Application


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
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self._running = True
        self.application = None
        self.mw = None


    def run(self):
        pythoncom.CoInitialize()
        self.mw = MainWindow()
        self.mw.DataContext = ApplicationViewModel()
        self.t = LogicThread(self.mw.DataContext)
        self.t.start()
        self.application = Application()
        self.mw.Hide()
        self.application.Run(self.mw)


    def show_window(self):
        self.mw.Show()

    def close_window(self):
        self.mw.Close()









