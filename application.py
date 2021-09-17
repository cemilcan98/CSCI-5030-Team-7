from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__, template_folder="templates")

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    
        return render_template("/index.html")


if __name__ == "__main__":
    app.run()