import subprocess

__author__ = 'George Herde'

def pull():

    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]

def reset():
    pass

def log():
    pass
