# app/api/search.py
from flask import Blueprint, jsonify, request

from app import db

ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    post_data = request.get_json()
    return jsonify({
        'status': 'success',
        'message': 'pong!!'
    })
