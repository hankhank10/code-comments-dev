from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask_login import login_user, logout_user
import secrets

from .models import User


auth = Blueprint('auth_blueprint', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    #return redirect(url_for('main.index'))
    return "done"

