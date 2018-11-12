class InputProcessor:
    """process keypress inputs such as key_up and key_down"""

    def __init__(self, commands, keys_down=None):
        self.keys_down = keys_down
        self.key_chain = ""
        self.commands = commands
        self.command_input_mode=False
        if keys_down is None:
            self.outside_keys_down = False
            self.keys_down = set()
        else:
            self.outside_keys_down = True
            self.keys_down = keys_down


    def on_key_down(self, key_name):
        if not self.outside_keys_down:
            self.keys_down.add(key_name)

        self.key_chain += key_name
        while len(self.key_chain) > 0:
            is_valid = False
            for command in self.commands:
                if comamnd.activation_chain.startswith(self.key_chain):
                    if command.activation_chain == self.key_chain:
                        command.activate()
                    elif len(command.activation_chain) > self.key_chain:
                        is_valid = True

            if not is_valid:
                self.key_chain = self.key_chain[1:]

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

        return not self.command_input_mode

