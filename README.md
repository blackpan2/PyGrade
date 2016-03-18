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
- Python version: 3
- Argument Parsing: argparse https://docs.python.org/3.4/library/argparse.html

## Plans made with Kocsen 3/4
### Action items:
- [x] receive config assignment directory
- [x] parse config file from directory
- [x] regex current directory to create a list ("student_repos") of student repositories
        - Identify student directory:
        - regex = "/\w{2}\w?\d{4}/"
- [x] `for "student" (directory name) in "student_repos": cd "student"/"submission_directory" (submission_directory is parsed from config)`
- [x] "submission_directory" not found present options for other directories
- [ ] create and set to 0 counter for grade totals (BONUS)
- [x] git pull
- [x] git log -> parse for the date (use to determine if late)
- [x] check for required files (print if present or not)
- [x] move support files
- [x] run build (which may not exist, in which case do nothing)
- [x] if diff: execute diff jobs
- [x] if unit tests: execute tests
- [x] if bash commands: executes commands
- [x] reset the students directory back to their information "git reset && git clean -f"



###config elements [`+` required, `-` optional]:
- (`+`) dir
- (`+`) required files
- (`-`) support files
- (`+`) due date
- (`-`) build (can be make)
- (`-`) diff exe
- (`-`) diff actions [ DiffJobs]
- (`-`) exe


