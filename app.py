import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
# imported Flask, render_template, request, redirect, url_for, and session
app = Flask(__name__)
#create instance of class Flask
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    if len(request.args) == 2:
        if verifyLogin(request.args["username"], request.args["password"]):
            session["username"] = request.args["username"]
            #session["id"] = <get id from db>
        else:
            flash("some message")
    return render_template("login/login.html")

@app.route("/home")
def home():
    return ""



if __name__ == "__main__":
    app.debug = True
    app.run()
