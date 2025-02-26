"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favoritos
#from models import Person
CURRENT_USER_ID=1

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_active = request.json.get("is_active", True)
    new_user = User(email = email, password = password, is_active = is_active)

    db.session.add(new_user)
    db.session.commit

    return jsonify({"msg" : "user created succesfully"})


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = [user.serialize() for user in users ]
    return jsonify({"result" : result})

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]

    return jsonify({"result" : result})

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"msg" : "planeta no existe"})
    return jsonify(planet.serialize())

@app.route ('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person == None:
        return jsonify({"msg" : "person doesnt exist"})
    return jsonify(person.serialize())

@app.route('/user/favorites', methods = ['GET'])
def get_favorites():
    favoritos = Favoritos.query.filter_by(user_id=CURRENT_USER_ID).all()
    if favoritos == []:
        return jsonify({"message" : "no favorites added"})
    return jsonify([favorito.serialize() for favorito in favoritos])

@app.route('/favorite/planet/<int:planet_id>',methods = ['POST'])
def add_favorite_planet(planet_id):
    add_planet = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if add_planet is None:
        new_planet = Favoritos(user_id=CURRENT_USER_ID, planet_id=planet_id)
        db.session.add(new_planet)
        db.session.commit
    return jsonify({"msg" : "planet added to favorites"})







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



 

