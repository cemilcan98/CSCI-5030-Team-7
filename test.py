# from flask import Flask, flash, jsonify, redirect, render_template, request, session
# from flask_session import Session
# from hunspell import Hunspell

# # initializing string
# test_str = "You're a nice person."
 
# # printing original string
# print("The original string is : " + test_str)
 
# # initializing punctuations string
# punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
 
# # Removing punctuations in string
# # Using loop + punctuation string
# for ele in test_str:
#     if ele in punc:
#         test_str = test_str.replace(ele, "")
 
# # printing result
# print("The string after punctuation filter : " + test_str)

sentence = "helo, my name is omar."

punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
for element in sentence:
    if element in punc:
        sentence = sentence.replace(element, "")

print(sentence)