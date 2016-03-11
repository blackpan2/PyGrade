import os

__author__ = 'George Herde'


class UnitJob:
    def __init__(self, name, exe):
        """

        :param name: provides a description of the test
        :param exe: the executable to be used for this unit job
        """
        self.name = name
        self.exe = exe

    def __str__(self):
        return "Unit Job:{}".format(str(self.name))

    def run(self):
        base_command = "./" + str(self.exe)
        os.system(base_command)
