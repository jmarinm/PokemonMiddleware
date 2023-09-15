from unittest import TestCase
from app import APP


class PokemonTest(TestCase):
    """
    This class is the test for the pokemon
    """
    def setUp(self):
        """
        This method is executed before the tests
        """
        #We create the client for the tests
        self.client = APP.test_client()
        APP.config['TESTING'] = True

    def test_get_pokemon_by_name(self):
        """
        This method tests the GET method for a pokemon by name
        """
        #We get the pokemon
        response = self.client.get('/pokemon/charizard')
        pokemon = response.json
        #We check the response
        self.assertEqual(response.status_code, 200)
        #We check the pokemon name
        self.assertEqual(pokemon["name"], "charizard")
        #We check the pokemon pokedex number
        self.assertEqual(pokemon["pokedex_number"], 6)
        #We check the pokemon types
        self.assertEqual(pokemon["types"], ["fire", "flying"])
        #We check the pokemon abilities
        self.assertEqual(pokemon["abilities"], ["blaze", "solar-power"])
        #We check that the pokemon has sprites
        self.assertIn("sprites", pokemon)
    
    def test_get_pokemon_by_id(self):
        """
        This method tests the GET method for a pokemon by id
        """
        #We get the pokemon
        response = self.client.get('/pokemon/6')
        pokemon = response.json
        #We check the response
        self.assertEqual(response.status_code, 200)
        #We check the pokemon name
        self.assertEqual(pokemon["name"], "charizard")
        #We check the pokemon pokedex number
        self.assertEqual(pokemon["pokedex_number"], 6)
        #We check the pokemon types
        self.assertEqual(pokemon["types"], ["fire", "flying"])
        #We check the pokemon abilities
        self.assertEqual(pokemon["abilities"], ["blaze", "solar-power"])
        #We check that the pokemon has sprites
        self.assertIn("sprites", pokemon)

    def test_get_pokemon_not_found_by_id(self):
        """
        This method tests the GET method for a pokemon by id
        """
        #We get a pokemon that does not exist
        response = self.client.get('/pokemon/5000')
        #We check the response is 404
        self.assertEqual(response.status_code, 404)
        #We check the response has the error message
        self.assertEqual(response.json, {"error": "Pokemon not found"})
    
    def test_get_pokemon_not_found_by_name(self):
        """
        This method tests the GET method for a pokemon by name
        """
        #We get a pokemon that does not exist
        response = self.client.get('/pokemon/asdasdasdas')
        #We check the response is 404
        self.assertEqual(response.status_code, 404)
        #We check the response has the error message
        self.assertEqual(response.json, {"error": "Pokemon not found"})

    def test_get_pokemon_page(self):
        """
        This method tests the GET method for a pokemon page
        """
        #We get the pokemon page
        response = self.client.get('/pokemon?page=1')
        poke_list = response.json
        #We check the response is 200
        self.assertEqual(response.status_code, 200)
        #We check the response is a list
        self.assertIsInstance(poke_list, list)
        #We check the response has 20 pokemons
        self.assertEqual(len(poke_list), 20)
        #We check the items of the have the name and the resource
        self.assertIn("resource", poke_list[0])
        self.assertIn("name", poke_list[0])
        #We check the first pokemon is bulbasaur
        self.assertEqual(poke_list[0]["name"], "bulbasaur")

    def test_get_pokemon_page_not_found(self):
        """
        This method tests the GET method for a pokemon page
        """
        #We get a pokemon page that does not exist
        response = self.client.get('/pokemon?page=999')
        #We check the response is 404
        self.assertEqual(response.status_code, 404)
        #We check the response has the error message
        self.assertEqual(response.json, {"error": "Page not found"})

    def test_get_all_pokemon(self):
        """
        This method tests the GET method for all the pokemons
        """
        #We get all the pokemons
        response = self.client.get('/pokemon')
        poke_list = response.json
        #We check the response is 200
        self.assertEqual(response.status_code, 200)
        #We check the response is a list
        self.assertIsInstance(poke_list, list)
        #We check the response has 1281 pokemons
        self.assertEqual(len(poke_list), 1281)
        #We check the items of the have the name and the resource
        self.assertIn("resource", poke_list[0])
        self.assertIn("name", poke_list[0])
        #We check the first pokemon is bulbasaur
        self.assertEqual(poke_list[0]["name"], "bulbasaur")


    def tearDown(self) -> None:
        APP.config['TESTING'] = False
        return super().tearDown()
    
    