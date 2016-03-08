import subprocess
import time
from GradeHelpUtil import yes_no_question
from Colorify import green, red

__author__ = 'George Herde'


def pull():
    print("Pulling changes...")
    process = subprocess.Popen(["git", "pull"])
    output, error = process.communicate()
    if error is not None:
        pass
    if output is None:
        pass


def reset():
    pass


def log(config):
    GIT_COMMIT_FIELDS = ['id', 'author_name', 'date', 'message']
    GIT_LOG_FORMAT = ['%H', '%an', '%ad', '%s']
    GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'

    p = subprocess.Popen('git log --format="%s"' % GIT_LOG_FORMAT, shell=True, stdout=subprocess.PIPE)
    (git_log, _) = p.communicate()
    git_log = git_log.decode('ascii')
    git_log = git_log.strip('\n\x1e').split("\x1e")
    git_log = [row.strip().split("\x1f") for row in git_log]
    git_log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in git_log]

    last_submit_time = time.strptime(git_log[0]['date'], "%a %b %d %H:%M:%S %Y %z")

    if config.due_date > last_submit_time:
        print_date = red(git_log[0]['date'])
        print_status = red("Late")
    else:
        print_date = green(git_log[0]['date'])
        print_status = green("On Time")
    print('Latest Change: {}'.format(print_date))
    print("Status: {}".format(print_status))

    if yes_no_question("View VCS Log?"):
        log_string=""

        print(git_log)
    else:
        pass