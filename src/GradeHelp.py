import argparse
import Build
import Config
import GitFunction
from GradeHelpUtil import yes_no_question, print_array_of_strings, move_support_files, cd_into_assignment, \
    execute_testing, view_source
import os
import re

__author__ = 'George Herde'


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grade", help="assignment folder (containing config) to be graded")
    parser.add_argument("-s", "--student", help="provide a student's username to start at their folder")
    parser.add_argument("-p", "--pull", help="update all of the student repositories", action="store_true")
    parser.add_argument("--reset", help="reset all student repositories to their last commit",
                        action="store_true")
    return parser, parser.parse_args()


def get_student_directories(start=None):
    grade_list, excluded = [], []
    if start is not None:
        start = start.rstrip('\/')
    for cur_dir in os.listdir(os.getcwd()):
        if os.path.isdir(cur_dir):
            pattern = re.compile('^\w{2}\w?\d{4}$')
            if pattern.match(str(cur_dir)):
                if start is None:
                    grade_list.append(cur_dir)
                elif cur_dir >= start:
                    grade_list.append(cur_dir)
            else:
                excluded.append(cur_dir)
    grade_list.sort()
    return grade_list, excluded


def main():
    """
    Main progression of the program
    :return: 0 if success
    """
    parser, args = init()

    if args.pull:
        print("Updating Student Repositories:")
        grade_list = get_student_directories()[0]
        print("Loaded {} student repositories\n".format(len(grade_list)))
        # Reference to move program back to top level after finishing work on a student
        top_level = os.getcwd()
        # Iterate through the list of folders identified as student folders
        for student in grade_list:
            os.chdir("{}/{}".format(top_level, student))  # Go into the student's directory
            GitFunction.pull()
            os.chdir(top_level)

    elif args.reset:
        print("Resetting Student Repositories:")
        grade_list = get_student_directories()[0]
        print("Loaded {} student repositories\n".format(len(grade_list)))
        # Reference to move program back to top level after finishing work on a student
        top_level = os.getcwd()
        # Iterate through the list of folders identified as student folders
        for student in grade_list:
            os.chdir("{}/{}".format(top_level, student))  # Go into the student's directory
            GitFunction.reset()
            os.chdir(top_level)

    elif args.grade is not None:
        # Setup grading process
        config_file, config_location = Config.setup_config(args)

        # Generate list of student directories to be graded
        grade_list, excluded = get_student_directories(start=args.student)
        print("Starting Grading at: {}".format(grade_list[0]))
        print("Excluded: ", end="")
        print_array_of_strings(excluded)
        print("Loaded {} student repositories\n".format(len(grade_list)))

        # Reference to move program back to top level after finishing work on a student
        top_level = os.getcwd()

        # Iterate through the list of folders identified as student folders
        for student in grade_list:

            # Start the grading for a new student
            print("-------------------------------------------------------------")
            print("Grading:{} for Assignment:{}\n".format(student, config_file.dir))
            os.chdir("{}/{}".format(top_level, student))  # Go into the student's directory

            # Reset and then Update the student repository
            GitFunction.reset()
            GitFunction.pull()

            # Move into the assignment's directory
            if cd_into_assignment(top_level=top_level, student=student, config=config_file):

                checkout = False
                # Git Log information
                if GitFunction.log(config=config_file):
                    if yes_no_question("Checkout to another commit?", y_default=False):
                        checkout = GitFunction.checkout(input("Hash:"))

                # Build student source (if needed)
                if Build.confirm_files(config=config_file):
                    ready_for_build = True
                else:
                    print("Directory Contains:")
                    print_array_of_strings(os.listdir(os.getcwd()))
                    ready_for_build = yes_no_question("\nMissing required files. Continue with build?", y_default=False)

                built = ready_for_build  # This sets built to True if compiling isn't required
                if config_file.build is not None and ready_for_build:
                    # Prepare assignment folder by moving support files
                    move_support_files(config_file, config_location, os.getcwd())
                    built = Build.build(config_file)

                if not built:
                    built = yes_no_question("\nError or warning while build. Would you like to continue?",
                                            y_default=False)

                if built:
                    if len(config_file.diff_actions) != 0:
                        # Diff Testing
                        if yes_no_question("\nExecute to Diff Tests?"):
                            execute_testing("diff", config_file.diff_actions, config_location)

                    if len(config_file.unit_actions) != 0:
                        # Unit Testing
                        if yes_no_question("\nExecute to Unit Tests?"):
                            execute_testing("unit", config_file.unit_actions)

                    if len(config_file.bash_actions) != 0:
                        # Extra bash commands
                        if yes_no_question("\nExecute Additional Bash?"):
                            execute_testing("bash", config_file.bash_actions)

                if yes_no_question("\nView source files?"):
                    view_source(config_file)

                # Restore repository
                os.chdir("{}/{}".format(top_level, student))  # Go into the student's directory
                GitFunction.reset(checkout_executed=checkout)

                # Go back to top level & proceed to next student
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
