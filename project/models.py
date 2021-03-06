from . import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)

    is_superuser = db.Column(db.Boolean)

    # setup strings
    verified = db.Column(db.Boolean)
    unique_setup_key = db.Column(db.String(30))

    # password reset
    password_reset_key = db.Column(db.String(30))
    password_reset_expiry = db.Column(db.DateTime)

    snapshots = db.relationship('Snapshot', backref='owner', lazy=True)
    #comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return self.id


class Snapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    unique_reference = db.Column(db.String(100))
    nickname = db.Column(db.String(100))

    #github specific stuff
    repo_author = db.Column(db.String(50))
    repo_name = db.Column(db.String(100))
    url = db.Column(db.String(300))

    owner_id = db.Column(db.ForeignKey('user.id'))

    tutorial = db.Column(db.Boolean)

    @property
    def restricted(self):
        if self.owner_id == None:
            return False
        else:
            return True

    date_snapped = db.Column(db.DateTime)
    date_last_comment = db.Column(db.DateTime)

    @property
    def date_snapped_timestamp(self):
        return datetime.timestamp(self.date_snapped)

    @property
    def display_name(self):
        if self.nickname == None:
            return self.unique_reference
        else:
            return self.nickname


    gists = db.relationship('Gist', backref='snapshot', lazy=True)

    @property
    def gist_count(self):
        gist_count = Gist.query.filter_by(snapshot_id = self.id).count()
        return gist_count

    @property
    def comment_count(self):
        comment_count = Comment.query.filter_by(owner_id = self.id).count()
        return comment_count

    def __repr__(self):
        return self.unique_reference()


class Gist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    snapshot_id = db.Column(db.ForeignKey('snapshot.id'), nullable = False)

    def snapshot_unique_reference(self):
        snapshot = Snapshot.query.filter_by(id = self.snapshot_id).first()
        return snapshot.unique_reference

    filename = db.Column(db.String(50))
    url = db.Column(db.String(300))
    downloaded = db.Column(db.Boolean, default=True)

    file_type = db.Column(db.String(20))

    lines = db.relationship('Line', backref='gist', lazy=True)
    comments = db.relationship('Comment', backref='gist', lazy=True)

    @property
    def owner_id(self):
        return self.snapshot.owner_id

    @property
    def restricted(self):
        return self.snapshot.restricted

    def __repr__(self):
        return self.id


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gist_id = db.Column(db.ForeignKey('gist.id'), nullable = False)
    content = db.Column(db.String(1000))
    line_number = db.Column(db.Integer)

    comments = db.relationship('Comment', backref='line', lazy=True)

    @property
    def owner_id(self):
        return self.gist.owner_id

    @property
    def restricted(self):
        return self.gist.restricted

    def __repr__(self):
        return self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.ForeignKey('line.id'), nullable = False)
    gist_id = db.Column(db.ForeignKey('gist.id'), nullable = False)
    content = db.Column(db.String(1000))

    @property
    def owner_id(self):
        return self.line.owner_id

    @property
    def restricted(self):
        return self.line.restricted

    def __repr__(self):
        return self.id
