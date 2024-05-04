#!/usr/bin/python3
"""A module that contains the index view"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """get the status of the API"""
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    """retrieves the number of each objects by type"""
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for k, v in objects.items():
        objects[k] = storage.count(v)
    return jsonify(objects)
