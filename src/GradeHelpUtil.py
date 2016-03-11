import os
import shutil
from Colorify import red

__author__ = 'George Herde'


def cd_into_assignment(top_level, student, config):
    # Tries to move into the assignment folder (as set in the config.ini) within the student's directory
    if os.path.exists("{}/{}/{}".format(top_level, student, config.dir)):
        os.chdir("{}/{}/{}".format(top_level, student, config.dir))
        return True
    else:
        # Provides a list of folders in the student's directory to use an an alternative
        print("{} Not found.\nAlternate folders:{}".format(config.dir, os.listdir(os.getcwd())))
        target_dir = input("Choose an alternative(or 'None'): ")
        if target_dir == 'None':
            return False
        else:
            # Move into the chosen directory
            os.chdir("{}/{}/{}".format(top_level, student, target_dir))
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
    for item in config.support_files:
        if os.path.exists("{}/{}".format(destination, item)):
            pass
        else:
            print(red("Supporting file missing {} into student repository".format(item)))
            shutil.copy("{}/{}".format(config_location, item), "{}/{}".format(destination, item))
    for item in config.grading_files:
        print("Copying grading file: {} into student repository".format(item))
        shutil.copy("{}/{}".format(config_location, item), "{}/{}".format(destination, item))