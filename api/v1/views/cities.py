#!/usr/bin/python3
""" This module handles the Restful Actions for the Cities """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """
    Returns all the cities of a State from the storage
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in storage.all(City).values()
        if city.state_id == state.id]
    
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def find_city(city_id):
    """ Returns a city based on the ID """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Removes a city from the storage based on the ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new city on a state into the storage
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    req_body = request.get_json()
    obj = City(**req_body)
    obj.state_id = state.id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a city into the storage
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignorable = ['id', 'created_at', 'updated_at']

    req_body = request.get_json()
    for key, value in req_body.items():
        if key not in ignorable:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
