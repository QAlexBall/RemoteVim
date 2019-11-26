import os
import click
from session import Session, read_config


class RemoteVim:
    def __init__(self, session):
        self.session = session

    def __str__(self):
        return "You are editing {}".format(self.session)

    def edit(self):
        return self.session.get_vim_command()


def update_current_path():
    pass


config = read_config()
username = config.get('username', None)
hostname = config.get('hostname', None)
port = config.get('port', None)
current_path = config.get('current_path', None)

rvim = RemoteVim(Session(username, hostname, port, current_path))
print(rvim.edit())


@click.command()
@click.option("--file", default=None)
def main(file):
    if file is not None:
        rvim.session.connect()
        _, stdout, _ = rvim.session.ssh.exec_command("ls " + rvim.session.current_path)
        print(stdout.read().decode())
        print("please enter 'y' to confirm edit this file!")
        edit = input()
        if edit == "y":
            os.system(rvim.edit() + '/{}'.format(file))


main()
