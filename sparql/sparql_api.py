from functools import cache

from rdflib import Dataset


class SparqlAPI:
    def __init__(self, dataset="poke-a.nq"):
        self.dataset = Dataset()
        try:
            self.dataset.parse(dataset)
        except Exception as e:
            print(e)

    @cache
    def list_pokemons(self):
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
        return [str(result).split("Literal('")[1].split("'")[0] for result in results]


sparql_api = SparqlAPI()
