import argparse
import Build
import Config
from Colorify import cyan
from DiffJob import student_output, diff, prepare
import GitFunction
from GradeHelpUtil import yes_no_question, print_array_of_strings, move_support_files
import subprocess
import os
import re
import BashJob

__author__ = 'George Herde'


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grade", help="assignment folder (containing config) to be graded")
    parser.add_argument("-s", "--student", help="provide a student's username to start at their folder")
    parser.add_argument("-p", "--pull", help="update all of the student repositories", action="store_true")
    parser.add_argument("-r", "--reset", help="reset all student repositories to their last commit",
                        action="store_true")
    return parser, parser.parse_args()


def get_student_directories(start=None):
    grade_list, excluded = [], []
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir):
            pattern = re.compile('^\w{2}\w?\d{4}$')
            if pattern.match(str(dir)):
                if start is None:
                    grade_list.append(dir)
                elif dir >= start:
                    grade_list.append(dir)
            else:
                excluded.append(dir)
    return grade_list, excluded


def main():
    """
    Main progression of the program
    :return: 0 if success
    """
    parser, args = init()

    if args.pull:
        print("pull")
    elif args.reset:
        print("reset")
    elif args.grade is not None:
        ###### Setup grading process
        config_file, config_location = Config.setup_config(args)

        ###### Generate list of student directories to be graded
        grade_list, excluded = get_student_directories(start=args.student)
        print("Starting Grading at: {}".format(grade_list[0]))
        print("Excluded: ", end="")
        print_array_of_strings(excluded)
        print("Loaded {} student repositories\n".format(len(grade_list)))

        ###### Reference to move program back to top level after finishing work on a student
        top_level = os.getcwd()

        ###### Iterate through the list of folders identified as student folders
        for student in grade_list:
            ###### Start the grading for a new student
            print("-------------------------------------------------------------")
            print("Grading:{} for Assignment:{}\n".format(student, config_file.dir))
            os.chdir("{}/{}".format(top_level, student))  # Go into the student's directory

            ###### Reset and then Update the student repository
            GitFunction.reset()
            GitFunction.pull()

            ###### Move into the assignment's directory
            try:
                # Tries to move into the assignment folder (as set in the config.ini) within the student's directory
                os.chdir("{}/{}/{}".format(top_level, student, config_file.dir))
            except FileNotFoundError:
                # Provides a list of folders in the student's directory to use an an alternative
                print("{} Not found.\nAlternate folders:{}".format(config_file.dir, os.listdir(os.getcwd())))
                dir = input("Choose an alternative:")
                # Move into the chosen directory
                os.chdir("{}/{}/{}".format(top_level, student, dir))
            # Prints the name of the current folder back to the user
            print("\nUsing Directory: {}".format(os.path.relpath(os.getcwd(), start=os.getcwd() + "/..")))

            ###### Git Log information
            GitFunction.log(config=config_file)
            print("-------------------------------------------------------------")

            ###### Prepare assignment folder by moving support files
            # move_support_files(config_file, config_location, os.getcwd())

            ###### Build student source
            if config_file.build is not None:
                ready_for_build = True
            else:
                ready_for_build = False
            if not Build.confirm_files(config=config_file):
                print("Directory Contains:")
                print_array_of_strings(os.listdir(os.getcwd()))
                ready_for_build = yes_no_question("\nMissing required files. Continue with build?", y_default=False)
            built = False
            if config_file.build is not None and ready_for_build:
                built = Build.build(config_file)

            ###### Diff Testing
            if len(config_file.diff_actions) != 0:
                if (yes_no_question("\nExecute to Diff Tests?")):
                    for job in config_file.diff_actions:
                        print("\n{}".format(cyan(job.__str__())))
                        print("-------------------------------------------------------------")
                        prepare(job, config_location, os.getcwd())
                        student_output(job)
                        diff(job)

            ###### Unit Testing
            if len(config_file.unit_actions) != 0:
                if (yes_no_question("\nExecute to Unit Tests?")):
                    for job in config_file.unit_actions:
                        pass
                        # print("\n{}".format(cyan(job.__str__())))
                        # print("-------------------------------------------------------------")
                        # prepare(job, config_location, os.getcwd())
                        # student_output(job)
                        # diff(job)


            ###### Extra bash commands
            if len(config_file.bash_actions) != 0:
                if (yes_no_question("\nExecute to Additional Bash?")):
                    for bash in config_file.bash_actions[:-1]:
                        print("\n{}".format(cyan(bash.__str__())))
                        print(cyan("-------------------------------------------------------------"))
                        bash.run()
                        print("\n")
                        input("Continue to next bash command...")
                    bash = config_file.bash_actions[-1]
                    print("\n{}".format(cyan(bash.name)))
                    print(cyan("-------------------------------------------------------------"))
                    bash.run()

            ###### View Source Files
            if yes_no_question("\nView source files?"):
                vim_array = ["vim", "-p"]
                print("Files opened: {}".format(config_file.required_files))
                for file in config_file.required_files:
                    vim_array.append(str(file))
                output, error = subprocess.Popen(vim_array).communicate()

            ###### Restore repository
            os.chdir('..')
            GitFunction.reset()

            ###### Go back to top level & proceed to next student
            os.chdir(top_level)
            if yes_no_question("\nContinue to next student"):
                print("")
            else:
                break  # Ends loop if stopped

    else:
        parser.print_help()
    print("\n")
    return 0


main()
