from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app

import secrets
import os

from . import gists
from . import pastebin_api


loader = Blueprint('loader_blueprint', __name__)

from .models import Snapshot, Gist, Line


@loader.route('/load/file/', methods=['POST'])
@loader.route('/load/file/<snapshot_unique_reference>', methods=['POST'])
def file_upload(snapshot_unique_reference = None):

    if len(request.files) == 0:
        return jsonify(
            error="No file in request"
        ), 400

    write_file = request.files['file']
    temporary_filename = secrets.token_hex(20)
    temporary_path = os.path.join(app.config['UPLOAD_FOLDER'], temporary_filename)
    write_file.save(temporary_path)

    with open(temporary_path, 'r') as read_file:
        content = read_file.read()

    snapshot_unique_reference, filename = gists.create_gist(
        filename = write_file.filename,
        content = content,
        snapshot_unique_reference = snapshot_unique_reference)

    flash("Script " + filename + " uploaded to " + snapshot_unique_reference, "success")

    return jsonify(
        status="success",
        snapshot_unique_reference = snapshot_unique_reference,
        gist_filename = filename
    ), 201


@loader.route('/load/pastebin/', methods=['POST'])
@loader.route('/load/pastebin/<snapshot_unique_reference>', methods=['POST'])
def load_from_pastebin(snapshot_unique_reference = None):

    pastebin_url = request.form.get('pastebin_url')
    content, pastebin_unique_reference = pastebin_api.get_from_bin(pastebin_url)

    if content == "error":
        flash("URL not available 🤦🏻‍️", "danger")
        if snapshot_unique_reference:
            return redirect(url_for('main_blueprint.show_snapshot', snapshot_unique_reference=snapshot_unique_reference))
        return redirect(url_for('main_blueprint.new'))

    snapshot_unique_reference, filename = gists.create_gist(
        filename=pastebin_unique_reference,
        content=content,
        snapshot_unique_reference=snapshot_unique_reference,
        url = request.form.get('pastebin_url'))

    return redirect(url_for('main_blueprint.show_snapshot',
                    snapshot_unique_reference=snapshot_unique_reference,
                    filename=filename))
