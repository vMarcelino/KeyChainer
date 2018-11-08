
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
    def __init__(self, vm):
        threading.Thread.__init__(self)
        
        self.vm = vm
        self.daemon = True
        self._running = True
        

    def run(self):
        print(threading.currentThread().getName())
        print('THREAD START')
        self.vm.RecordCommand = RelayCommand(Action(self.RecordCommand))


    def RecordCommand(self):
        self.vm.IsRecording = not self.vm.IsRecording


    def stop(self):
        self._running = False



mw = MainWindow()
mw.DataContext = ApplicationViewModel()
t = LogicThread(mw.DataContext)
t.start()

Application().Run(mw)

t.stop()









