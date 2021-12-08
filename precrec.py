# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 09:27:39 2021

@author: omars
"""
labels = []
file = open("corrections500.tsv", encoding = "UTF-8")
for line in file:
    line = line.strip('\n')
    word = line.split('\t')
    if word[0] == word[1]:
        labels.append(0)
    else:
        labels.append(1)
file.close()

# textfile = open("correctionslabels.txt", "w")
# for element in labels:
#     textfile.write(element + '\n')
# textfile.close()



labels1 = []
file1 = open("pval12.tsv", encoding = "UTF-8")
for line1 in file1:
    line1 = line1.strip('\n')
    word1 = line1.split('\t')
    if word1[0] == word1[1]:
        labels1.append(0)
    else:
        labels1.append(1)
file1.close()

# textfile1 = open("predictionslabels.txt", "w")
# for element1 in labels1:
#     textfile1.write(element1 + '\n')
# textfile1.close()

labels_less = labels[:1000]
labels_less1 = labels1[:1000]

from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
cm = confusion_matrix(labels_less, labels_less1)
recall = recall_score(labels_less, labels_less1)
precision = precision_score(labels_less, labels_less1)
f1 = f1_score(labels_less, labels_less1)