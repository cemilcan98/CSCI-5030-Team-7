# -*- coding: utf-8 -*-

import re


def isEnglish(x):
    try:
        x.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def detect(words):

    print("in langdetect.py file: this is words: ")
    print(words)
    flag = False
    for i in words:
        if isEnglish(i):
            print("this is word: ", i, " and it is an alphabet")
            flag = True
        else:
            print("this is word: ", i, " and it is not an alphabet")
            flag = False

    print("flag is : ", flag)
    return flag
