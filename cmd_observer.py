class CmdObserver:
    def __init__(self, command, name="hello"):
        self.command = command
        self.name = name

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value: str):
        print("set command to", value)
        self._command = value

    def execute(self):
        print("excute command", self.command)


class Cd(CmdObserver):
    pass


class Pwd(CmdObserver):
    pass


class Cat(CmdObserver):
    pass


class Ls(CmdObserver):
    pass


if __name__ == "__main__":
    cd = Cd("cd")
    cd.execute()

    ls = Ls("ls")
    ls.execute()
