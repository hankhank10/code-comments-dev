from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify
from flask_login import login_required, current_user
from . import db
from . import app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .models import User

auth = Blueprint('auth_blueprint', __name__)


