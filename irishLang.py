import nltk
import re
import unicodedata
import pickle

with open("bible.txt", newline = '\n', encoding= "UTF-8") as bible:
    bible1 = bible.read()
bible.close()
with open("blogs.txt", newline = '\n', encoding= "UTF-8") as blogs:
    blogs1 = blogs.read()
blogs.close()
with open("legal.txt", newline = '\n', encoding= "UTF-8") as legal:
    legal1 = legal.read()
legal.close()
with open("news.txt", newline = '\n', encoding= "UTF-8") as news:
    news1 = news.read()
news.close()
with open("tweets.txt", newline = '\n', encoding= "UTF-8") as tweets:
    tweets1 = tweets.read()
tweets.close()
with open("wiki.txt", newline = '\n', encoding= "UTF-8") as wiki:
    wiki1 = wiki.read()
wiki.close()

#bible_test = 45*nltk.sent_tokenize(bible1)
#bible_test1 = nltk.sent_tokenize(bible1)
#for i in range(len(bible_test)):
#    bible_test [i] = re.sub(r'\W',' ',bible_test [i])
#    bible_test [i] = re.sub(r'\s+',' ',bible_test [i])
#    bible_test [i] = unicodedata.normalize('NFC', bible_test [i])
#    bible_test [i] = bible_test [i].lower()
#
#bible_test_dict = {}
#for sentence in bible_test:
#    tokens = nltk.word_tokenize(sentence)
#    for token in tokens:
#        irish_vowels = ["A","E","I","O","U","\u00C1","\u00C9","\u00CD","\u00D3","\u00DA",
#                    "a","e","i","o","u","á","é","í","ó","ú"]
#        if len(token) != 1:
#            if (token[0] == 'n' or token[0] == 't') and token[1] in irish_vowels and  len(token) != 2:
#                token = token[0] + '-' + token[1:]
#        if token not in bible_test_dict.keys():
#            bible_test_dict[token] = 1
#        else:
#            bible_test_dict[token] += 1

corpus = 45*nltk.sent_tokenize(bible1) + 3*nltk.sent_tokenize(blogs1) + 30*nltk.sent_tokenize(legal1) + 5*nltk.sent_tokenize(news1) + 2*nltk.sent_tokenize(tweets1) + 15*nltk.sent_tokenize(wiki1)
for i in range(len(corpus)):
    corpus [i] = re.sub(r'\W',' ',corpus [i])
    corpus [i] = re.sub(r'\s+',' ',corpus [i])
    corpus [i] = unicodedata.normalize('NFC', corpus [i])
    corpus [i] = corpus [i].lower()

irish_dict = {}
for sentence in corpus:
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        irish_vowels = ["A","E","I","O","U","\u00C1","\u00C9","\u00CD","\u00D3","\u00DA",
                    "a","e","i","o","u","á","é","í","ó","ú"]
        if len(token) != 1:
            if (token[0] == 'n' or token[0] == 't') and token[1] in irish_vowels and  len(token) != 2:
                token = token[0] + '-' + token[1:]
        if token not in irish_dict.keys():
            irish_dict[token] = 1
        else:
            irish_dict[token] += 1

for key in irish_dict.copy():
    if irish_dict[key] < 45:
        irish_dict.pop(key)

numbers = '''0123456789_'''
for key in irish_dict.copy():
    for element in key:
       if element in numbers:
           irish_dict.pop(key)
           break

irish_dict = {k: v for k, v in sorted(irish_dict.items(), reverse = True, key=lambda item: item[1])}

total = 0
for key in irish_dict:
    total += irish_dict[key]

frequency_dict = {}
for key in irish_dict:
    frequency_dict[key] = irish_dict[key]/total


file = open("irish_dictionary.txt", "w", encoding = "UTF-16")
file.write("%s\n" % (irish_dict))
file.close()

file = open("irish_frequency.txt", "w", encoding = "UTF-16")
file.write("%s\n" % (frequency_dict))
file.close()

import ast
file = open("irish_dictionary.txt", "r", encoding = "UTF-16")
corpus1 = file.read()
irish_dictionary = ast.literal_eval(corpus)
file.close()

file = open("irish_frequency.txt", "r", encoding = "UTF-16")
corpus1 = file.read()
frequency_dictionary = ast.literal_eval(corpus)
file.close()

file = open("irish_dictionary_old.txt", "r", encoding = "UTF-16")
corpus1 = file.read()
irish_dictionary_old = ast.literal_eval(corpus)
file.close()

file = open("irish_frequency_old.txt", "r", encoding = "UTF-16")
corpus1 = file.read()
frequency_dictionary_old = ast.literal_eval(corpus)
file.close()

from nltk import ngrams

n = 3
grams_irish_dict_3 = {}
for sentence in corpus:
    grams= ngrams(nltk.word_tokenize(sentence), n)
    for gram in grams:
        if gram not in grams_irish_dict_3.keys():
            grams_irish_dict_3[gram] = 1
        else:
            grams_irish_dict_3[gram] += 1

grams_irish_dict_3 = {k: v for k, v in sorted(grams_irish_dict_3.items(), reverse = True, key=lambda item: item[1])}

for key in grams_irish_dict_3.copy():
    if grams_irish_dict_3[key] < 15:
        grams_irish_dict_3.pop(key)

total = 0
for key in grams_irish_dict_3:
    total += grams_irish_dict_3[key]

gram_frequency_dict_3 = {}
for key in grams_irish_dict_3:
    gram_frequency_dict_3[key] = grams_irish_dict_3[key]/total

file = open("gram_irish_frequency_3a.txt", "w", encoding = "UTF-16")
file.write("%s\n" % (gram_frequency_dict_3))
file.close()

import ast
file = open("gram_irish_dictionary.txt", "r", encoding = "UTF-16")
corpus1 = file.read()
gram_irish_dictionary = ast.literal_eval(corpus1)
file.close()


import ast
file1 = open("irish_dictionary.txt", "r", encoding = "UTF-16")
corpus1 = file1.read()
irish_dictionary = ast.literal_eval(corpus1)
file1.close()

irish_alphabet = '''abcdefghilmnoprstuáéíóú-'''
for key in irish_dictionary.copy():
    for element in key:
       if element not in irish_alphabet:
           irish_dictionary.pop(key)
           break

file2 = open("irish_dictionary_filtered.txt", "w", encoding = "UTF-16")
file2.write("%s\n" % (irish_dictionary))
file2.close()

file3 = open("gram_irish_dictionary_3a.txt", "r", encoding = "UTF-16")
corpus2 = file3.read()
gram_irish_dictionary_3a = ast.literal_eval(corpus2)
file3.close()

irish_alphabet = '''abcdefghilmnoprstuáéíóú-'''
for key in gram_irish_dictionary_3a.copy():
    break_flag = False
    for element in key:
        if break_flag:
            break
        for letter in element:
            if letter not in irish_alphabet:
                gram_irish_dictionary_3a.pop(key)
                break_flag = True
                break

file4 = open("gram_irish_dictionary_3a_filtered.txt", "w", encoding = "UTF-16")
file4.write("%s\n" % (gram_irish_dictionary_3a))
file4.close()

total = 0
for key in gram_irish_dictionary_3a:
    total += gram_irish_dictionary_3a[key]

gram_frequency_dict_3a = {}
for key in gram_irish_dictionary_3a:
    gram_frequency_dict_3a[key] = gram_irish_dictionary_3a[key]/total

file5 = open("gram_irish_frequency_filtered_3a.txt", "w", encoding = "UTF-16")
file5.write("%s\n" % (gram_frequency_dict_3a))
file5.close()


file6 = open("irish_dictionary_filtered.txt", "r", encoding = "UTF-16")
corpus3 = file6.read()
irish_dictionary1 = ast.literal_eval(corpus3)
file6.close()

total = 0
for key in irish_dictionary1:
    total += irish_dictionary1[key]

frequency_dict = {}
for key in irish_dictionary1:
    frequency_dict[key] = irish_dictionary1[key]/total

file7 = open("irish_frequency_filtered.txt", "w", encoding = "UTF-16")
file7.write("%s\n" % (frequency_dict))
file7.close()


