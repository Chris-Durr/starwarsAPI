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
from models import db, User, People, Planets, Fav_people, Fav_planets
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
def get_user():
    alluser = User.query.all() 
    alluser = list(map(lambda elemento: elemento.serialize(),
    alluser)) 
    print(alluser)
    return jsonify({"resultado":alluser})

    return jsonify(response_body), 200
# Aqui uestras rutas
@app.route('/people', methods=['GET'])
def get_people():
    allpeople = People.query.all()  #retorna un arreglo de clases
    allpeople = list(map(lambda elemento: elemento.serialize(),
    allpeople)) # iteron en cada clase y almaceno el resultado de la funcion serialize
    print(allpeople)
    return jsonify({"resultado":allpeople})

@app.route('/planets', methods=['GET'])
def get_planets():
    allplanets = Planets.query.all() 
    allplanets = list(map(lambda elemento: elemento.serialize(),
    allplanets)) 
    print(allplanets)
    return jsonify({"resultado":allplanets})

@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    #bajo un parametro especifico
    #onepeople = People.query.filter_by(id=id).first()
    #buscar solo por ID
    onepeople = People.query.get(id)
    if onepeople:
        onepeople = onepeople.serialize()
        return jsonify({"resultado": onepeople})
    else:
        return jsonify({"resultado": "Try harder, young padawan"})

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    oneplanet = Planets.query.get(id)
    if oneplanet:
        oneplanet = oneplanet.serialize()
        return jsonify({"resultado": oneplanet})
    else:
        return jsonify({"resultado": "The planet you're looking for is not in the archive"})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    onepeople = People.query.get(people_id)
    if onepeople:
        new = Fav_people()
        new.user_id = 1
        new.people_id = people_id
        db.session.add(new) #agregar rejistro a la Base de Datos
        db.session.commit() #guardar los cambios
        return jsonify({"resultado": "Success! Woho!"})
    else:
        return jsonify({"resultado": "Try harder, young padawan"})

@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def add_fav_planets(planets_id):
    oneplanet = Planets.query.get(planets_id)
    if oneplanet:
        new = Fav_planets()
        new.user_id = 1
        new.planets_id = planets_id
        db.session.add(new) #agregar rejistro a la Base de Datos
        db.session.commit() #guardar los cambios
        return jsonify({"resultado": "Success! Woho!"})
    else:
        return jsonify({"resultado": "Try harder, young padawan"})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
