import argparse
import subprocess
from Colorify import cyan
import Config
import GitFunction
from GradeHelpUtil import yes_no_question, print_array_of_strings
import Build
from DiffJob import student_output, diff, prepare
import os
import re

__author__ = 'George Herde'


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grade", help="assignment folder (containing config) to be graded")
    parser.add_argument("-s", "--student", help="provide a student's username to start at their folder")
    parser.add_argument("-p", "--pull", help="update all of the student repositories", action="store_true")
    parser.add_argument("-r", "--reset", help="reset all student repositories to their last commit",
                        action="store_true")
    return parser


def get_student_directories(start=None):
    grade_list, excluded = [], []
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir):
            pattern = re.compile("^\w{2}\w?\d{4}$")
            if pattern.match(str(dir)):
                if start is None:
                    grade_list.append(dir)
                elif dir >= start:
                    grade_list.append(dir)
            else:
                excluded.append(dir)
    print("Starting Grading at: {}".format(grade_list[0]))
    print("Excluded: ", end="")
    print_array_of_strings(excluded)
    print("Loaded {} student repositories\n".format(len(grade_list)))
    return grade_list


def main():
    """
    Main progression of the program
    :return: 0 if success
    """
    parser = init()
    args = parser.parse_args()

    if args.pull:
        print("pull")
    elif args.reset:
        print("reset")
    elif args.grade is not None:
        ### Setup grading process
        config_file, config_location = Config.setup_config(args)

        ### Generate list of student directories to be graded
        grade_list = get_student_directories(start=args.student)

        ### Reference to move program back to top level after finishing work on a student
        top_level = os.getcwd()

        for student in grade_list:
            print("-------------------------------------------------------------")
            print("Grading:{} for Assignment:{}\n".format(student, config_file.dir))
            os.chdir("./{}".format(student))  # Go into the student's directory
            GitFunction.pull()
            try:
                os.chdir("./{}".format(config_file.dir))  # Try to move into the assignment directory
            except FileNotFoundError:
                print("{} Not found.\nAlternate folders:{}".format(config_file.dir, os.listdir(os.getcwd())))
                os.chdir(input("Choose an alternative:"))

            print("\nUsing Directory: {}".format(os.path.relpath(os.getcwd(), start=os.getcwd() + "/..")))
            GitFunction.log(config=config_file)
            print("-------------------------------------------------------------")

            if config_file.build is not None:
                build = True
            else:
                build = False
            if not Build.confirm_files(config=config_file):
                print("Directory Contains:")
                print_array_of_strings(os.listdir(os.getcwd()))
                build = yes_no_question("\nMissing required files. Continue with build?", y_default=False)

            built = False
            if config_file.build is not None and build:
                built = Build.build(config_file)

            diff_testing = False
            if config_file.diff_actions is not None:
                diff_testing = True

            if diff_testing:
                yes_no_question("\nExecute to Diff Tests?")
                for job in config_file.diff_actions:
                    print("\n{}".format(cyan(job.__str__())))
                    print("-------------------------------------------------------------")
                    prepare(job, config_location, os.getcwd())
                    student_output(job)
                    diff(job)

            unit_testing = False
            if config_file.build is not None and build:
                if not built:
                    built = True
                    unit_testing = Build.build(config_file)
            elif config_file.build is None and config_file.unit_actions is not None:
                unit_testing = True

            if unit_testing:
                pass

            if yes_no_question("View source files?"):
                vim_array = ["vim","-p"]
                print("Files opened: {}".format(config_file.required_files))
                for file in config_file.required_files:
                    vim_array.append(str(file))
                output, error = subprocess.Popen(vim_array).communicate()

            os.chdir('..')
            GitFunction.reset()
            os.chdir(top_level)
            if yes_no_question("\nContinue to next student"):
                print("")
            else:
                break

    else:
        parser.print_help()

    print("\n")
    return 0


main()
