from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app

import secrets
import os

from datetime import datetime

from . import gists


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


