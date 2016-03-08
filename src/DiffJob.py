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

    def create_student_output(self):
        bashCommand = "./" + str(self.exe) + " < " + str(self.input) + " > " + str(self.student_output)
        return bashCommand

    def create_diff_bash(self):
        if self.student_output :
            return "diff " + str(self.student_output) + " " + self.output

    def clean(self):
        bashCommand = ["rm -f " + str(self.input),
                       "rm -f " + str(self.output),
                       "rm -f " + str(self.student_output),
                       "rm -f " + str(self.exe) + " \n"]
        return bashCommand

    def __str__(self):
        return "DiffJob:{}".format(str(self.name))