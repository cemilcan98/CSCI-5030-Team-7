# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 16:41:14 2021

@author: omars
"""
import ast
import unicodedata
import math

class irishspell:

    def __init__(self):
        self.file1 = open("irish_frequency_new_1.txt", "r", encoding = "UTF-16")
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

        return 1 - d[lenstr1-1,lenstr2-1]/ lenstr1

    def spell(self, word):
        self.word = word.lower()
        self.word = unicodedata.normalize('NFC', self.word)
        self.special_characters = '''0123456789!@#$%^&*()\_+jkqvwxyz<>?|,:;[]{}*/.'''
        self.length = len(self.word)

        if self.length == 1:
            return True

        for character in self.word:
            if character in self.special_characters:
                return True

        self.probabilities = {}
        self.conditional = {}
        if self.length < 4:
            for word1 in self.frequency_dictionary:
                self.distance = self.damerau_levenshtein_distance(self.word, word1)
                if self.distance >= (1/self.length):
                    self.probabilities[word1] = math.pow(self.distance, self.probability) #P(given word | dictionary word)
                    self.conditional[word1] = self.probabilities[word1] * self.frequency_dictionary[word1]
        elif self.length < 12:
            for word1 in self.frequency_dictionary:
                self.distance = self.damerau_levenshtein_distance(self.word, word1)
                if self.distance >= (2/self.length):
                    self.probabilities[word1] = math.pow(self.distance, self.probability) #P(given word | dictionary word)
                    self.conditional[word1] = self.probabilities[word1] * self.frequency_dictionary[word1]
        else:
            for word1 in self.frequency_dictionary:
                self.distance = self.damerau_levenshtein_distance(self.word, word1)
                if self.distance >= (3/self.length):
                    self.probabilities[word1] = math.pow(self.distance, self.probability) #P(given word | dictionary word)
                    self.conditional[word1] = self.probabilities[word1] * self.frequency_dictionary[word1]

        if self.conditional == {}:
            return True

        self.conditional = {k: v for k, v in sorted(self.conditional.items(), reverse = True, key=lambda item: item[1])}
        self.suggestions[self.word] = self.conditional

        if list(self.conditional.keys())[0] == self.word:
            return True
        else:
            return False

    def gram(self, grams, word):
        self.exist = {}
        self.word = word.lower()
        self.word = unicodedata.normalize('NFC', self.word)
        for word1 in list(self.suggestions[self.word].keys())[:5]:
            sentence = list(grams)
            sentence[1] = word1
            sentence = tuple(sentence)
            if sentence in self.gram_irish_frequency_3:
                self.exist[word1] = self.gram_irish_frequency_3[sentence]
            else:
                self.exist[word1] = 0

        self.exist = {k: v for k, v in sorted(self.exist.items(), reverse = True, key=lambda item: item[1])}

        return list(self.exist.keys())

    def suggest(self,word,n):
        self.word = word.lower()
        self.word = unicodedata.normalize('NFC', self.word)
        return list(self.suggestions[self.word].keys())[:n]