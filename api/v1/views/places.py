#!/usr/bin/python3
""" This module handles the Restful Actions for the Places """
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def list_places(city_id):
    """
    Returns all the places of a City from the storage
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = storage.all(Place)
    places_list = []
    for place in places:
        if place.city_id == city.id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def find_place(place_id):
    """ Returns a place based on the ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one(place_id):
    """
    Removes a place from the storage based on the ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create(city_id):
    """
    Creates a new place on a city into the storage
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    req_body = request.get_json()
    obj = Place(**req_body)
    user = storage.get(User, obj.user_id)

    if not user:
        abort(404)

    obj.city_id = city.id
    obj.user_id = user.id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update(place_id):
    """
    Updates a place into the storage
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignorable = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    req_body = request.get_json()
    for key, value in req_body.items():
        if key not in ignorable:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
