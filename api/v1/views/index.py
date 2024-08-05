#!/usr/bin/python3
""" This module defines the root page from our Flask API """

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns the API status  """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Returns an object containing each type's amount"""
    class_names = [Amenity, City, Place, Review, State, User]
    t_names = ["amenities", "cities", "places", "reviews", "states", "users"]

    count_objs = {}
    for i in range(len(class_names)):
        count_objs[t_names[i]] = storage.count(class_names[i])

    return jsonify(count_objs)
