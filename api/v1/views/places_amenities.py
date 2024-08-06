#!/usr/bin/python3
""" This module handles the Restful Actions for the Place Amenities """
from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
    strict_slashes=False)
def list_place_amenities(place_id):
    """
    Returns all the amenities of a Place from the storage
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Removes an place-amenity from the storage based on both IDs
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        place.amenities.remove(amenity)
        storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                methods=['POST'], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """
    Creates a new relation place-amenity into the storage
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        place.amenities.append(amenity)
        storage.save()
        status = 201
    else:
        status = 200

    return make_response(jsonify(amenity.to_dict()), status)
