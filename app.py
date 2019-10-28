import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
# import flask functions
from data import db_manager, db_builder
# import database functions
app = Flask(__name__)
app.secret_key = os.urandom(32)
# set up sessions with random secret key

@app.route("/")
def root():
    if "username" in session:
    #if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    return redirect(url_for("login"))
    # else, redirect to login page


@app.route("/login")
def login():
    if "username" in session:
    # if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    if len(request.args) == 2:
    # if users clicked the log in button,
        if request.args["username"] == "" or request.args["password"] == "":
        # if either username or password is blank
            flash("Please do not leave any fields blank")
            # flash error
        else:
            response = db_manager.verify_login(request.args["username"],
                                               request.args["password"])
            # verify entered username and password with database
            if response == "":
            # if username and password combo is in database
                session["username"] = request.args["username"]
                # add username to session (log user in)
                return redirect(url_for("home"))
                # redirect to homepage
            else:
            # else is username/password is incorrect
                flash(response)
                # flash error
    return render_template("login/login.html")
    # render login template


@app.route("/create-account")
def create_account():
    if "username" in session:
    # if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    if len(request.args) == 3:
    # if users clicked the submit button on create account page
        if request.args["username"] == "" or request.args["passwordNew"] == "" or request.args["passwordRepeat"] == "":
        # if any one of the three fields are blank,
            flash("Please do not leave any fields blank")
            # flash an error
        else:
            if request.args["passwordNew"] != request.args["passwordRepeat"]:
            # if the two passwords do not match,
                flash("Passwords don't match, try again")
                # flash an error
            else:
            # else if the passwords match
                response = db_manager.add_login(request.args["username"],
                                                request.args["passwordNew"])
                # check with database to see if the username is valid/unique
                if response == "":
                # if username is valid,
                    session["username"] = request.args["username"]
                    # add username to session (log user in)
                    return redirect(url_for("home"))
                    # redirect to homepage
                else:
                # else if the username is already taken
                    flash(response)
                    # flash error
    return render_template("login/create-account.html")
    # render create-account.html template


@app.route("/home")
def home():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    if "user" in request.args:
    # if user clicked on a button to view other users' blogs
        return redirect(url_for("blogs", user=request.args["user"]))
        # redirect logged in user to blogs page with the username they clicked on as a GET request
    blog_users = db_manager.get_usernames_with_blogs()
    # get the list of usernames with blogs from database
    user = session["username"]
    # user is set to the username of person logged in
    if user in blog_users:
    # if the user logged in has blogs
        blog_users.remove(user)
        # remove their username from the list of usernames
    return render_template("home.html", username=user, usernames=blog_users)
    # render home.html template with the username and list of other users with blogs


@app.route("/blogs", methods=['GET'])
def blogs():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    user = session["username"]
    # user is set to username of logged in user
    blog_owner = user
    # blog_owner is set to user by default
    if "user" in request.args:
    # if user is not blog_owner
        blog_owner = request.args["user"][:len(request.args["user"]) - 8]
        #set blog_owner to the username of the actual owner of the blog
    if "blog_creation" in request.args:
    # if the blog_owner clicked on create blog button,
        title = request.args["blog_name"]
        # set title to the blog title that user entered
        if title == "":
            flash("Please do not have an empty blog title")
        else:
            response = db_manager.create_blog_for_username(user, title)
            # verify blog title with database
            if response == "":
            # if blog title is unique
                return redirect(url_for("entries",
                                        blog_id=db_manager.get_blog_id_from_title(
                                            user, title),
                                        blog_name=title))
                # redirect to the entries page of the new blog with
                # the blog title and blog id as GET requests
            flash(response)
            # else flash error if blog with the same title already exists
    return render_template("blogs.html", username=user,
                           name=("Your" if blog_owner == user else blog_owner),
                           isOwner=(blog_owner == user),
                           blogs=db_manager.get_blogs_for_username(blog_owner))
    # render blogs.html template with the username of user logged in,
    # the blog owner, whether the user logged in is the owner, and
    # the list of blogs owned by logged in user


@app.route("/blogs/entries", methods=['GET'])
def entries():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    blog_title = request.args["blog_name"]
    # set blog_title to blog name acquired from GET request
    user = session["username"]
    # set user to username of person logged in
    blog_owner = user
    # blog_owner is set to user by default
    if "user" in request.args and request.args["user"] != "Your":
        blog_owner = request.args["user"]
    if "blog_id" in request.args:
    # if blog_id is in GET request (which happens when blog is just created),
        blog_id = request.args["blog_id"]
        # set blog_id to that GET request
    else:
    # else if blog_id is not in GET request
        blog_id = db_manager.get_blog_id_from_title(blog_owner, blog_title)
        # get blog_id from database based on the username and blog_title
        # if user is not the owner of the blog, None is returned
    if len(request.args) == 4:
    # if the length of GET requests is 4, meaning user is updating, deleting,
    # or creating entries,
        entry_title = request.args["entry_title"]
        entry_content = request.args["entry_content"]
        # set entry_title and entry_content based on the GET requests
    if "update" in request.args:
    # if user is updating an entry
        db_manager.remove_entry(db_manager.get_entry_id(entry_title, blog_id))
        # tell database to remove the entry
        db_manager.add_entry(entry_title,
                             entry_content,
                             blog_id)
        # create a new entry in database with the same blog_id and entry_title,
        # but with the updated content
    if "delete" in request.args:
    # if user is deleting an entry
        db_manager.remove_entry(db_manager.get_entry_id(entry_title, blog_id))
        # tell database to remove the entry after getting its entry_id given
        # entry_title and blog_id
    if "create" in request.args:
    # if user is creating entry
        if entry_title == "":
        # if entry_title is blank,
            flash("Please do not have a blank entry title")
            # flash an error
        else:
            response = db_manager.add_entry(entry_title,
                                            entry_content,
                                            blog_id)
            # tell database to add entry given the entry_title, entry_content,
            # and blog_id
            if response != "":
            # if entry was not added successfully (because of duplicate title),
                flash(response)
                # flash an error
    return render_template("entries.html", blog_name=blog_title,
                           entries=db_manager.get_entries_for_blog(blog_id),
                           isOwner=db_manager.is_owner(
                               user, blog_id))
    # render entries.html template given blog_name, list of entries, and isOwner


@app.route("/logout")
def logout():
    if "username" in session:
    # if user is logged in
        session.pop("username")
        # pop "username" from session (logging the user out)
    return redirect(url_for("login"))
    # redirect user back to login page


if __name__ == "__main__":
    app.debug = True
    app.run()
