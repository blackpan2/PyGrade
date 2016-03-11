import os

__author__ = 'George Herde'


class BashJob:
    def __init__(self, name, command):
        """

        :param name: provides a description of the test
        :param command: the command to be executed by this bash job
        """
        self.name = name
        self.command = command

    def __str__(self):
        return "Bash Job:{}".format(str(self.name))

    def run(self):
        os.system("{}".format(self.command))
