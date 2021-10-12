import re


def detect(word):
    word = "hello"
    reg = re.compile(r'[a-zA-Z]')

    if reg.match(word):
        print("It is an alphabet")
    else:
        print("It is not an alphabet")
