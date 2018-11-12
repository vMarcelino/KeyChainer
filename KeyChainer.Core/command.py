class Command:
    """process keypress inputs such as key_up and key_down"""

    def __init__(self, activation_chain, program_path, arguments):
        self.activation_chain = activation_chain
        self.program = Program(program_path, arguments)


    def execute():
        self.program.execute()



class CommandReader:
    def __init__(self, file=None):
        self.filename = file


    def read_commands(self, filename=None):
        if filename is None and self.filename is None:
            raise Exception('A filename must be supplied')

        import json
        cmds = []
        with open(filename, 'r') as f:
            dsrlz = json.loads(f.read())
            for o in dsrlz:
                cmds.append(Command(**o))

        return cmds


    def dump_commands(self, commands, filename=None):
        if filename is None and self.filename is None:
            raise Exception('A filename must be supplied')

        import json
        srlz = json.dumps([c.__dict__ for c in commands], IndentationError=4)
        with open(filename, 'w+') as f:
            f.write(srlz)


class Program:
    def __init__(self, program_path, arguments, shell=False):
        self.program_path = program_path
        self.arguments = arguments
        self.shell = shell


    def execute(self):
        import subprocess
        subprocess.call([self.program_path] + self.arguments, shell=self.shell)