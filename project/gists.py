from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from datetime import datetime

gists = Blueprint('gists_blueprint', __name__)

from . import snapshots

from .models import Snapshot, Gist, Line


def fix_name(snapshot_unique_reference, filename):

    # Get snapshot ID
    snapshot = Snapshot.query.filter_by(
        unique_reference=snapshot_unique_reference
    ).first()

    # Check if gist with that filename already exists
    original_filename = filename
    existing_file = True
    a = 0
    while existing_file:
        a = a + 1
        existing_file = Gist.query.filter_by(
            snapshot_id=snapshot.id,
            filename=filename
        ).first()

        if existing_file:
            filename = original_filename + ".copy" + str(a)

    return filename


def create_gist(filename, content, snapshot_unique_reference = None):

    # Check if new snapshot needs to be created
    if snapshot_unique_reference is None:
        snapshot_unique_reference = snapshots.create()

    # Get snapshot ID
    snapshot = Snapshot.query.filter_by(
        unique_reference = snapshot_unique_reference
    ).first()

    # Check if gist with that filename already exists
    filename = fix_name(snapshot_unique_reference, filename)

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


@gists.route('/<snapshot_unique_reference>/<filename>/delete')
def delete(snapshot_unique_reference, filename):

    snapshot = Snapshot.query.filter_by(unique_reference = snapshot_unique_reference).first_or_404()

    gist = Gist.query.filter_by(
        snapshot_id = snapshot.id,
        filename = filename
    ).first_or_404()

    Line.query.filter_by(gist_id = gist.id).delete()

    db.session.delete(gist)
    db.session.commit()

    flash(filename + " deleted from" + snapshot_unique_reference + ".", "success")

    return redirect(url_for('main_blueprint.show_snapshot', snapshot_unique_reference = snapshot_unique_reference))


@gists.route('/<snapshot_unique_reference>/<filename>/rename', methods=['POST'])
def rename(snapshot_unique_reference, filename):

    if 'new_filename' not in request.form:
        return jsonify(status = "error")

    new_filename = request.form['new_filename']

    # Check if gist with that filename already exists
    new_filename = fix_name(snapshot_unique_reference, new_filename)

    gist = Gist.query.filter_by(
        snapshot_id=snapshots.get_id(snapshot_unique_reference),
        filename=filename
    ).first()

    gist.filename = new_filename
    db.session.commit()

    flash("Script renamed "+ new_filename, "success")

    return redirect(url_for('main_blueprint.show_snapshot',
                            snapshot_unique_reference = snapshot_unique_reference,
                            filename = new_filename))