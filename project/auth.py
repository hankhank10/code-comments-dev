from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from project import mailman

import arrow

from flask_login import login_user, logout_user
import secrets

from .models import User, Snapshot


auth = Blueprint('auth_blueprint', __name__)


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def username_available(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return False
    else:
        return True


@auth.get('/api/username_available')
def api_username_available():
    username = request.args.get('username')
    if not username:
        return jsonify(
            status = "error",
            error = "No username passed"
        )

    return jsonify(
        status = "success",
        username = username,
        available = username_available(username)
    )


@auth.get('/register')
def register_link():
    return redirect('/#modal-register')


@auth.post('/register')
def register():
    email = request.form['signup_email']
    username = request.form['signup_username']
    password = request.form['signup_password1']

    if not username_available(username):
        flash("This username is already registered.", "danger")
        return redirect(redirect_url())

    user = User.query.filter_by(username=username).first()

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        username=username,
        password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash("Account created. Please login. 🍻", "success")
    return redirect(redirect_url())


@auth.post('/login')
def login():
    username = request.form['login_username']
    password = request.form['login_password']

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Typo. Check and try again 🤦', 'danger')
        return redirect(redirect_url())

    login_user(user, remember=True)
    flash('Login successful 👋', 'success')

    # if the above check passes, then we know the user has the right credentials
    return redirect(redirect_url())


@auth.get('/logout')
def logout():
    logout_user()
    flash('All good things come to an end. Come back soon 😿', 'success')
    return redirect(redirect_url())


@auth.get('/profile')
@login_required
def profile():

    user_snapshots = Snapshot.query.filter_by(owner_id = current_user.id).all()

    return render_template('profile.html',
                           snapshot=None,
                           gist=None,
                           user_snapshots = user_snapshots)


@auth.post('/profile/change_email')
@login_required
def change_email():

    current_user.email = request.form['email']
    db.session.commit()

    flash ("Email changed 💌", "success")
    return redirect(redirect_url())


@auth.post('/profile/change_password')
@login_required
def change_password():

    current_password = request.form['current_password']
    new_password = request.form['new_password_1']
    new_password2 = request.form['new_password_2']

    if new_password != new_password2:
        flash('New passwords do not match 👎', 'danger')
        return redirect(redirect_url())

    if not check_password_hash(current_user.password, current_password):
        flash('Your original password is incorrect 🤦', 'danger')
        return redirect(redirect_url())

    current_user.password = generate_password_hash(new_password, method='sha256')

    db.session.commit()

    flash ("Updated that for you 👍", "success")
    return redirect(redirect_url())


@auth.route('/profile/reset-password', methods=['POST'])
def reset_password():
    email_address = request.form['reset_email']

    print (email)
    users = User.query.filter_by(email = email_address).all()

    for user in users:

        password_reset_key = secrets.token_hex(20)
        user.password_reset_key = password_reset_key
        user.password_reset_expiry = arrow.utcnow().shift(hours=1).datetime
        db.session.commit()

        messages = [
            'Well hello there 👋',
            'You recently requested a password reset from <a href="https://codecomments.dev">CodeComments.dev</a> for the username ' + user.username +'.',
            "If that sounds right, then you can click below to reset your password.",
            "If you didn't request a reset then don't worry, but do send me an email at scaryhackers@codecomments.dev to let me know.",
            "Have a 💯👌💪 day!"
        ]

        try:
            mailman.compose_and_send_message(
                to_address=email_address,
                subject="Password reset link",
                messages=messages,
                call_to_action_text="Click here to reset",
                call_to_action_url="https://codecomments.dev/profile/reset_password_link/" + user.username + "/" + password_reset_key
            )
        except:
            flask ("Error sending email. Please try again in a few minutes.", "danger")
            return redirect(redirect_url())

    flash("If I found that email address (not telling 😉) then I sent it a reset link", "success")
    return redirect(redirect_url())


@auth.route("/profile/reset_password_link/<username>/<password_reset_key>", methods=['GET', 'POST'])
def reset_password_link(username, password_reset_key):

    if password_reset_key == None or password_reset_key == "":
        flash("Invalid password reset key 🙅", "danger")
        return redirect(url_for('main_blueprint.new'))

    user = User.query.filter_by(username=username, password_reset_key=password_reset_key).first()

    if not user:
        flash("Invalid password reset key 🙅", "danger")
        return redirect(url_for('main_blueprint.new'))

    if user.password_reset_key == None:
        flash("Invalid password reset key 🙅", "danger")
        return redirect(url_for('main_blueprint.new'))

    if user.password_reset_expiry < datetime.utcnow():
        flash("Invalid password reset key 🙅", "danger")
        return redirect(url_for('main_blueprint.new'))

    if request.method == 'GET':
        return render_template('password_reset.html')

    if request.method == 'POST':

        new_password = request.form['password1']

        user.password = generate_password_hash(new_password, method='sha256')
        user.password_reset_key = "None"
        db.session.commit()

        flash ("Password successfully reset", "success")
        return redirect(url_for('main_blueprint.new'))
