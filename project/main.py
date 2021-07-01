from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app

main = Blueprint('main_blueprint', __name__)

from .models import Snapshot, Gist, Line

@main.route('/')
@main.route('/new-script')
def new():

    return render_template('upload.html', snapshot=None, gist=None)


@main.route('/<snapshot_unique_reference>/')
@main.route('/<snapshot_unique_reference>/<filename>')
def show_snapshot(snapshot_unique_reference, filename = None):

    snapshot = Snapshot.query.filter_by(unique_reference = snapshot_unique_reference).first_or_404()

    if filename == "new-script":
        return render_template('upload.html', snapshot=snapshot, gist=None)

    if len(snapshot.gists) == 0:
        return render_template('upload.html', snapshot=snapshot, gist=None)

    if filename == None:
        gist = Gist.query.filter_by(snapshot_id = snapshot.id).first()
    else:
        gist = Gist.query.filter_by(snapshot_id = snapshot.id, filename = filename).first()

    lines = Line.query.filter_by(gist_id = gist.id).all()

    return render_template('view.html', snapshot = snapshot, gist = gist, lines = lines)


