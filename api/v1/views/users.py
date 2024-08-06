#!/usr/bin/python3
""" This module handles the Restful actions for the User """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """
    Returns all the users from the storage
    """
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def find_user(user_id):
    """ Returns an user based on the ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Removes an user from the storage based on the ID
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new user into the storage
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")

    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    req_body = request.get_json()
    obj = User(**req_body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an user into the storage
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignorable = ['id', 'email', 'created_at', 'updated_at']

    req_body = request.get_json()
    for key, value in req_body.items():
        if key not in ignorable:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
