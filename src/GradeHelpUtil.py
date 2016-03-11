import os
import shutil
import subprocess
from Colorify import red, cyan
from DiffJob import prepare, diff, student_output

__author__ = 'George Herde'


def cd_into_assignment(top_level, student, config):
    # Tries to move into the assignment folder (as set in the config.ini) within the student's directory
    if os.path.exists("{}/{}/{}".format(top_level, student, config.dir)):
        os.chdir("{}/{}/{}".format(top_level, student, config.dir))
        return True
    else:
        # Provides a list of folders in the student's directory to use an an alternative
        alternate_dir = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and not d.startswith(".")]
        print("{} Not found.\nAlternate folders:".format(config.dir))
        print_array_of_strings(alternate_dir)
        target_dir = input("Choose an alternative(or 'None'): ")
        if target_dir == 'None':
            return False
        else:
            # Move into the chosen directory
            os.chdir("{}/{}/{}".format(top_level, student, target_dir))
            # Prints the name of the current folder back to the user
            print("\nUsing Directory: {}".format(os.path.relpath(os.getcwd(), start=os.getcwd() + "/..")))
            return True


def yes_no_question(question_text, y_default=True):
    if y_default:
        user_input = input("{} (Y/n)\n".format(question_text)).strip().lower()
        if user_input in "" or user_input in "y":
            return True
        else:
            return False
    else:
        user_input = input("{} (y/N)\n".format(question_text)).strip().lower()
        if user_input in "" or user_input in "n":
            return False
        else:
            return True


def print_array_of_strings(array):
    for element in array[:-1]:
        print("{}".format(element), end=", ")
    print("{}".format(array[-1]))


def move_support_files(config, config_location, destination):
    if config.support_files is not None:
        for item in config.support_files:
            if not os.path.exists("{}/{}".format(destination, item)):
                print(red("Supporting file missing {} into student repository".format(item)))
                shutil.copy("{}/{}".format(config_location, item), "{}/{}".format(destination, item))
    if config.grading_files is not None:
        for item in config.grading_files:
            print("Copying grading file: {} into student repository".format(item))
            shutil.copy("{}/{}".format(config_location, item), "{}/{}".format(destination, item))


def execute_testing(test_type, job_list, config_location=None):
    if test_type == "diff" and config_location is not None:
        execute_diff(job_list, config_location)
    elif test_type == "unit":
        execute_unit(job_list)
    elif test_type == "bash":
        execute_bash(job_list)


def execute_diff(job_list, config_location):
    for job in job_list:
        print("\n{}".format(cyan(job.__str__())))
        print("-------------------------------------------------------------")
        prepare(job, config_location, os.getcwd())
        student_output(job)
        diff(job)


def execute_unit(job_list):
    for job in job_list:
        print("\n{}".format(cyan(job.__str__())))
        print(cyan("-------------------------------------------------------------"))
        job.run()


def execute_bash(job_list):
    for bash in job_list[:-1]:
        print("\n{}".format(cyan(bash.__str__())))
        print(cyan("-------------------------------------------------------------"))
        bash.run()
        print("\n")
        input("Continue to next bash command...")
    bash = job_list[-1]
    print("\n{}".format(cyan(bash.name)))
    print(cyan("-------------------------------------------------------------"))
    bash.run()


def view_source(config):
    # View Source Files
    vim_array = ["vim", "-p"]
    vim_files = []
    for v_file in config.required_files:
        vim_files.append(v_file)
    if config.support_files is not None:
        for v_file in config.support_files:
            vim_files.append(v_file)
    print("Files opened: {}".format(vim_files))
    for file in vim_files:
        vim_array.append(str(file))
    subprocess.Popen(vim_array).communicate()
