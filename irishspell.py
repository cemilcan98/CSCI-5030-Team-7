# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 16:41:14 2021

@author: omars
"""
import math
import ast

class irishspell:

    def __init__(self):
        self.file1 = open("irish_frequency_filtered.txt", "r", encoding = "UTF-16")
        self.corpus1 = self.file1.read()
        self.frequency_dictionary = ast.literal_eval(self.corpus1)
        self.file1.close()
        self.file3 = open("gram_irish_frequency_filtered_3a.txt", "r", encoding = "UTF-16")
        self.corpus3 = self.file3.read()
        self.gram_irish_frequency_3 = ast.literal_eval(self.corpus3)
        self.file3.close()
        self.suggestions = {}

        self.probability = 25

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

        return 1 - d[lenstr1-1,lenstr2-1]/ max(lenstr1, lenstr2)

    def spell(self, word):
        word = word.lower()
        self.probabilities = {}
        self.conditional = {}
        for word1 in self.frequency_dictionary:
            self.probabilities[word1] = math.pow(self.damerau_levenshtein_distance(word, word1), self.probability) #P(given word | dictionary word)
            self.conditional[word1] = self.probabilities[word1] * self.frequency_dictionary[word1]

        self.conditional = {k: v for k, v in sorted(self.conditional.items(), reverse = True, key=lambda item: item[1])}
        self.suggestions[word] = (self.conditional)
        for key in self.conditional.keys():
            if list(self.conditional.keys())[0] == word:
                return True
            else:
                return False

    def gram(self, word):
        exist = []
        word = word.lower()
        for gram in self.gram_irish_frequency_3:
            if word in gram:
                exist.append(gram)
        return exist

    def suggest(self, word, n):
        word = word.lower()
        self.suggestion = []
        for key in self.suggestions[word].keys():
            self.suggestion.append(key)
        return self.suggestion[:n]