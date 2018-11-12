class Command:
    """process keypress inputs such as key_up and key_down"""

    def __init__(self, activation_chain, program_path, arguments):
        self.activation_chain = activation_chain
        self.program = Program(program_path, arguments)


    def execute():
        self.program.execute()


class Program:
    def __init__(self, program_path, arguments):
        self.program_path = program_path
        self.arguments = arguments


    def execute():
        raise NotImplementedError()