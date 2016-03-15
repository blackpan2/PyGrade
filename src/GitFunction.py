import subprocess
import time
from GradeHelpUtil import yes_no_question
from Colorify import cyan, green, red, yellow, grey

__author__ = 'George Herde'


def pull():
    print("Pulling changes...")
    process = subprocess.Popen(["git", "pull"])
    output, error = process.communicate()
    if error is not None:
        pass
    if output is None:
        pass


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

    if len(git_log) is not 0:
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
    p = subprocess.Popen('git reset .', shell=True, stdout=subprocess.PIPE)
    p.communicate()
    p = subprocess.Popen('git clean . -f', shell=True, stdout=subprocess.PIPE)
    p.communicate()
    print("{}".format(green("Reset complete\n")))
