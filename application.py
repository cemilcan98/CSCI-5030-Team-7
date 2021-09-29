from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from hunspell import Hunspell
import string

app = Flask(__name__, template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True

h = Hunspell()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("text"):
            error = "Please provide a text to check"
            return render_template("index.html", error=error)
        text = request.form.get("text")
        clear_text = text.translate(str.maketrans('', '', string.punctuation))
        words = clear_text.split()
        suggestions = []
        misspelled = []
        for word in words:
            if h.spell(word) == True:
                continue
            suggest = h.suggest(word)
            misspelled.append(word)
            suggestions.append(suggest)
        return render_template("/index.html", text=text, misspelled=misspelled, suggestions=suggestions)
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.run()
