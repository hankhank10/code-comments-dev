from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from datetime import datetime

import coolname

from .models import Snapshot, Gist, Line


snapshots = Blueprint('snapshots_blueprint', __name__)


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@snapshots.get('/<snapshot_unique_reference>/claim_ownership')
def claim_ownership(snapshot_unique_reference):

    snapshot = Snapshot.query.filter_by(unique_reference=snapshot_unique_reference).first()

    if snapshot.owner_id != None:
        flash("This comment set cannot be claimed as it is already owned 🤷🏻‍", "danger")

    snapshot.owner_id = current_user.id
    db.session.commit()

    flash ("Congratulations, this comment set is now yours 🙌", "success")
    return redirect(url_for('main_blueprint.show_snapshot', snapshot_unique_reference = snapshot_unique_reference))


@snapshots.post('/<snapshot_unique_reference>/give_name')
def give_nickname(snapshot_unique_reference):

    new_nickname = request.form['new_snapshot_name']

    snapshot = Snapshot.query.filter_by(unique_reference=snapshot_unique_reference).first()

    if new_nickname == "":
        snapshot.nickname = None
        flash("Comment set name deleted.", "success")
    else:
        snapshot.nickname = new_nickname
        flash("Comment set given nickname " + new_nickname, "success")
    db.session.commit()

    return redirect(redirect_url())


def get_id(snapshot_unique_reference):
    snapshot = Snapshot.query.filter_by(unique_reference = snapshot_unique_reference).first()
    return snapshot.id


def create():
    unique_reference = coolname.generate_slug(3)

    owner_id = None
    if current_user.is_authenticated:
        owner_id = current_user.id

    new_snapshot = Snapshot(
        unique_reference = unique_reference,
        date_snapped = datetime.now(),
        owner_id = owner_id
    )
    db.session.add(new_snapshot)
    db.session.commit()

    return unique_reference
