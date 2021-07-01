from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app
from datetime import datetime

import coolname

from .models import Snapshot, Gist, Line



def get_id(snapshot_unique_reference):
    snapshot = Snapshot.query.filter_by(unique_reference = snapshot_unique_reference).first()
    return snapshot.id


def create():
    unique_reference = coolname.generate_slug(3)

    new_snapshot = Snapshot(
        unique_reference = unique_reference,
        date_snapped = datetime.now(),
    )
    db.session.add(new_snapshot)
    db.session.commit()

    return unique_reference