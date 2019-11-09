"""
RVim
"""
import os
import json
import click
import paramiko


class Session:
    """ Create an Session for ssh connection"""

    def __init__(self, username, hostname, port, current_path):
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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            ssh.connect(
                hostname=self.hostname, port=self.port, username=self.username)
            self.ssh = ssh
        except Exception as e:
            return False


def read_config(config_path=None):
    if config_path is None:
        config_path = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
    config_file = open(config_path, 'r')
    config = json.load(config_file)
    config_file.close()
    return config


def write_config(new_path=None):
    config_path = os.path.abspath(os.path.dirname(__file__)) + "/config.json"


@click.command()
@click.option("--username", default=None)
@click.option("--hostname", default=None)
@click.option("--port", default=None)
@click.option("--command", default="ls")
def main(username, hostname, port, command):
    config = read_config()

    session = Session(username, hostname, port, "/")
    print(session)
    connection = session.connect()
    if not connection:
        if username != config['username'] or hostname != config['hostname'] or port != config['port']:
            write_config()
        stdin, stdout, stderr = session.ssh.exec_command(command)
        print(stdout.read().decode())
    else:
        print("[error] connection error! please check your input")


main()
