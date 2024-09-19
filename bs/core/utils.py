import re

def validate_email(email):
    regex = r'\S+@\S+'
    if re.match(regex, email):
        return True
    else:
        return False