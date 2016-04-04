# PyGrade
Automated grading workflow.  Written in python, without dependencies.<br />
Author: George Herde<br />
Contact: gh1823@rit.edu<br />

## Introduction
This is a Python version of the Gradehelp tool reworked in order to make installation more straightforward 
as well as make it easier to iterate on, then the current version which is a Ruby Gem.

## Project Requirements
- Project should not require future users to install any additional resources
- Project needs to be able to build an assignment when provided with source and compile parameters, in the config file for that assignment.
- Project needs to run a program with an input file and then compare it to an expected output file
- Project needs to run a program for unit tests
- Project needs to support additional bash commands at the end of a testing set
- Project will expect a config file for each assignment.  Configs will be stored in a project level folder named configs.
- Project will automatically clean upon entering and leaving student repository

## Project Details
- Python version: 3 (Written on 3.4, will work with all python 3 versions)
- Argument Parsing: [argparse] (https://docs.python.org/3.4/library/argparse.html)
- Version Control System: [git] (https://git-scm.com/)
- Configuration File parsing: [configparser](https://docs.python.org/3.4/library/configparser.html)
- OS Commands: [os](https://docs.python.org/3.4/library/os.html)

## Installation:
1. Copy the files from the source folder to your target machine.
2. Make "gradehelp.py" executable
  * chmod +x gradehelp.py
3. PyGrade is now installed.
4. For ease of access setup an alias in your bashrc file to the target location:
  * alias gradehelp="python3 %PATH%/GradeHelp.py"
  * %PATH% from ~ to GradeHelp.py

## Running:
To grade an assignment: gradehelp -g [assignment name]
- [assignment name] is the folder containing the files to be used for grading (minimum is a config.ini file)
To grade an assignment starting at a certain student: gradehelp -g [assignment name] -s [student username]

## Commands:
usage: GradeHelp.py [-h] [-g GRADE] [-s STUDENT] [-p] [--reset]<br />

optional arguments:<br />
  -h, --help            show this help message and exit <br />
  -g GRADE, --grade GRADE
                        assignment folder (containing config) to be graded<br />
  -s STUDENT, --student STUDENT
                        provide a student's username to start at their folder<br />
  -p, --pull            update all of the student repositories<br />
  --reset               reset all student repositories to their last commit<br />
