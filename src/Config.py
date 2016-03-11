import configparser
import time
import os
import BashJob
from GradeHelpUtil import print_array_of_strings
import UnitJob
import DiffJob

__author__ = 'George Herde'


class Config:
    def __init__(self, assignment_dir, required_files, due_date,
                 support_files=None, grading_files=None,
                 build=None, diff_actions=None,
                 unit_actions=None, bash_actions=None,
                 rubric=False):
        self.dir = assignment_dir
        self.required_files = required_files
        self.due_date = due_date
        self.support_files = support_files
        self.build = build
        if diff_actions is None:
            self.diff_actions = []
        else:
            self.diff_actions = diff_actions
        if unit_actions is None:
            self.unit_actions = []
        else:
            self.unit_actions = unit_actions
        if bash_actions is None:
            self.bash_actions = []
        else:
            self.bash_actions = bash_actions
        if grading_files is None:
            self.grading_files = []
        else:
            self.grading_files = grading_files
        self.rubric = rubric

    def __str__(self):
        return_string = "Directory: {}\n".format(self.dir)
        return_string += "Required files: {}\n".format(print_array_of_strings(self.required_files))
        return_string += "Due Date: {}\n".format(self.due_date)
        return_string += "Supporting Files: {}\n".format(print_array_of_strings(self.support_files))
        return_string += "Grading Files: {}\n".format(print_array_of_strings(self.grading_files))
        return_string += "Build commands: {}\n".format(self.build)
        return_string += "List of Diff actions: {}\n".format(print_array_of_strings(self.diff_actions))
        return_string += "List of Unit Test actions: {}\n".format(print_array_of_strings(self.unit_actions))
        return_string += "List of Bash actions: {}\n".format(print_array_of_strings(self.bash_actions))
        return return_string


def parse_config(rubric) -> Config:
    config_obj = Config(assignment_dir=None, required_files=None, due_date=None, rubric=rubric)
    config = configparser.ConfigParser()
    config.read('config.ini')
    for section in config.sections():
        if str(section) == "Default":
            default = config['Default']
            # Submission folder name
            config_obj.dir = default['folder']
            # Comma separated list of the files required for submission
            config_obj.required_files = str(default['source']).split(',')
            # Due Date Formatting:
            # {Number Day 01-31} {Abbreviated Month} {Full Year} {24-Hour}:{Minute}:{Second}--{Timezone}
            # Example: "05 Feb 2016 08:00:00--0500"
            config_obj.due_date = time.strptime(default['due'], "%d %b %Y %H:%M:%S-%z")
            # Supporting files that are needed for compiling, can be empty
            # Example: Standardized Header file or a Makefile
            if 'support files' in default:
                config_obj.support_files = str(default['support files']).split(',')
            # Grading files that are files that are needed for compiling and required to be consistent
            # (you provide a version for all students, it will replace their version), this field can be empty
            # Example: Standardized Header file or a Makefile
            if 'grading files' in default:
                config_obj.grading_files = str(default['grading files']).split(',')

            # Build command (can be make), can be empty
            if 'build' in default:
                config_obj.build = default['build']
        else:
            section_header = str(section).split()
            item_name = config[section]['name']
            if "Diff" == str(section_header[0]):
                item_exe = config[section]['exe']
                item_in = config[section]['input']
                item_out = config[section]['output']
                diff_item = DiffJob.DiffJob(item_name, item_exe, item_in, item_out)
                config_obj.diff_actions.append(diff_item)
            elif "Unit" == str(section_header[0]):
                item_exe = config[section]['exe']
                unit_item = UnitJob.UnitJob(item_name, item_exe)
                config_obj.unit_actions.append(unit_item)
            elif "Bash" == str(section_header[0]):
                item_command = config[section]['command']
                bash_item = BashJob.BashJob(item_name, item_command)
                config_obj.bash_actions.append(bash_item)
    return config_obj, os.getcwd()


def setup_config(args):
    pwd = os.getcwd()
    home_dir = os.path.expanduser('~')
    pwd = pwd.replace(home_dir, '~', 1)
    args.grade = str(args.grade).rstrip('\/')
    print("\nGRADING {}".format(args.grade))  # Print processing statement, to confirm selection
    print("Config file: {}/{}/config.ini".format(pwd, args.grade))  # Print config file which will be used
    try:
        os.chdir("./{}".format(args.grade))  # Move into the provided directory
        config_file = parse_config(args.rubric)
        os.chdir("../")
        # print(config_file) # Prints out processed config
        return config_file  # Load the config file
    except FileNotFoundError:
        print("Assignment not found, make sure the Grading folder is in this directory\n")
        import sys
        sys.exit()
