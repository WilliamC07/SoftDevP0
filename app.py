import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from data import db_manager, db_builder
app = Flask(__name__)
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
        if ("\'" in request.args["username"] or
            "\'" in request.args["password"]):
            flash("Username and password cannot have single quotes")
        else:
            response = db_manager.verify_login(request.args["username"],
                                               request.args["password"])
            if response == "":
                session["username"] = request.args["username"]
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
            response = db_manager.add_login(request.args["username"],
                                            request.args["passwordNew"])
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
    if "user" in request.args:
        return redirect(url_for("blogs", user=request.args["user"]))
    blog_users = db_manager.get_usernames_with_blogs()
    usr = session["username"]
    if usr in blog_users:
        blog_users.remove(usr)
    return render_template("home.html", username=usr, usernames=blog_users)


@app.route("/blogs", methods=['GET'])
def blogs():
    if "username" not in session:
        return redirect(url_for("login"))
    usr = session["username"]
    user = usr
    if "user" in request.args:
        user = request.args["user"]
    if "blog_creation" in request.args:
        title = request.args["blog_name"]
        response = db_manager.create_blog_for_username(usr, title)
        if response == "":
            return redirect(url_for("entries",
                                    blog_id=db_manager.get_blog_id_from_title(
                                        usr, title),
                                    blog_title=title))
        flash(response)
    return render_template("blogs.html", username=usr,
                           name=user, isOwner=True,
                           blogs=db_manager.get_blogs_for_username(user))


@app.route("/blogs/entries", methods=['GET'])
def entries():
    if "username" not in session:
        return redirect(url_for("login"))
    if "blog_title" in request.args:
        blog_title = request.args["blog_title"]
    else:
        blog_title = request.args["blog_name"]
    if "blog_id" in request.args:
        blog_id = request.args["blog_id"]
    else:
        if "user" in request.args:
            user = request.args["user"]
        else:
            user = session["username"]
        blog_id = db_manager.get_blog_id_from_title(user, blog_title)
    if "update" in request.args:
        db_manager.remove_entry(blog_id)
        db_manager.add_entry(session["username"],
                             request.args["entry_title"],
                             request.args["entry_content"])
    if "delete" in request.args:
        db_manager.remove_entry(blog_id)
    if "create" in request.args:
        db_manager.add_entry(session["username"],
                             request.args["entry_title"],
                             request.args["entry_content"])
    return render_template("entries.html", blog_name=blog_title,
                           entries=db_manager.get_entries_for_blog(blog_id),
                           isOwner=db_manager.is_owner(
                               session["username"], blog_id))


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.debug = True
    app.run()
