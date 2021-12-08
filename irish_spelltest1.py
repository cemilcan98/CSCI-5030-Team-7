# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 19:42:37 2021

@author: omars
"""
import ast
import unicodedata
import nltk
import math

class irishspell:

    def __init__(self):
        self.file1 = open("irish_frequency_new.txt", "r", encoding = "UTF-16")
        self.corpus1 = self.file1.read()
        self.frequency_dictionary = ast.literal_eval(self.corpus1)
        self.file1.close()
        self.file3 = open("gram_irish_frequency_3a.txt", "r", encoding = "UTF-16")
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
        self.irish_alphabet = '''abcdefghilmnoprstuáéíóú-'''
        self.special_characters = '''0123456789!@#$%^&*()\_+jkqvwxyz<>?|,:;[]{}*/.'''
        self.length = len(self.word)

        if self.length == 1:
            return True

        # if self.word[0] not in self.irish_alphabet:
        #         return True

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

        # for word1 in self.frequency_dictionary:
        #     self.probabilities[word1] = self.damerau_levenshtein_distance(self.word, word1)

        #     self.conditional[word1] = self.probabilities[word1]

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

'''
if __name__ == '__main__':
    s = irishspell()
    file = open('input.txt', 'r', encoding = "UTF-8")
    predictions = open('pval1.tsv', 'w', encoding = "UTF-8")
    count = 0
    for line in file:
        word = line.rstrip('\n')
        count += 1
        print(count)
        if s.spell(word) == True:
            predictions.write(word+"\t"+word+"\n")
        else:
            predictions.write(word+"\t"+s.suggest(word, 1)+"\n")
    file.close()
    predictions.close()
'''


if __name__ == '__main__':
    text = "Dia duite is anim dom Omar"
    text = text.lower()
    trigrams= nltk.ngrams(nltk.word_tokenize(text), 3)
    # text = "hóstáin Là bhi TV5MONDE"
    # text = "Rarh"
    s = irishspell()
    suggestions = {}
    misspelled = []
    grams = {}
    prob = {}

    for word in text.split():
        if s.spell(word) == True:
            continue
        misspelled.append(word)
    for gram in trigrams:
        for word in misspelled:
            suggestions[word] = s.suggest(word,5)
            if word == gram[1]:
                #grams[word] = gram
                prob[word] = s.gram(gram,word)
    for word in misspelled:
        if word not in prob.keys():
            prob[word] = suggestions[word]



'''
    with open('records.tsv', 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', newline='\n')
'''
# file = open("gram_irish_dictionary_3.txt", "r", encoding = "UTF-16")
# corpus1 = file.read()
# gram_irish_dictionary_3 = ast.literal_eval(corpus1)
# file.close()

# file = open("gram_irish_frequency_3.txt", "r", encoding = "UTF-16")
# corpus1 = file.read()
# gram_irish_frequency_3 = ast.literal_eval(corpus1)
# file.close()

# file = open("gram_irish_dictionary_1.txt", "r", encoding = "UTF-16")
# corpus1 = file.read()
# gram_irish_dictionary_4 = ast.literal_eval(corpus1)
# file.close()

# file = open("gram_irish_frequency_1.txt", "r", encoding = "UTF-16")
# corpus1 = file.read()
# gram_irish_frequency_4 = ast.literal_eval(corpus1)
# file.close()

# file = open("gram_irish_dictionary_3a.txt", "r", encoding = "UTF-16")
# corpus1 = file.read()
# gram_irish_dictionary_3 = ast.literal_eval(corpus1)
# file.close()

# file = open("gram_irish_frequency_3a.txt", "r", encoding = "UTF-16")
# corpus2 = file.read()
# gram_irish_frequency_3 = ast.literal_eval(corpus2)
# file.close()

# file = open("irish_dictionary.txt", "r", encoding = "UTF-16")
# corpus3 = file.read()
# irish_dictionary = ast.literal_eval(corpus3)
# file.close()

# file = open("irish_frequency.txt", "r", encoding = "UTF-16")
# corpus4 = file.read()
# frequency_dictionary = ast.literal_eval(corpus4)
# file.close()
