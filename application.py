from os import terminal_size
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from hunspell import Hunspell
import string
import sys
import langDetect
import random

app = Flask(__name__, template_folder="templates")

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

h = Hunspell()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["submit_button"] == "submit":
            # check if text is empty or not
            if not request.form.get("text"):
                error = "Please provide a text to check"
                return render_template("index.html", error=error)
            session['text'] = request.form.get("text")
            session['given_text'] = session['text']
            # checking punctuation marks
            punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
            for element in session['text']:
                if element in punc:
                    session['text'] = session['text'].replace(element, "")
            session['words'] = session['text'].split()
            session['misspelled'] = []

            # this function check if text in english or not using "detect" function in "langDetect"
            isEng = langDetect.detect(session['words'])
            session['notEng'] = ""
            if not(langDetect.detect(session['words'])):
                session['notEng'] = "The text is not in English."
            else:
                session['notEng'] = "The text is in English."
            # only if the word is in English, then we continue through this function to check spell
            if (isEng):
                for word in session['words']:
                    if h.spell(word) == True:
                        continue
                    session['misspelled'].append(word)
                # create suggestions from the dictionary
                session['suggestions'] = dict.fromkeys(session['misspelled'])
                for key in session['suggestions']:
                    session['suggestions'][key] = h.suggest(key)

            return render_template("/index.html", text=session['given_text'], misspelled=session['misspelled'], suggestions=session['suggestions'], notEng=session['notEng'])

        elif request.form["submit_button"] == "clear":
            return render_template("/index.html")
        # if user uses the correct button, this function first checks if text is empty or not,
        # and then spells it
        elif request.form["submit_button"] == "correct":
            if not request.form.get("text"):
                error = "Please provide a text to check"
                return render_template("index.html", error=error)
            session['new_text'] = session['given_text']
            for word in session['misspelled']:
                if request.form.get(word) != None:
                    session['new_text'] = session['new_text'].replace(
                        word, request.form.get(word))
                    print(session['new_text'])
                else:
                    error = "Please select a correction for all misspelled words"
                    return render_template("/index.html", error=error, text=session['given_text'], misspelled=session['misspelled'], suggestions=session['suggestions'], notEng=session['notEng'])
            return render_template("/index.html", text=session['given_text'], new_text=session['new_text'], misspelled=session['misspelled'], suggestions=session['suggestions'], notEng=session['notEng'])
        # if user uses the example button, this function creates some correct and wrong sentences
        elif request.form["submit_button"] == "example":

            example_dict = {
                1: 'What can I do with this?',
                2: "As you can easily notice the second block of text looks more realistic.",
                3: "Sam is looking for a job.",
                4: "I need to buy some things from IKEA.",
                5: "I hope to visit Peru again in the future.",
                6: "David came to dinnner with us.",
                7: "Would you lika to travl with me?",
                8: "I love learnning!",
            }
            # this random function make a random number every time so we can use it to have a new sentence
            # every time user uses the example button
            rand_num = random.randint(1, len(example_dict))
            example_text = example_dict[rand_num]
            return render_template("/index.html", text=example_text)

    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.run()
