# I think this function is not useful anymore.

# -*- coding: utf-8 -*-

import re

# check if word is in English or not using ascii and utf-8 code


def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

# check if text is in English


def detect(words):

    flag = False
    for i in words:
        if isEnglish(i):
            flag = True
        else:
            flag = False

    return flag
