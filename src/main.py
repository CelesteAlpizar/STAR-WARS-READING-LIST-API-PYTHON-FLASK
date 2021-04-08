"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_allUsers():

    return jsonify(User.uservalues()), 200

@app.route('/user', methods=['POST'])
def handle_addUsers():
    request_body_user=request.data
    decoded_object = json.loads(request_body_user)
    return jsonify(User.add_user(decoded_object)), 200

@app.route('/characters', methods=['GET'])
def handle_allCharacters():

    return jsonify(Character.charactersvalues()), 200

@app.route('/characters', methods=['POST'])
def handle_addCharacters():
    request_body_character=request.data
    decoded_object = json.loads(request_body_character)
    return jsonify(Character.add_character(decoded_object)), 200

@app.route('/planets', methods=['GET'])
def handle_allPlanets():

    return jsonify(Planet.planetsvalues()), 200

@app.route('/planets', methods=['POST'])
def handle_addPlanets():
    request_body_planet=request.data
    decoded_object = json.loads(request_body_planet)
    return jsonify(Planet.add_planet(decoded_object)), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
