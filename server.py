"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

# why use parentheses up top and not down here? ASK**
from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def show_register_form():
	"""Shows registration form for new users."""

	return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def processes_new_user():
	"""Checks to see if a user with that email address exists. 
	If not, creates new user in database."""

	# gets data from form
	user_email = request.form.get("email")
	password = request.form.get("password")
	age = request.form.get("age")
	zipcode = request.form.get("zipcode")

	# query the db for user email
	check_email = User.query.filter(User.email==user_email)
	check_email = check_email.first()
	# check_email = True when there's a record. 

	if not check_email:
		new_user = User(email=user_email, password=password,
						age=int(age), zipcode=zipcode)
		db.session.add(new_user)
		db.session.commit()

	return redirect("/")

@app.route("/login", methods=["GET"])
def show_login_form():
	"""Shows login form for new users."""

	return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def logs_in_user():
	"""Checks for email and password in database, then logs in if they match."""

	# gets email and password from form
	email = request.form.get("email")
	password = request.form.get("password")

	# query db for user email
	check_email = User.query.filter(User.email==email) # REMINDER TO CHECK YOUR VARIABLES
	check_email = check_email.first()

	# check if email is in db
	if check_email:
		check_email_and_pw = User.query.filter(User.email==email, User.password==password)
		check_email_and_pw = check_email_and_pw.first()

		if check_email_and_pw:
			print("if statement true")
			session["current_user"] = email
			print("USER IS LOGGED IN!")
			flash("Logged in as %s" % email)
			return redirect("/")






	return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
