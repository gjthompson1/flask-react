# app/api/search.py
import sys
from flask import Blueprint, jsonify, request, make_response, render_template
from sqlalchemy import exc

from app import db
from app.lib import elastickit
from app.lib import mlkit

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/ping', methods=['POST'])
def ping_pong():
    post_data = request.get_json()
    return jsonify({
        'status': 'success',
        'message': 'pong!!'
    })
