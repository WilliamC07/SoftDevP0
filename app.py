import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from data import db_manager, db_builder
# imported Flask, render_template, request, redirect, url_for, and session
app = Flask(__name__)
#create instance of class Flask
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/login")
def login():
    if len(request.args) == 2:
        response = db_manager.verifyLogin(request.args["username"], request.args["password"])
        if response == "":
            session["username"] = request.args["username"]
            #session["id"] = <get id from db>
            return redirect(url_for("home"))
        else:
            flash(response)
    return render_template("login/login.html")

@app.route("/create-account")
def create_account():
    if len(request.args) == 3:
        if request.args["passwordNew"] != request.args["passwordRepeat"]:
            flash("Passwords don't match, try again")
        else:
            response = db_manager.addLogin(request.args["username"], request.args["passwordNew"])
            if response == "":
                session["username"] = request.args["username"]
                #session["id"] = <get id from db>
                return redirect(url_for("home"))
            else:
                flash(response)
    return render_template("login/create-account.html")

@app.route("/home")
def home():
    # get username from session
    # need: function from database to get list of all users, beside the one logged in, with blogs
    return "welcome home - home.html to be added"

@app.route("/blogs")
def blogs():
    # get username/id from session and get user_id from frontend
    # need: function from database to get all the blogs of the user with given user_id
    #       function (createBlog) from database
    return ""

@app.route("/blogs/entries")
def entries():
    # get username/id from session and get blog_id from frontend
    # need: function from database to return list of all entries for the blog
    #       functions (addEntry, updateEntry, verifyBlogAuthor) from database
    #
    return ""

@app.route("/logout")
def logout():
    # pop session, redirect to /login
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()
