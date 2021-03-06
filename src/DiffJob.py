import os
import shutil

__author__ = 'George Herde'


class DiffJob:
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

    def __str__(self):
        return "DiffJob:{}".format(str(self.name))


def prepare(job, config_location, destination):
    shutil.copy("{}/{}".format(config_location, job.input), "{}/{}".format(destination, job.input))
    shutil.copy("{}/{}".format(config_location, job.output), "{}/{}".format(destination, job.output))


def student_output(job):
    bash_command = "./" + str(job.exe) + " < " + str(job.input) + " > " + str(job.student_output)
    os.system(bash_command)


def diff(job):
    bash_command = "diff -b " + str(job.student_output) + " " + job.output
    os.system(bash_command)
