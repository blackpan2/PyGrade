# PyGrade

Automated grading workflow.  Written in python, without dependencies.
Author: George Herde
Contact: gh1823@rit.edu

## Introduction

This is a Python version of the Gradehelp tool reworked in order to make installation more straightforward as well as make it easier to iterate on, then the current version which is a Ruby Gem.

## Project Requirements

- Project should not require future users to install any additional resources
- Project needs to be able to build an assignment when provided with source and compile parameters, in the config file for that assignment.
- Project needs to run a program with an input file and then compare it to an expected output file
- Project will expect a config file for each assignment.  Configs will be stored in a project level folder named configs.

## Project Future Goals

- Project will automatically clean, removing the created files


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
- [ ] git log -> parse for the date (use to determine if late)
- [ ] check for required files (print if present or not)
- [ ] move support files
- [ ] run build (which may not exist, in which case do nothing)
- [ ] if diff: execute diff jobs
- [ ] if exe: execute exe
- [ ] reset the students directory back to their information "git reset && git clean -f"


argparse for parsing command line arguments

###config elements [`+` required, `-` optional]:
- (`+`) dir
- (`+`) required files
- (`-`) support files
- (`+`) due date
- (`-`) build (can be make)
- (`-`) diff exe
- (`-`) diff actions [ DiffJobs]
- (`-`) exe

