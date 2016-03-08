__author__ = 'George Herde'

def yes_no_question(question_text, y_default = True):
    if y_default:
        user_input = input("{} (Y/n)".format(question_text)).strip().lower()
        if user_input in "" or user_input in "y":
            return True
        else:
            return False
    else:
        user_input = input("{} (y/N)".format(question_text)).strip().lower()
        if user_input in "" or user_input in "n":
            return False
        else:
            return True