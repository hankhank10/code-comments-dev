from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
from werkzeug.utils import secure_filename
import os
import coolname

from datetime import datetime


loader = Blueprint('loader_blueprint', __name__)

from .models import Snapshot, Gist, Line


def create_snapshot():
    unique_reference = coolname.generate_slug(3)

    new_snapshot = Snapshot(
        unique_reference = unique_reference,
        date_snapped = datetime.now(),
    )
    db.session.add(new_snapshot)
    db.session.commit()

    return unique_reference


def create_gist(filename, content, snapshot_unique_reference = None):

    # Check if new snapshot needs to be created
    if snapshot_unique_reference is None:
        snapshot_unique_reference = create_snapshot()

    # Get snapshot ID
    snapshot = Snapshot.query.filter_by(
        unique_reference = snapshot_unique_reference
    ).first()

    # Check if gist with that filename already exists
    original_filename = filename
    existing_file = True
    a = 0
    while existing_file:
        a = a + 1
        existing_file = Gist.query.filter_by(
            snapshot_id = snapshot.id,
            filename = filename
        ).first()

        if existing_file:
            filename = original_filename + ".copy" + str(a)

    # Create gist
    new_gist = Gist(
        snapshot_id = snapshot.id,
        filename = filename,
        downloaded = True
    )
    db.session.add(new_gist)
    db.session.commit()

    # Create lines
    lines = content.splitlines()

    a = 0
    for line in lines:
        a = a + 1
        new_line = Line(
            gist_id = new_gist.id,
            line_number = a,
            content = line
        )
        db.session.add(new_line)

    db.session.commit()

    return snapshot_unique_reference, filename


@loader.route('/load/file', methods=['POST'])
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

    snapshot_unique_reference, filename = create_gist(
        filename = write_file.filename,
        content = content,
        snapshot_unique_reference = snapshot_unique_reference)

    return jsonify(
        message="ok",
        snapshot_unique_reference = snapshot_unique_reference,
        gist_filename = filename
    ), 201


@loader.route('/<snapshot_unique_reference>/<filename>/delete')
def delete_gist(snapshot_unique_reference, filename):

    snapshot = Snapshot.query.filter_by(unique_reference = snapshot_unique_reference).first_or_404()

    gist = Gist.query.filter_by(
        snapshot_id = snapshot.id,
        filename = filename
    ).first_or_404()

    Line.query.filter_by(gist_id = gist.id).delete()

    db.session.delete(gist)
    db.session.commit()

    return redirect(url_for('main_blueprint.show_snapshot', snapshot_unique_reference = snapshot_unique_reference))