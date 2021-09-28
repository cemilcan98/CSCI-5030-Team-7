from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__, template_folder="templates")

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("text"):
            error = "Please provide a text to check"
            return render_template("index.html", text=error)

        text = request.form.get("text")
        return render_template("/index.html", text=text)

    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.run()
