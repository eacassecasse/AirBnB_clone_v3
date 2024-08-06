#!/usr/bin/python3
""" This module handles the Restful Actions for the Reviews """
from models.user import User
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def list_reviews(place_id):
    """
    Returns all the reviews of a Place from the storage
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in storage.all(Review).values()
        if review.place_id == place.id]
    
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def find_review(review_id):
    """ Returns a review based on the ID """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Removes a review from the storage based on the ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new review on a place into the storage
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    req_body = request.get_json()
    obj = Review(**req_body)

    user = storage.get(User, obj.user_id)

    if not user:
        abort(404)

    obj.place_id = place.id
    obj.user_id = user.id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a review into the storage
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignorable = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    req_body = request.get_json()
    for key, value in req_body.items():
        if key not in ignorable:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
