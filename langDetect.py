# -*- coding: utf-8 -*-

import re


def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def detect(words):

    flag = False
    for i in words:
        if isEnglish(i):
            print("this is word: ", i, " and it is an alphabet")
            flag = True
        else:
            print("this is word: ", i, " and it is not an alphabet")
            flag = False

    return flag
