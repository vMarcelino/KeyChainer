class Application:
    def __init__(self):
        # spawn ui thread
        import user_interface

        # wait for the ui to initialize
        while not user_interface._running:
           pass

        user_interface.show_window()

        self.keys_down = set()

        # import parser to pass on to keyboard hook
        import input_parser
        parser = input_parser.InputParser(keys_down = self.keys_down)

        import win_low_level_hook
        keyboard_hook = win_low_level_hook.WinLowLevelHook(parser.process_keyboard_event, mouse_hook_callback)
        keyboard_hook.start()



def mouse_hook_callback(event):
    # print(event)
    return True


if __name__ == '__main__':
    print('start')
    Application()
    input()
    print('The End')