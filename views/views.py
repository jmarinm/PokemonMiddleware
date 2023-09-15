# Description: This file contains the views of the API
# Path: views/views.py

# We import the libraries we are going to use
from flask_restful import Resource
from flask import jsonify, make_response, request
import requests

# We create the constants, the URL of the Pokedex API and the URL of the local server
POKEDEX_URL = "https://pokeapi.co/api/v2"
LOCAL_URL = "http://localhost:5000"

class PokemonsView(Resource):
    """
    This class is the view for the list of pokemons
    """
    def get(self):
        """
        This method is the GET method for the list of pokemons
        Returns:
            A list of pokemons
        """
        #If there is a page parameter, we return the page
        if request.args.get("page"):
            return self.get_pokedex_page(int(request.args.get("page")))
        #If there is no page parameter, we return all the pokemons
        else:
            return self.get_all_pokemon()

    def get_pokedex_page(self, page):
        """
        This method returns a page of the pokedex
        Args:
            page: The page number
        Returns:
            A list of the 20 pokemons of a page"""
        #We get the page of the pokedex
        res = requests.get(f"{POKEDEX_URL}/pokemon?offset={(page-1)*20}")
        #If the page is not found, we return an error
        if res.json()["results"] == []:
            return make_response({"error": "Page not found"}, 404)
        #If the page is found, we return the list of pokemons
        return make_response(self.list_pokemon(res.json()["results"]), 200)

    def get_all_pokemon(self):
        """
        This method returns all the pokemons
        Returns:
            A list of all the pokemons
        """
        #We get the number of pokemons
        res = requests.get(f"{POKEDEX_URL}/pokemon?limit=1")
        #We get the list of pokemons
        res = requests.get(f'{POKEDEX_URL}/pokemon?limit={res.json()["count"]}')
        pokemon_list = self.list_pokemon(res.json()["results"])
        return make_response(pokemon_list, 200)

    def list_pokemon(self, pokemons):
        """
        This method returns a list of pokemons
        Args:
            pokemons: The list of pokemons from the pokeapi
        Returns:
            A list of pokemons with the name and the resource
        """
        pokemon_list = []
        for pokemon in pokemons:
            resource = pokemon["url"].split("/")[-2]
            pokemon_list.append({"name": pokemon["name"], "resource": resource})
        return pokemon_list

# A view for a pokemon is created
class PokemonView(Resource):
    """
    This class is the view for a pokemon
    """
    def get(self, arg):
        """
        This method is the GET method for a pokemon
        Args:
            arg: The name or the id of the pokemon
        Returns:
            A pokemon
        """
        #We get the pokemon from the pokeapi
        pokemonReq = requests.get(f"{POKEDEX_URL}/pokemon/{arg}")
        #If the pokemon is not found, we return an error
        if pokemonReq.status_code == 404:
            return make_response({"error": "Pokemon not found"}, 404)
        #If the pokemon is found, we return the pokemon
        return make_response(self.transform_pokemon(pokemonReq.json()), 200)

    def transform_pokemon(self, pokemon_data):
        """
        This method transforms the pokemon from the pokeapi to the pokemon with the data needed in this app
        Args:
            pokemon_data: The pokemon from the pokeapi
        Returns:
            A pokemon with the data needed in this app
        """
        pokemon = {
            "name":pokemon_data["name"],
            # We iterate over the abilities to get the name of each one
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
            "pokedex_number": pokemon_data["id"],
            # We iterate over the types to get the name of each one
            "types": [type["type"]["name"] for type in pokemon_data["types"]],
            "sprites": pokemon_data["sprites"],
        }
        return pokemon