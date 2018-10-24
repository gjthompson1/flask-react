# app/api/search.py
from flask import Blueprint, jsonify, request

from app import db
from app.schema import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        "users": [user.to_dict() for user in users]
    })
