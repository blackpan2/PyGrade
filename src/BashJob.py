import os
import shutil

__author__ = 'George Herde'


class BashJob():
    def __init__(self, name, command):
        """

        :param name: provides a description of the test
        :param exe: the executable to be used for this diff job
        :param input: (file name, with extension) is the expected output from the diff job
        :param output: (file name, with extension) is the input file that will be provided for the diff job
        """
        self.name = name
        self.command = command

    def __str__(self):
        return "Bash Job:{}".format(str(self.name))

    def run(self):
        os.system("{}".format(self.command))
