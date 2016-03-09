import os
import subprocess
from Colorify import red, green

__author__ = 'George Herde'


def confirm_files(config) -> bool:
    required_files = config.required_files
    all_files = True
    for item in required_files:
        check = exists(item)
        if not check:
            all_files = False
        print("{}: {}".format(item, exists_string(check)))
    return all_files


def exists(filename) -> bool:
    for file in os.listdir(os.getcwd()):
        if file == filename:
            return True
    return False


def exists_string(boolean):
    if boolean:
        return "Exists"
    else:
        return red("MISSING")


def build(config):
    build_list = config.build.split(",")
    build_commands = []
    for item in build_list:
        build_commands.append(item.split(" "))
    for command in build_commands:
        output, error = subprocess.Popen(command).communicate()
        if output is not None:
            print(output)
        if error is not None:
            print(red("Error while building"))
            print(error)
            return False
    print("{}".format(green("Build Successful")))
    return True
