#!/usr/bin/python3
"""cities view for the API"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_city(state_id=None, city_id=None):
    """handler for the cities endpoint"""
    handler_dict = {
        'GET': get_cities,
        'DELETE': remove_city,
        'POST': add_city,
        'PUT': update_city,
    }
    if request.method in handler_dict:
        return handler_dict[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handler_dict.keys()))


def get_cities(state_id=None, city_id=None):
    """get the city"""
    if state_id:
        state = storage.get(State, state_id)
        if state:
            cities = list(map(lambda x: x.to_dict(), state.cities))
            return jsonify(cities)
    elif city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
    raise NotFound()


def remove_city(state_id=None, city_id=None):
    """remove a city"""
    if city_id:
        city = storage.get(City, city_id)
        if city:
            storage.delete(city)
            if storage_t != "db":
                for place in storage.all(Place).values():
                    if place.city_id == city_id:
                        for review in storage.all(Review).values():
                            if review.place_id == place.id:
                                storage.delete(review)
                        storage.delete(place)
            storage.save()
            return jsonify({}), 200
        raise NotFound()


def add_city(state_id=None, city_id=None):
    """Add a new city"""
    state = storage.get(State, state_id)
    if not state:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


def update_city(state_id=None, city_id=None):
    """update the city"""
    key = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        city = storage.get(City, city_id)
        if city:
            data = request.get_json()
            if type(data) is not dict:
                raise BadRequest(description='Not a JSON')
            for k, v in data.items():
                if k not in key:
                    setattr(city, k, v)
                city.save()
                return jsonify(city.to_dict()), 200
    raise NotFound()
