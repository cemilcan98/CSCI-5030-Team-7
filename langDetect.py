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
            flag = True
        else:
            flag = False

    return flag
