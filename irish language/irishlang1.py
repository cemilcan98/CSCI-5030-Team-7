# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:06:11 2021

@author: omars
"""
import ast

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


    def similar(self, word1, word2):
        word1 = word1 + ' ' * (len(word2) - len(word1))
        word2 = word2 + ' ' * (len(word1) - len(word2))
        return sum(1 if i == j else 0 for i, j in zip(word1, word2)) / float(len(word1))

    def spell(self, word):
        if word not in self.frequency_dictionary:
            return False
        else:
            return True

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
