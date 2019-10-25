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
    if "username" in session:
        return redirect(url_for("home"))
    if len(request.args) == 2:
        if "\'" in request.args["username"] or "\'" in request.args["password"]:
            flash("Username and password cannot have single quotes")
        else:
            response = db_manager.verify_login(request.args["username"], request.args["password"])
            if response == "":
                session["username"] = request.args["username"]
                #session["id"] = <get id from db>
                return redirect(url_for("home"))
            else:
                flash(response)
    return render_template("login/login.html")


@app.route("/create-account")
def create_account():
    if "username" in session:
        return redirect(url_for("home"))
    if len(request.args) == 3:
        if request.args["passwordNew"] != request.args["passwordRepeat"]:
            flash("Passwords don't match, try again")
        else:
            response = db_manager.add_login(request.args["username"], request.args["passwordNew"])
            if response == "":
                session["username"] = request.args["username"]
                return redirect(url_for("home"))
            else:
                flash(response)
    return render_template("login/create-account.html")


@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    blog_users = db_manager.get_usernames_with_blogs()
    usr = session["username"]
    if usr in blog_users:
        blog_users.remove(usr)
    return render_template("home.html", username=usr, usernames=blog_users)


@app.route("/blogs")
def blogs():
    if "username" not in session:
        return redirect(url_for("login"))
    usr = session["username"]
    if "myblogs" in request.args:
        return render_template("blogs.html", username=usr, name=usr)
    # get username from session and username of viewing blog from frontend
    # need: function from database to get all the blogs' title of the user (should be recent first, need list)
    #       function (createBlog) from database
    return render_template("")


@app.route("/blogs/entries")
def entries(blog_id):
    if "username" not in session:
        return redirect(url_for("login"))
    # get username from session and get blog_id from frontend
    # need: function from database to return list of all entries for the blog
    #       functions (addEntry, updateEntry, is_owner) from database
    #
    return ""


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))
    # pop session, redirect to /login


if __name__ == "__main__":
    app.debug = True
    app.run()
