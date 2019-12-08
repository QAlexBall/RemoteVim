"""
RVim
Use to find correct file in remote host.
"""
import os
import json
import click
import paramiko
from utils.session_utils import write_config, read_config


class Session:
    """ Create an Session for ssh connection"""

    def __init__(self, username, hostname, port, current_path="/"):
        self.username = username
        self.hostname = hostname
        self.port = port
        self.current_path = current_path
        self.ssh = None
        self.connection = self.connect()

    def __str__(self):
        return "<Session> {} in {} at {}".format(
            self.username,
            self.hostname,
            self.current_path
        )

    def connect(self):
        """ create ssh client """
        connection = False
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username)
            connection = True
        except Exception as e:
            print(e)
        return connection

    def get_current_path(self):
        return self.current_path

    def get_vim_command(self):
        return "vim scp://{}@{}/{}".format(self.username, self.hostname, self.current_path)

    def analysis_command(self, command):
        """
        analysis command and do operation for every command
        TODO: support more command and operation
        """
        command_split = command.split(' ')
        command_split = list(filter(lambda x: x != "", command_split))
        if command_split[0] == "cd":
            _, stdout, _ = self.ssh.exec_command(self.analysis_command("ls " + self.current_path))
            stdout = stdout.read().decode()
            config = read_config()
            if len(command_split) == 2:
                if command_split[1] != "" and command_split[1] in stdout.split('\n'):
                    self.current_path = self.current_path + '/' + command_split[1] \
                        if self.current_path != "/" else self.current_path + command_split[1]
                    config['current_path'] = self.current_path
                    write_config(config)
                    print("[current_path] =>", self.current_path)
                elif command_split[1] == "..":
                    index = len(self.current_path) - (self.current_path[::-1].find('/') + 1)
                    self.current_path = self.current_path[:index] if self.current_path[:index] != "" else "/"
                    config['current_path'] = self.current_path
                    write_config(config)
                    print("[current_path] =>", self.current_path)
                else:
                    print("no such direction!")
            else:
                print("cd need only one input.")
        elif command_split[0] == "ls":
            command = "ls " + self.current_path
        return command

    def run_command(self, command):
        if self.connection:
            print("[remote info] => \n[session] => in {}@{} at {}".format(
                self.username, self.hostname, self.current_path
            ))
            stdin, stdout, stderr = self.ssh.exec_command(self.analysis_command(command))
            print("[command] => " + command + '\n' + stdout.read().decode())
        else:
            print("[error] connection error! please check your input")


def create_session(username, hostname, port, config_path):
    config = read_config()
    username = username if username != config['username'] and username is not None else config['username']
    hostname = hostname if hostname != config['hostname'] and hostname is not None else config['hostname']
    port = port if port != config['port'] and port is not None else config['port']
    current_path = config['current_path']
    if username != config['username'] or hostname != config['hostname'] or port != config['port']:
        config['username'] = username
        config['hostname'] = hostname
        config['port'] = port
        config['current_path'] = current_path = "~"
        write_config(config, config_path)
    session = Session(username, hostname, port, current_path)
    return session


def dispatcher(session):
    """
    as an consumer for command
    as an producer for output
    TODO:
     ------------------      -----------      -----------------
    | command_producer | => ｜dispatcher｜ => | output_consumer |
     ------------------      -----------      -----------------
    """

    command = yield
    while True:
        stdin, stdout, stderr = session.ssh.exec_command(session.analysis_command(command))
        print("[command] => " + command + '\n' + stdout.read().decode())
        output = stdout.read().decode()
        yield output


@click.command()
@click.option("--username", default=None)
@click.option("--hostname", default=None)
@click.option("--port", default=None)
@click.option("--config_path", default=None)
@click.option("--command", default="ls")
def main(username, hostname, port, command, config_path):
    session = create_session(username, hostname, port, config_path)
    session.run_command(command)


if __name__ == "__main__":
    main()
