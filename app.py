#We import the libraries we are going to use
from flask import Flask
from flask_restful import Api

#We import the views
from views import \
    PokemonsView, PokemonView 

#We create the app and the API
APP = Flask(__name__)
API = Api(APP)

#We add the routes, to each view
API.add_resource(PokemonsView, '/pokemon')
API.add_resource(PokemonView, '/pokemon/<string:arg>')
