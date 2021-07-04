from flask import Flask, Blueprint, render_template, current_app, redirect, jsonify, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from . import app

comments = Blueprint('comments_blueprint', __name__)

from .models import Snapshot, Gist, Line, Comment


def create(line_id, content = None):

    line = Line.query.filter_by(id = line_id).first()

    new_comment = Comment(
        line_id = line_id,
        gist_id = line.gist_id,
        content = content
    )
    db.session.add(new_comment)
    db.session.commit()
    return new_comment.id


def edit(comment_id, comment_content):
    comment = Comment.query.filter_by(id = comment_id).first()
    comment.content = comment_content
    db.session.commit()


def get_content(comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    if comment:
        return comment.content
    else:
        return "## error ##"


def delete(comment_id):
    Comment.query.filter_by(id = comment_id).delete()
    db.session.commit()
    return


@comments.route('/api/comment', methods=['GET', 'POST', 'DELETE', 'PUT'])
def api_comment():

    # GET
    if request.method == "GET":
        comment_id = request.args.get('comment_id')
        if comment_id is None: return jsonify(status ="failed", reason ="no comment_id provided"), 404

        comment_content = get_content(comment_id)
        if comment_content == "## error ##":
            return jsonify(status = "failed", reason = "comment_id not found"), 404
        else:
            return jsonify(
                status = "success",
                comment_content = comment_content
            )

    # POST
    if request.method == "POST":

        request_data = request.json

        line_id = request_data['line_id']
        comment_content = request_data['comment_content']

        if line_id is None: return jsonify(status ="failed", reason ="no line_id provided"), 404
        if comment_content is None: return jsonify(status ="failed", reason ="no comment_content provided"), 404

        new_comment_id = create(line_id, comment_content)
        return jsonify(
            status = "success",
            new_comment_id = new_comment_id
        )

    # PUT to edit
    if request.method == "PUT":
        request_data = request.json

        comment_id = request_data['comment_id']
        comment_content = request_data['comment_content']

        if comment_id is None: return jsonify(status ="failed", reason ="no comment_id provided"), 404
        if comment_content is None: return jsonify(status ="failed", reason ="no comment_content provided"), 404

        edit(comment_id, comment_content)
        return jsonify(
            status = "success",
            comment_id = comment_id
        )

    # DELETE
    if request.method == "DELETE":
        request_data = request.json

        comment_id = request_data['comment_id']

        if comment_id is None: return jsonify(status ="failed", reason ="no comment_id provided"), 404

        delete(comment_id)

        return jsonify(
            status = "success"
        )


@comments.route('/api/script_comments/<gist_id>')
def api_gist_comment(gist_id):

    gist = Gist.query.filter_by(id = gist_id).first()

    output = []
    for comment in gist.comments:
        output.append({
            "comment_id": comment.id,
            "line_id": comment.line_id
        })

    return jsonify(output)

