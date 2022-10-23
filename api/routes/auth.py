import sys

from json import dumps
from flask import abort, Blueprint, current_app, request, jsonify, Response
from flask_jwt import current_identity

from api.dao.auth import AuthDAO

auth_routes = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_routes.route('/register', methods=['POST'])
def register():
    form_data = request.get_json()

    email = form_data['email']
    print(email)
    password = form_data['password']
    print(password)

    dao = AuthDAO(current_app.driver, current_app.config.get('SECRET_KEY'))
    user_registered = dao.register(email, password)

    print('user_registered in routes\auth:')
    print(user_registered)

    if user_registered == None:
        return jsonify({'msg': 'email already registered', 'code': 406})
    return user_registered


@auth_routes.route('/login', methods=['POST'])
def login():

    form_data = request.get_json()

    username = form_data['username']
    print("username in login", username)
    password = form_data['password']
    print("password in login", password)
    dao = AuthDAO(current_app.driver, current_app.config.get('SECRET_KEY'))

    user = dao.authenticate(username, password)

    if user is False:
        return "Unauthorized", 401

    print("login successfully!")
    print(user['email'])
    print(user['username'])
    print(user['token'])

    return jsonify(user)

@auth_routes.route('/logout', methods=['POST'])
def logout():
    print("logout bye!")
    return jsonify({'success': True})

