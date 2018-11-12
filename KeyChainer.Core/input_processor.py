class InputProcessor:
    """process keypress inputs such as key_up and key_down"""

    def __init__(self, commands, keys_down=None, key_down_handlers = [], key_up_handlers = []):
        self.keys_down = keys_down
        self.key_chain = ""
        self.commands = commands
        self.command_input_mode=False
        self.key_down_handlers = key_down_handlers
        self.key_up_handlers = key_up_handlers

        if keys_down is None:
            self.outside_keys_down = False
            self.keys_down = set()
        else:
            self.outside_keys_down = True
            self.keys_down = keys_down

        self.allow_release = set()


    def on_key_down(self, key_name):
        if not self.outside_keys_down:
            self.keys_down.add(key_name)
            
        for handler in self.key_down_handlers:
            handler(key_name)

        if set(['F1' ,'LControlKey']) == self.keys_down:
            self.allow_release = self.keys_down.copy()
            self.command_input_mode = not self.command_input_mode


        if self.command_input_mode:
            self.key_chain += key_name
            valid = False
            while len(self.key_chain) > 0 and not valid:
                for command in self.commands:
                    if command.activation_chain.startswith(self.key_chain):
                        if command.activation_chain == self.key_chain:
                            self.command_input_mode = False
                            command.execute()
                        elif len(command.activation_chain) > len(self.key_chain):
                            valid = True

                print(f'chain valid: {valid} ({self.key_chain})')
                if not valid:
                    self.key_chain = self.key_chain[1:]
        else:
            self.key_chain = ""

        return not self.command_input_mode


    def on_key_up(self, key_name):
        if not self.outside_keys_down:
            try:
                self.keys_down.remove(key_name)
            except KeyError as ke:
                print('\nkey error:', ke)
            except Exception as ex:
                import exception_handler
                exception_handler.print_traceback(ex)

        for handler in self.key_up_handlers:
            handler(key_name)

        if key_name in self.allow_release:
            self.allow_release.remove(key_name)
            return True

        return not self.command_input_mode

