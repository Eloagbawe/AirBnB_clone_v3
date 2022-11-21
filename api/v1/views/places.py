#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_places(city_id):
    """Retrieves the list of all Place objects based on the city_id"""
    city = storage.get(City, city_id)

    if city:
        places = city.places
        places_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place based on it's ID"""
    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place based on it's ID"""
    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """Adds a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(place, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
