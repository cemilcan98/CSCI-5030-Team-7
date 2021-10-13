from os import terminal_size
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from hunspell import Hunspell
import string
import sys
import langDetect


app = Flask(__name__, template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

h = Hunspell()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["submit_button"] == "submit":
            if not request.form.get("text"):
                error = "Please provide a text to check"
                return render_template("index.html", error=error)
            session['text'] = request.form.get("text")
            punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
            for element in session['text']:
                if element in punc:
                    session['text'] = session['text'].replace(element, "")
            session['words'] = session['text'].split()
            session['misspelled'] = []
            # Amir
            # this function check if text in english or not
            isEng = langDetect.detect(session['words'])
            notEng = ""
            if not(langDetect.detect(session['words'])):
                notEng = "The text is not in English."
            else:
                notEng = "The text is in English."

            suggestions = ""
            # end Amir
            if (isEng):
                for word in session['words']:
                    if h.spell(word) == True:
                        continue
                    session['misspelled'].append(word)
                session['suggestions'] = dict.fromkeys(session['misspelled'])
                for key in session['suggestions']:
                    session['suggestions'][key] = h.suggest(key)

            return render_template("/index.html", text=session['text'], misspelled=session['misspelled'], suggestions=session['suggestions'], notEng=notEng)

        elif request.form["submit_button"] == "clear":
            return render_template("/index.html")

        elif request.form["submit_button"] == "correct":
            for word in session['misspelled']:
                session['text'] = session['text'].replace(
                    word, request.form.get(word))
            return render_template("/index.html", new_text=session['text'])

        elif request.form["submit_button"] == "example":

            example_dict = {
                1: 'What can I do with this?',
                2: "As you can easily notice the second block of text looks more realistic.",
                3: "Sam is looking for a job.",
                4: "I need to buy some things from IKEA.",
                5: "I hope to visit Peru again in the future."
            }

            #rand_num = random.randint(0, len(example_arr))
            example_text = example_dict[1]
            print(example_text)
            return render_template("/index.html", example_text=example_text)

    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.run()
