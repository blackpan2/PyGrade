import os
import subprocess
from Colorify import red
import shutil

__author__ = 'George Herde'


class DiffJob():
    def __init__(self, name, exe, input, output):
        """

        :param name: provides a description of the test
        :param exe: the executable to be used for this diff job
        :param input: (file name, with extension) is the expected output from the diff job
        :param output: (file name, with extension) is the input file that will be provided for the diff job
        """
        self.name = name
        self.exe = exe
        self.input = input
        self.output = output
        self.student_output = "student_out.txt"

    def clean(self):
        bashCommand = ["rm -f " + str(self.input),
                       "rm -f " + str(self.output),
                       "rm -f " + str(self.student_output),
                       "rm -f " + str(self.exe) + " \n"]
        return bashCommand

    def __str__(self):
        return "DiffJob:{}".format(str(self.name))


def prepare(job, config_location, destination):
    shutil.copy("{}/{}".format(config_location, job.input), "{}/{}".format(destination, job.input))
    shutil.copy("{}/{}".format(config_location, job.output), "{}/{}".format(destination, job.output))


def student_output(job):
    bashCommand = "./" + str(job.exe) + " < " + str(job.input) + " > " + str(job.student_output)
    os.system(bashCommand)


def diff(job):
    bashCommand = "diff " + str(job.student_output) + " " + job.output
    os.system(bashCommand)
