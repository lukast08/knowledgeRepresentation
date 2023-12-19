from rdflib import Dataset
dataset = Dataset()
try:
    dataset.parse("poke-a.nq")
except Exception as e:
    print(e)

query = """
SELECT ?object
WHERE {
  GRAPH <https://pokemonkg.org/dataset/pokewiki-de-pokemonlist> {
    ?subject ?predicate ?object .
    FILTER (?predicate = <http://www.w3.org/2000/01/rdf-schema#label>)
    FILTER (lang(?object) = "" || lang(?object) = "en")
  }
}
ORDER BY RAND()
LIMIT 1
"""

def getWeightOf(pokemon):
    query = """
    SELECT ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject ?predicate ?object .
            FILTER (?subject = <https://pokemonkg.org/instance/pokemon/"""+pokemon+"""/weight/quantity>)
            FILTER (?predicate = <http://qudt.org/schema/qudt/quantityValue>)
        }
    }
    """

    result = dataset.query(query)
    return str(result.bindings).split("value/")[1].split("'")[0].lower()

results = dataset.query(query)
pokemon = str(results.bindings[0]).split("Literal('")[1].split("'")[0]
weight = getWeightOf(pokemon.lower())

print("The weight of the pokemon is " + weight)
print("Guess a pokemon: ")
hiddenWord = pokemon[:3]
for _ in range(len(pokemon[3:])):
    hiddenWord += "*"
print("Hint: it is " + hiddenWord)
guess = input()
print("Wrong, the correct pokemon was " + pokemon)