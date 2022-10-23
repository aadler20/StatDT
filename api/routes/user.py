import sys

from flask import Blueprint, current_app, request, jsonify
from flask_jwt import current_identity

from api.dao.auth import AuthDAO

user_routes = Blueprint("user", __name__, url_prefix="/api/user")


@user_routes.route('/info', methods=['GET'])
def user_info():

    form_data = request.get_json()

    print('Hello user_info')

    print('request.headers')
    print(request.headers)

    token = request.headers.get('Access-Token')
    print('token:\n' + token)

    dao = AuthDAO(current_app.driver, current_app.config.get('SECRET_KEY'))
    user = dao.decode_token(token)

    print('user:')
    print(user)

    if user is None:
        return "Unauthorized", 401
    return jsonify(user)
