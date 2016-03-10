import shutil

__author__ = 'George Herde'


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
        shutil.copy("{}/{}".format(config_location, item), "{}/{}".format(destination, item))