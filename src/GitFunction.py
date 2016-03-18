import subprocess
import time
from GradeHelpUtil import yes_no_question
from Colorify import cyan, green, red, yellow, grey

__author__ = 'George Herde'


def log(config):
    git_commit_fields = ['id', 'author_name', 'date', 'message']
    git_log_format = ['%H', '%an', '%ad', '%s']
    git_log_format = '%x1f'.join(git_log_format) + '%x1e'

    p = subprocess.Popen('git log --format="%s" .' % git_log_format, shell=True, stdout=subprocess.PIPE)
    (git_log, _) = p.communicate()
    git_log = git_log.decode('ascii')
    git_log = git_log.strip('\n\x1e').split("\x1e")
    git_log = [row.strip().split("\x1f") for row in git_log]
    git_log = [dict(zip(git_commit_fields, row)) for row in git_log]

    # Currently there is an error that causes the system to close if the student
    # creates a directory that they then commit, but do not commit any files within it
    last_submit_time = time.strptime(git_log[0]['date'], "%a %b %d %H:%M:%S %Y %z")

    if config.due_date < last_submit_time:
        print_date = red(git_log[0]['date'])
        print_status = red("Late")
    else:
        print_date = green(git_log[0]['date'])
        print_status = green("On Time")
    print('Latest Change: {}'.format(print_date))
    print("Status: {}\n".format(print_status))

    if yes_no_question("View VCS Log?"):
        for event in git_log:
            log_string = ""
            log_string += yellow("Commit: {}\n".format(event['id']))
            log_string += cyan('Author: {}\n'.format(event['author_name']))
            log_string += 'Date: {}\n'.format(event['date'])
            log_string += '\tMessage: {}\n'.format(event['message'])
            print(log_string)
    print("-------------------------------------------------------------")


def reset():
    print("{}".format(grey("Resetting student repository")))
    subprocess.Popen('git reset .', shell=True, stdout=subprocess.PIPE).communicate()
    subprocess.Popen('git clean . -f', shell=True, stdout=subprocess.PIPE).communicate()
    print("{}".format(green("Reset complete\n")))


def pull():
    print("Pulling changes...")
    process = subprocess.Popen(["git", "pull"])
    process.communicate()


def checkout(bash):
    print("Checkout out to %s".format(bash))
    subprocess.Popen('git checkout %s'.format(bash), shell=True, stdout=subprocess.PIPE).communicate()
