from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from project import mailman, gists, snapshots, pastebin_api

main = Blueprint('main_blueprint', __name__)

from .models import Snapshot, Gist, Line


@main.route('/')
def index():
    return render_template('index.html', snapshot=None, gist=None)

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

    if filename is None:
        gist = Gist.query.filter_by(snapshot_id = snapshot.id).first()
    else:
        gist = Gist.query.filter_by(snapshot_id = snapshot.id, filename = filename).first()

    lines = Line.query.filter_by(gist_id = gist.id).all()

    return render_template('view.html', snapshot = snapshot, gist = gist, lines = lines)


@main.route('/help')
def tutorial():

    tutorial_snapshot_unique_reference = snapshots.create(True)

    list_of_urls = [
        'https://github.com/hankhank10/code-comments-tutorial/blob/main/what-is-this.js',
        'https://github.com/hankhank10/code-comments-tutorial/blob/main/tutorial.md',
        'https://github.com/hankhank10/code-comments-tutorial/blob/main/supported_languages.py',
        'https://github.com/hankhank10/code-comments-tutorial/blob/main/tools_used.py',
        'https://github.com/hankhank10/code-comments-tutorial/blob/main/get_help.html'
    ]

    for url in list_of_urls:
        content, pastebin_unique_reference = pastebin_api.get_from_bin(url)
        gists.create_gist(
            filename=pastebin_unique_reference,
            content=content,
            snapshot_unique_reference=tutorial_snapshot_unique_reference)

    return redirect(url_for('main_blueprint.show_snapshot',
                            snapshot_unique_reference = tutorial_snapshot_unique_reference))