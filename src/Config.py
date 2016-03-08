import src.DiffJob as DiffJob
import configparser
import time
import os

__author__ = 'George Herde'


class Config():
    def __init__(self, dir, required_files, due_date,
                 support_files=None, build=None,
                 diff_actions=None, unit_actions=None):
        self.dir = dir
        self.required_files = required_files
        self.due_date = due_date
        self.support_files = support_files
        self.build = build
        if diff_actions == None:
            self.diff_actions = []
        else:
            self.diff_actions = diff_actions
        if unit_actions == None:
            self.unit_actions = []
        else:
            self.unit_actions = unit_actions

    def __str__(self):
        return_string = "Directory: {}\n".format(self.dir)
        return_string += "Required files: {}\n".format(self.required_files)
        return_string += "Due Date: {}\n".format(self.due_date)
        return_string += "Supporting Files: {}\n".format(self.support_files)
        return_string += "Build command: {}\n".format(self.build)
        return_string += "List of Diff actions: "
        for item in self.diff_actions:
            return_string += "{}, ".format(item)
        return_string += "\nList of Unit Test actions: "
        for item in self.unit_actions:
            return_string += "{}, ".format(item)
        return return_string


def parse_config() -> Config:
    self = Config(dir=None, required_files=None, due_date=None)
    config = configparser.ConfigParser()
    config.read('config.ini')
    for section in config.sections():
        if str(section) == "Default":
            # Submission folder name
            self.dir = config['Default']['folder']
            # Comma separated list of the files required for submission
            self.required_files = str(config['Default']['source']).split(',')
            # Due Date Formatting:
            # {Number Day 01-31} {Abbreviated Month} {Full Year} {24-Hour}:{Minute}:{Second}--{Timezone}
            # Example: "05 Feb 2016 08:00:00--0500"
            self.due_date = time.strptime(config['Default']['due'], "%d %b %Y %H:%M:%S-%z")
            # Supporting files that are needed for grading purposes, can be empty
            # Example: Standardized Header file or a Makefile
            if 'support files' in config: self.support_files = config.get('Default', 'support files')
            # Build command (can be make), can be empty
            if 'build' in config: self.build = config.get('Default', 'build')
        else:
            section_header = str(section).split()
            item_name = config[section]['name']
            item_exe = config[section]['exe']
            item_in = config[section]['input']
            item_out = config[section]['output']
            if str(section_header[0]) == "Diff":
                diff_item = DiffJob(item_name, item_exe, item_in, item_out)
                self.diff_actions.append(diff_item)
            elif str(section_header[0] == "Unit"):
                unit_item = DiffJob(item_name, item_exe, item_in, item_out)
                self.unit_actions.append(unit_item)
    return self


def setup_config(args):
    pwd = os.getcwd()
    home_dir = os.path.expanduser('~')
    pwd = pwd.replace(home_dir, '~', 1)
    print("\nGRADING {}".format(args.grade))  # Print processing statement, to confirm selection
    print("Config file: {}/{}/config.ini".format(pwd, args.grade))  # Print config file which will be used
    try:
        os.chdir("./{}".format(args.grade))  # Move into the provided directory
        config_file = parse_config()
        os.chdir("../")
        # print(config_file) # Prints out processed config
        return config_file  # Load the config file
    except FileNotFoundError:
        print("Assignment not found, make sure the Grading folder is in this directory\n")
        import sys
        sys.exit()
