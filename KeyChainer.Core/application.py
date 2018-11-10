class Application:
    def __init__(self):
        # spawn ui thread
        import ui_spawner
        ui_thread = ui_spawner.UIThread()
        ui_thread.start()

        # wait for the ui to initialize
        while not ui_thread._running: pass

        # import parser to pass on to keyboard hook
        import input_parser
        parser = input_parser.InputParser(ui=ui_thread)

        import win_low_level_hook
        keyboard_hook = win_low_level_hook.WinLowLevelHook(parser.process_keyboard_event, mouse_hook_callback)
        keyboard_hook.start()



def mouse_hook_callback(event):
    # print(event)
    return True


if __name__ == '__main__':
    Application()
    input()
    print('The End')