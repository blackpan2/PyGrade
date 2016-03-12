import os
import subprocess
from Colorify import red, green, grey

__author__ = 'George Herde'


def confirm_files(config) -> bool:
    req_files = True
    print(grey("Required Files:"))
    for item in config.required_files:
        check = os.path.exists("{}/{}".format(os.getcwd(), item))
        if not check:
            req_files = False
        print("{}: {}".format(item, exists_string(check)))
    if config.support_files is not None:
        print("{}".format(config.support_files))
        print(grey("Supporting Files:"))
        for item in config.support_files:
            check = os.path.exists("{}/{}".format(os.getcwd(), item))
            print("{}: {}".format(item, exists_string(check)))
    print("\n")
    return req_files


def exists_string(boolean):
    if boolean:
        return green("Exists")
    else:
        return red("MISSING")


def build(config):
    build_list = config.build.split(",")
    build_commands = []
    for item in build_list:
        build_commands.append(item.split(" "))
    for command in build_commands:
        try:
            proc = subprocess.check_output(command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(red("Error or Warning while building"))
            return False
        subprocess.Popen(command).communicate()
    print("{}".format(green("Build Successful")))
    return True
