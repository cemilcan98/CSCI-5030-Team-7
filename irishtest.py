# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 13:43:02 2021

@author: omars
"""
from irishspell import irishspell

s = irishspell()
text = input("Please enter your text:")
suggestions = []
misspelled = []
parsed = text.split()
for word in parsed:
    if s.spell(word) == True:
        continue
    misspelled.append(word)
suggestions = dict.fromkeys(misspelled)
for key in suggestions:
    suggestions[key] = s.suggest(key)
print(suggestions)

'''
if __name__ == '__main__':
    s = irishspell()
    text = input("Please enter your text:")
    suggestions = []
    misspelled = []
    parsed = text.split()
    for word in parsed:
        if s.spell(word) == True:
            continue
        misspelled.append(word)
    suggestions = dict.fromkeys(misspelled)
    for key in suggestions:
        suggestions[key] = s.suggest(key)
    print(suggestions)
'''




#    word1 = list[0]
#    word2 = 'an'
#    print(word1)
#    print(word2)
#    similar(word1, word2)
#
#    text = "is é mo ainm amir akkad"

#
#    for misword in misspelled:
#        for word in frequency_dictionary:
#             = similar(misword, word)
#
#


#    word = "an"
#    print("Probablitiy of", word,"is", frequency_dictionary[word])
#

#

#
#    irish_dictionary['ainm']