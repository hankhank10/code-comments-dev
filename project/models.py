from . import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))

    # setup strings
    verified = db.Column(db.Boolean)
    unique_setup_key = db.Column(db.String(30))

    snapshots = db.relationship('Snapshot', backref='owner', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return self.id


class Snapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_author = db.Column(db.String[50])
    repo_name = db.Column(db.String[100])
    unique_suffix = db.Column(db.String[50])
    url = db.Column(db.String[300])

    owner_id = db.Column(db.ForeignKey('user.id'), nullable = False)

    date_snapped = db.Column(db.DateTime)

    gists = db.relationship('Gist', backref='snapshot', lazy=True)

    def unique_reference(self):
        return self.repo_author + "*" + self.repo_name + "*" + self.unique_suffix

    def __repr__(self):
        return self.unique_reference()



class Gist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.ForeignKey('snapshot.id'), nullable = False)
    filename = db.Column(db.String[50])
    url = db.Column(db.String[300])
    downloaded = db.Column(db.Boolean)
    content = db.Column(db.String[20000])

    lines = db.relationship('Line', backref='gist', lazy=True)

    def __repr__(self):
        return self.id


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gist_id = db.Column(db.ForeignKey('gist.id'), nullable = False)
    content = db.Column(db.String[1000])
    line_number = db.Column(db.Integer)

    comments = db.Relationship('Comment', backref='line', lazy=True)

    def __repr__(self):
        return self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.ForeignKey('line.id'), nullable = False)
    owner_id = db.Column(db.ForeignKey('user.id'), nullable = False)
    content = db.Column(db.String[1000])
