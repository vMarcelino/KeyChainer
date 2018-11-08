class WinLowLevelHook:
    def __init__(self, keyboard_callback, mouse_callback):
        import collections
        self.keyboard_callback = keyboard_callback
        self.mouse_callback = mouse_callback
        self.KeyboardEvent = collections.namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                                                     'scan_code', 'alt_pressed',
                                                                     'time'])
                                             
        self.hook_id_keyboard = None
        self.hook_id_mouse = None
        
        
    def start(self):
        import win32con
        keyboard_event_types = {win32con.WM_KEYDOWN: 'key down',
                               win32con.WM_KEYUP: 'key up',
                               0x104: 'key down', # WM_SYSKEYDOWN, used for Alt key.
                               0x105: 'key up', # WM_SYSKEYUP, used for Alt key.
                              }
                      
        mouse_event_types = {win32con.WM_RBUTTONDOWN: 'RMB down',
                               win32con.WM_RBUTTONUP: 'RMB up',
                               win32con.WM_MOUSEMOVE: 'mouse move'
                             }

        def low_level_keyboard_handler(nCode, wParam, lParam):
            event = (nCode, self.KeyboardEvent(keyboard_event_types[wParam], lParam[0], lParam[1],
                                  lParam[2] == 32, lParam[3]))
                                  
            
            # Be a good neighbor and call the next hook.
            if self.keyboard_callback(event):
                return ctypes.windll.user32.CallNextHookEx(self.hook_id_keyboard, nCode, wParam, lParam)
            else:
                print("#")
                return 1
                
                
        def low_level_mouse_handler(nCode, wParam, lParam):
            event = (nCode, mouse_event_types.get(wParam, 'unknown'))
            

            if self.mouse_callback(event):
            # Be a good neighbor and call the next hook.
                return ctypes.windll.user32.CallNextHookEx(self.hook_id_mouse, nCode, wParam, lParam)
            else:
                return 1

            
        import ctypes
        CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int,ctypes. c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
        # Convert the Python handler into C pointer.
        pointer_keyboard = CMPFUNC(low_level_keyboard_handler)
        pointer_mouse = CMPFUNC(low_level_mouse_handler)

        import win32api
        # Hook both key up and key down events for common keys (non-system).
        self.hook_id_keyboard = ctypes.windll.user32.SetWindowsHookExA(win32con.WH_KEYBOARD_LL, pointer_keyboard,
                                                 win32api.GetModuleHandle(None), 0)
        self.hook_id_mouse = ctypes.windll.user32.SetWindowsHookExA(win32con.WH_MOUSE_LL, pointer_mouse,
                                                 win32api.GetModuleHandle(None), 0)

        # Register to remove the hook when the interpreter exits. Unfortunately a
        # try/finally block doesn't seem to work here.
        import atexit
        atexit.register(ctypes.windll.user32.UnhookWindowsHookEx, self.hook_id_keyboard)
        atexit.register(ctypes.windll.user32.UnhookWindowsHookEx, self.hook_id_mouse)

        while True:
            import win32gui
            #peek_result, msg = win32gui.PeekMessage(None, 0, 0, 1)
            result, msg = win32gui.GetMessage(None, 0, 0)
            print('got msg:', msg)
            win32gui.TranslateMessage(msg)
            #print('translated')
            win32gui.DispatchMessage(msg)
            #print('sent')
            #sleep(0.5)
            pass
        