from functools import cache

from rdflib import Dataset


def split_row(row, seperator):
    return str(row[0]).split(seperator)[-1]


class SparqlAPI:
    def __init__(self, dataset="poke-a.nq"):
        self.dataset = Dataset()
        try:
            self.dataset.parse(dataset)
        except Exception as e:
            print(e)

    @cache
    def get_all_pokemons(self):
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

    def get_pokemons_matching_condition(self, query_condition, graph):
        query = f"""
        SELECT ?subject
        WHERE {{
            GRAPH {graph} {{
                {query_condition}
            }}
        }}
        """
        results = self.dataset.query(query)
        return [split_row(row, '/pokemon/') for row in results]

    def get_type_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasType> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)
        return [split_row(row, 'Type:') for row in results]

    def get_color_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasColour> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)

        items = [split_row(row, 'resource/') for row in results]
        if not items:
            return ''
        return items if len(items) > 1 else items[0]

    def get_habitat_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#foundIn> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)
        items = [split_row(row, 'Habitat:') for row in results]
        if not items:
            return ''
        return items if len(items) > 1 else items[0]

    def get_moves_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#isAbleToApply> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)
        items = [split_row(row, 'move/') for row in results]
        return items

    def get_shape_of(self, pokemon):
        query = f"""
        
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasShape> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)
        items = [split_row(row, 'Shape:') for row in results]
        if not items:
            return ''
        return items if len(items) > 1 else items[0]

    def get_possible_abilites_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#mayHaveAbility> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)
        return [split_row(row, 'ability/') for row in results]

    def get_hidden_abilites_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#mayHaveHiddenAbility> ?object .
            }}
        }}
        """
        results = self.dataset.query(query)
        return [split_row(row, 'ability/') for row in results]

    def get_catch_rate_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasCatchRate> ?object .
            }}
        }}
        """

        results = self.dataset.query(query)
        items = [split_row(row, 'Literal') for row in results]
        return items if len(items) > 1 else items[0]

    def get_height_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                ?object <http://qudt.org/schema/qudt/value> ?value .
                FILTER(CONTAINS(STR(?object), 'https://pokemonkg.org/instance/pokemon/{pokemon}/height'))
            }}
        }}
        """

        result = self.dataset.query(query)
        for row in result:
            return split_row(row, '/height/quantity/value/')
        return None

    def get_weight_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                ?object <http://qudt.org/schema/qudt/value> ?value .
                FILTER(CONTAINS(STR(?object), 'https://pokemonkg.org/instance/pokemon/{pokemon}/weight'))
            }}
        }}
        """

        result = self.dataset.query(query)
        for row in result:
            return split_row(row, '/weight/quantity/value/')
        return None

    def get_genus_of(self, pokemon):
        query = f"""
        SELECT ?object
        WHERE {{
            GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {{
                <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasGenus> ?object .
                FILTER (lang(?object) = "" || lang(?object) = "en")
            }}
        }}
        """

        results = self.dataset.query(query)
        items = [split_row(row, 'Shape:') for row in results]
        if not items:
            return ''
        return items if len(items) > 1 else items[0]

    def get_all_genus(self):
        query = """
        SELECT ?object
        WHERE {
            GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {
                ?subject <https://pokemonkg.org/ontology#hasGenus> ?object .
                FILTER (lang(?object) = "" || lang(?object) = "en")
            }
        }
        """

        results = self.dataset.query(query)
        return [split_row(row, 'Literal') for row in results]

    def get_all_types(self):
        query = """
        SELECT DISTINCT ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#hasType> ?object .
            }
        }
        """

        results = self.dataset.query(query)
        return [str(row[0]).split('#PokéType:')[-1] for row in results]

    def get_all_colors(self):
        query = """
        SELECT DISTINCT ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#hasColour> ?object .
            }
        }
        """
        results = self.dataset.query(query)
        return [split_row(row, '/resource/') for row in results]

    def get_all_hidden_abilites(self):
        query = """
        SELECT Distinct ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#mayHaveHiddenAbility> ?object .
            }
        }
        """
        results = self.dataset.query(query)
        return [split_row(row, '/ability/') for row in results]

    def get_all_possible_abilites(self):
        query = """
        SELECT Distinct ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#mayHaveAbility> ?object .
            }
        }
        """
        results = self.dataset.query(query)
        return [split_row(row, '/ability/') for row in results]

    def get_all_shapes(self):
        query = """
        SELECT Distinct ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#hasShape> ?object .
            }
        }
        """
        result = self.dataset.query(query)
        return [split_row(row, 'Shape:') for row in result]

    def get_all_heights(self):
        query = """
        SELECT ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <http://qudt.org/schema/qudt/quantityValue> ?object .
            }
        }
        """

        result = self.dataset.query(query)
        heights = []
        for row in result:
            height = split_row(row, '/height/quantity/value/')
            if height.endswith('M'):
                heights.append(height)

        return list(set(heights))

    def get_all_weights(self):
        query = """
        SELECT ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <http://qudt.org/schema/qudt/quantityValue> ?object .
            }
        }
        """

        result = self.dataset.query(query)
        weights = []
        for row in result:
            height = split_row(row, '/weight/quantity/value/')
            if height.endswith('G'):
                weights.append(height)
        return list(set(weights))

    def get_all_moves(self):
        query = """
        SELECT Distinct ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#isAbleToApply> ?object .
            }
        }
        """

        results = self.dataset.query(query)
        return [split_row(row, 'move/') for row in results]

    def get_all_habitats(self):
        query = """
        SELECT Distinct ?object
        WHERE {
            GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {
                ?subject <https://pokemonkg.org/ontology#foundIn> ?object .
            }
        }
        """

        results = self.dataset.query(query)
        return [split_row(row, 'Habitat:') for row in results]

    def get_all_catch_rate(self):
        query = """
        SELECT Distinct ?object
        WHERE {
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
                ?subject <https://pokemonkg.org/ontology#hasCatchRate> ?object .
            }
        }
        """

        result = self.dataset.query(query)
        return [split_row(row, 'Literal') for row in result]

    def get_pokemons_by_height_or_weight(self, value, attribute):
        query = """
        SELECT ?subject
        WHERE {{
            GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
                ?subject <http://qudt.org/schema/qudt/value> ?object .
            }}
        }}
        """
        results = self.dataset.query(query)
        pokemons = []
        if attribute == 'height':
            sep = '/height/quantity/value/'
        else:
            sep = '/weight/quantity/value/'
        for row in results:
            item_value = split_row(row, sep)
            if item_value == value:
                pokemon = str(row).split('/pokemon/')[1].split(f'/{attribute}/')[0]
                pokemons.append(pokemon)
        return pokemons

    def get_pokemon_info(self, pokemon):
        print(f'Pokemon name: {pokemon}')
        print("Types:")
        for type in self.get_type_of(pokemon):
            print("\t" + type)
        print("Color: " + self.get_color_of(pokemon))
        print("Shape: " + self.get_shape_of(pokemon))
        print("Catch Rate: " + self.get_catch_rate_of(pokemon))
        print("Weight: " + self.get_weight_of(pokemon))
        print("Height: " + self.get_height_of(pokemon))
        print("Habitat: " + self.get_habitat_of(pokemon))
        print("Genus: " + self.get_genus_of(pokemon))
        print("Moves:")
        for move in self.get_moves_of(pokemon):
            print("\t" + move)

        print("Possible abilities:")
        for possibleAbilities in self.get_possible_abilites_of(pokemon):
            print("\t" + possibleAbilities)

        print("Hidden abilities:")
        for hiddenAbilities in self.get_hidden_abilites_of(pokemon):
            print("\t" + hiddenAbilities)


sparql_api = SparqlAPI()
