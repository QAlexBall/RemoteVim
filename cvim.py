"""
RVim
TODO: How to keep this Session?
"""
import os
import json
import click
import paramiko


class Session:
    """ Create an Session for ssh connection"""

    def __init__(self, username, hostname, port, current_path="/"):
        self.username = username
        self.hostname = hostname
        self.port = port
        self.current_path = current_path
        self.ssh = None

    def __str__(self):
        return "{} in {} at {}".format(
            self.username,
            self.hostname,
            self.current_path
        )

    def connect(self):
        """ create ssh client """
        connection = False
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            ssh.connect(
                hostname=self.hostname, port=self.port, username=self.username)
            self.ssh = ssh
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
        if command_split[0] == "ls":
            command = "ls " + self.current_path
        return command


def read_config(config_path=None):
    if config_path is None:
        config_path = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
    config_file = open(config_path, 'r')
    config = json.load(config_file)
    config_file.close()
    return config


def change_current_path():
    pass


def write_config(config):
    config_path = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
    config_file = open(config_path, 'w')
    json.dump(config, config_file, indent=4)
    config_file.close()


@click.command()
@click.option("--username", default=None)
@click.option("--hostname", default=None)
@click.option("--port", default=None)
@click.option("--command", default="ls")
def main(username, hostname, port, command):
    config = read_config()

    username = username if username != config['username'] and username is not None else config['username']
    hostname = hostname if hostname != config['hostname'] and hostname is not None else config['hostname']
    port = port if port != config['port'] and port is not None else config['port']
    current_path = config['current_path']
    session = Session(username, hostname, port, current_path)
    connection = session.connect()
    if connection:
        print("[remote info] => \n[session] => in {}@{} at {}".format(
            username, hostname, current_path
        ))
        if username != config['username'] or hostname != config['hostname'] or port != config['port']:
            write_config()
        stdin, stdout, stderr = session.ssh.exec_command(session.analysis_command(command))
        print("[command] => " + command + '\n' + stdout.read().decode())
    else:
        print("[error] connection error! please check your input")


if __name__ == "__main__":
    main()
