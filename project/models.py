from . import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))

    # setup strings
    verified = db.Column(db.Boolean)
    unique_setup_key = db.Column(db.String(30))

    def __repr__(self):
        return self.id


class Snapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_author = db.Column(db.String[50])
    repo_name = db.Column(db.String[100])
    unique_suffix = db.Column(db.String[50])

    url = db.Column(db.String[300])

    date_snapped = db.Column(db.DateTime)

    def unique_reference(self):
        return self.repo_author + "*" + self.repo_name + "*" + self.unique_suffix

    def __repr__(self):
        return self.unique_reference()

    owner = db.Column(db.ForeignKey('user.id'), nullable = False)


class Gist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot = db.Column(db.ForeignKey('snapshot.id'), nullable = False)
    filename = db.Column(db.String[50])
    url = db.Column(db.String[300])
    downloaded = db.Column(db.Boolean)
    content = db.Column(db.String[20000])

    def __repr__(self):
        return self.id


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gist = db.Column(db.ForeignKey('gist.id'), nullable = False)
    content = db.Column(db.String[1000])
    line_number = db.Column(db.Integer)

    def __repr__(self):
        return self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.ForeignKey('line.id'), nullable = False)
    owner = db.Column(db.ForeignKey('user.id'), nullable = False)
    content = db.Column(db.String[1000])
