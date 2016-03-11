import configparser
import os
from Colorify import green

__author__ = 'George Herde'


class Rubric:
    def __init__(self, name, config_location):
        self.name = name
        self.config_location = config_location
        self.categories = []


def parse_rubric(assignment, config_location) -> Rubric:
    os.chdir("{}".format(config_location))
    print("Config has a rubric.\nLooking for rubric at: {}/rubric.ini".format(config_location))
    rubric_obj = Rubric(name=assignment, config_location=config_location)
    rubric = configparser.ConfigParser()
    rubric.read('rubric.ini')
    for section in rubric.sections():
        section_list = []
        for key in rubric[section]:
            key_tuple = (key, rubric[section][key])
            section_list.append(key_tuple)
        rubric_obj.categories = section_list
    os.chdir("../")


class Grade:
    def __init__(self, username, rubric):
        self.username = username
        self.total = 0
        self.rubric = rubric
        self.categories = []
        for cat in rubric.categories:
            for attribute in cat:
                self.categories.append((0,""))

    def add_grade(self, category_number):
        rubric = self.rubric
        current_category = self.categories[category_number]

