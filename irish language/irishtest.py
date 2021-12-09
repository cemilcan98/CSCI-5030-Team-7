# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 13:43:02 2021

@author: omars
"""
import ast
import math

class irishspell:

    def __init__(self):
        self.file = open("irish_dictionary.txt", "r", encoding = "UTF-16")
        self.corpus = self.file.read()
        self.irish_dictionary = ast.literal_eval(self.corpus)
        self.file.close()
        self.file1 = open("irish_frequency.txt", "r", encoding = "UTF-16")
        self.corpus1 = self.file1.read()
        self.frequency_dictionary = ast.literal_eval(self.corpus1)
        self.file1.close()

        self.probability = 0.03

    def similar(self, word1, word2):
        word1 = word1 + ' ' * (len(word2) - len(word1))
        word2 = word2 + ' ' * (len(word1) - len(word2))
        return sum(1 if i == j else 0 for i, j in zip(word1, word2)) / float(len(word1))

    def levenshtein(self, s1, s2):
        l1 = len(s1)
        l2 = len(s2)
        matrix = [list(range(l1 + 1))] * (l2 + 1)
        for zz in list(range(l2 + 1)):
          matrix[zz] = list(range(zz,zz + l1 + 1))
        for zz in list(range(0,l2)):
          for sz in list(range(0,l1)):
            if s1[sz] == s2[zz]:
              matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
            else:
              matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
        distance = float(matrix[l2][l1])
        result = distance/max(l1,l2)
        return result

    def damerau_levenshtein_distance(self, s1, s2):
        d = {}
        lenstr1 = len(s1)
        lenstr2 = len(s2)
        for i in range(-1,lenstr1+1):
            d[(i,-1)] = i+1
        for j in range(-1,lenstr2+1):
            d[(-1,j)] = j+1

        for i in range(lenstr1):
            for j in range(lenstr2):
                if s1[i] == s2[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i,j)] = min(
                               d[(i-1,j)] + 1, # deletion
                               d[(i,j-1)] + 1, # insertion
                               d[(i-1,j-1)] + cost, # substitution
                              )
                if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                    d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

        return d[lenstr1-1,lenstr2-1]/ max(lenstr1, lenstr2)

    def damerau_levenshtein_distance_improved(self, a, b):
        # "Infinity" -- greater than maximum possible edit distance
        # Used to prevent transpositions for first characters
        INF = len(a) + len(b)

        # Matrix: (M + 2) x (N + 2)
        matrix  = [[INF for n in range(len(b) + 2)]]
        matrix += [[INF] + range(len(b) + 1)]
        matrix += [[INF, m] + [0] * len(b) for m in range(1, len(a) + 1)]

        # Holds last row each element was encountered: DA in the Wikipedia pseudocode
        last_row = {}

        # Fill in costs
        for row in range(1, len(a) + 1):
            # Current character in a
            ch_a = a[row-1]

            # Column of last match on this row: DB in pseudocode
            last_match_col = 0

            for col in range(1, len(b) + 1):
                # Current character in b
                ch_b = b[col-1]

                # Last row with matching character
                last_matching_row = last_row.get(ch_b, 0)

                # Cost of substitution
                cost = 0 if ch_a == ch_b else 1

                # Compute substring distance
                matrix[row+1][col+1] = min(
                    matrix[row][col] + cost, # Substitution
                    matrix[row+1][col] + 1,  # Addition
                    matrix[row][col+1] + 1,  # Deletion

                    # Transposition
                    # Start by reverting to cost before transposition
                    matrix[last_matching_row][last_match_col]
                        # Cost of letters between transposed letters
                        # 1 addition + 1 deletion = 1 substitution
                        + max((row - last_matching_row - 1),
                              (col - last_match_col - 1))
                        # Cost of the transposition itself
                        + 1)

                # If there was a match, update last_match_col
                if cost == 0:
                    last_match_col = col

            # Update last row for current character
            last_row[ch_a] = row

        # Return last element
        return matrix[-1][-1]

    def spell(self, word):
        self.probabilities = {}
        self.conditional = {}
        for word1 in self.frequency_dictionary:
            self.probabilities[word1] = math.pow(self.probability, self.levenshtein(word, word1)) #P(given word | dictionary word)
            self.conditional[word1] = self.probabilities[word1] * self.frequency_dictionary[word1]

        self.probabilities = {k: v for k, v in sorted(self.probabilities.items(), reverse = True, key=lambda item: item[1])}
        self.conditional = {k: v for k, v in sorted(self.conditional.items(), reverse = True, key=lambda item: item[1])}
        return self.probabilities, self.conditional


    def suggest(self, word):
        self.probabilities = {}
        self.suggestions = []

        for word1 in self.frequency_dictionary:
            self.probabilities[word1] = self.similar(word, word1)
        self.probabilities = {k: v for k, v in sorted(self.probabilities.items(), reverse = True, key=lambda item: item[1])}
        keys = self.probabilities.keys()
        for key in keys:
            self.suggestions.append(key)
        return self.suggestions[:10]

if __name__ == '__main__':
    text = "is é mo ainm amir akkad cemil can"
    s = irishspell()
    suggestions = []
    misspelled = []
    probabilities = {}
    conditional = {}
    parsed = text.split()
    for word in parsed:
        probabilities[word], conditional[word]  = s.spell(word)
    #misspelled.append(word)
    #suggestions = dict.fromkeys(misspelled)
    #for key in suggestions:
    #    suggestions[key] = s.suggest(key)
    #print(suggestions)

file = open("irish_dictionary.txt", "r", encoding = "UTF-16")
corpus = file.read()
irish_dictionary = ast.literal_eval(corpus)
file.close()

file = open("irish_frequency.txt", "r", encoding = "UTF-16")
corpus = file.read()
frequency_dictionary = ast.literal_eval(corpus)
file.close()

'''
from irishlang1 import irishspell
text = "is é mo ainm amir akkad cemil can"
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
'''