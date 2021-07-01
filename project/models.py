from . import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))

    is_superuser = db.Column(db.Boolean)

    # setup strings
    verified = db.Column(db.Boolean)
    unique_setup_key = db.Column(db.String(30))

    snapshots = db.relationship('Snapshot', backref='owner', lazy=True)
    #comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return self.id


class Snapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    unique_reference = db.Column(db.String(100))
    secret_key = db.Column(db.String(25))

    #github specific stuff
    repo_author = db.Column(db.String(50))
    repo_name = db.Column(db.String(100))
    url = db.Column(db.String(300))

    owner_id = db.Column(db.ForeignKey('user.id'))

    date_snapped = db.Column(db.DateTime)

    gists = db.relationship('Gist', backref='snapshot', lazy=True)

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

    lines = db.relationship('Line', backref='gist', lazy=True)

    def __repr__(self):
        return self.id


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gist_id = db.Column(db.ForeignKey('gist.id'), nullable = False)
    content = db.Column(db.String(1000))
    line_number = db.Column(db.Integer)

    comments = db.relationship('Comment', backref='line', lazy=True)

    def __repr__(self):
        return self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.ForeignKey('line.id'), nullable = False)
    #owner_id = db.Column(db.ForeignKey('user.id'), nullable = False)
    content = db.Column(db.String(1000))
