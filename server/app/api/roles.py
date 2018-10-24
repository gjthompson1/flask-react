# app/api/search.py
from flask import Blueprint, jsonify, request

from app import db
from app.schema import Role

roles_blueprint = Blueprint('roles', __name__)

@roles_blueprint.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify({
        "roles":[role.to_dict() for role in roles]
    })
