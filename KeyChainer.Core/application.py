class Application:
    def __init__(self):
        # loads commands
        import command
        self.reader = command.CommandReader('Keychains.txt')
        try:
            self.commands = self.reader.read_commands()
        except:
            self.commands = [command.Command('NP', 'notepad.exe', ['batata crua.txt']), command.Command('PS', 'powershell', [])]
            self.reader.dump_commands(self.commands)


        # spawn ui thread
        import user_interface
        user_interface.initialize(self)

        # wait for the ui to initialize
        while not user_interface._running:
            pass

        user_interface.show_window()

        # uses key_down set in here, main application class
        self.keys_down = set()

        # import processor and add ui key handlers
        import input_processor
        self.processor = input_processor.InputProcessor(commands=self.commands, keys_down=self.keys_down, key_down_handlers=[user_interface.on_key_down])

        # import parser to pass on to keyboard hook
        import input_parser
        self.parser = input_parser.InputParser(keys_down = self.keys_down, key_up_callback=self.processor.on_key_up, key_down_callback=self.processor.on_key_down)

        # hook keyboard and mouse
        import win_low_level_hook
        self.keyboard_hook = win_low_level_hook.WinLowLevelHook(self.parser.process_keyboard_event, mouse_hook_callback)
        self.keyboard_hook.start()



def mouse_hook_callback(event):
    # print(event)
    return True


if __name__ == '__main__':
    print('start')
    Application()
    input()
    print('The End')