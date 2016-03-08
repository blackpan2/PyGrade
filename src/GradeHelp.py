import argparse
import os
import Config
import re
import GitFunction

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
    print("Starting grading at: {}".format(grade_list[0]))
    print("Excluded:", end="")
    for element in excluded:
        print("{}".format(element), end=", ")
    print("\nLoaded {} student repositories".format(len(grade_list)))
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
        config_file = Config.setup_config(args)

        ### Generate list of student directories to be graded
        grade_list = get_student_directories(start=args.student)

        for student in grade_list:
            print("-------------------------------------------------------------")
            print("Grading:{} for Assignment:{}".format(student, config_file.dir))
            os.chdir("./{}".format(student))  # Go into the student's directory
            try:
                os.chdir("./{}".format(config_file.dir))  # Try to move into the assignment directory
                GitFunction.pull()
                os.chdir("../")
            except FileNotFoundError:
                print("{} Not found.\nAlternate folders:{}".format(config_file.dir, os.listdir(os.getcwd())))
                os.chdir(input("Choose an alternative:"))
                os.chdir("../")
            os.chdir("../")

    else:
        parser.print_help()

    print("\n")
    return 0


main()
