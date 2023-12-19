from rdflib import Dataset
import random


class Game:
    def __init__(self):
        self.dataset = Dataset()
        try:
            self.dataset.parse("poke-a.nq")
        except Exception as e:
            print(e)

    def draw_pokemon(self):
        query = """
        SELECT ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/pokewiki-de-pokemonlist> {
                ?subject ?predicate ?object .
                FILTER (?predicate = <http://www.w3.org/2000/01/rdf-schema#label>)
                FILTER (lang(?object) = "" || lang(?object) = "en")
            }
        }
        """

        results = self.dataset.query(query)
        pokemons = []
        for result in results:
            pokemon = str(result).split("Literal('")[1].split("'")[0]
            pokemons.append(pokemon)

        return random.choice(pokemons).lower()


game_api = Game()
