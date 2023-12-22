from rdflib import Dataset

dataset = Dataset()
try:
    dataset.parse("poke-a.nq")
except Exception as e:
    print(e)

def getAllPokemons():
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

    results = dataset.query(query)
    pokemons = []
    for result in results:
        pokemon = str(result).split("Literal('")[1].split("'")[0]
        pokemons.append(pokemon)

    return pokemons

def split_row(row, seperator):
    return str(row[0]).split(seperator)[-1]

def getAllTypes():
    query = """
    SELECT DISTINCT ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#hasType> ?object .
        }
    }
    """

    results = dataset.query(query)
    types = []
    for row in results:
        type_part = str(row[0]).split('#PokéType:')[-1]
        types.append(type_part)

    return types

def getAllColors():
    query = """
    SELECT DISTINCT ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#hasColour> ?object .
        }
    }
    """
    results = dataset.query(query)
    colors = []
    for row in results:
        colors.append(split_row(row, '/resource/'))
    return colors

def getAllHiddenAbilites():
    query = """
    SELECT Distinct ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#mayHaveHiddenAbility> ?object .
        }
    }
    """
    results = dataset.query(query)
    hiddenAbilities = []
    for row in results:
        hiddenAbilities.append(split_row(row, '/ability/'))

    return hiddenAbilities

def getAllPossibleAbilites():
    query = """
    SELECT Distinct ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#mayHaveAbility> ?object .
        }
    }
    """
    results = dataset.query(query)
    possibleAbilities = []
    for row in results:
        possibleAbilities.append(split_row(row, '/ability/'))

    return possibleAbilities

def getAllShapes():
    query = """
    SELECT Distinct ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#hasShape> ?object .
        }
    }
    """
    result = dataset.query(query)
    shapes = []
    for row in result:
        shapes.append(split_row(row, 'Shape:'))
    return shapes

def getAllHeights():
    query = """
    SELECT ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <http://qudt.org/schema/qudt/quantityValue> ?object .
        }
    }
    """

    result = dataset.query(query)
    heights = []
    for row in result:
        height = split_row(row, '/height/quantity/value/')
        if height.endswith('M'):
            heights.append(height)
    return heights

def getAllWeights():
    query = """
    SELECT ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <http://qudt.org/schema/qudt/quantityValue> ?object .
        }
    }
    """

    result = dataset.query(query)
    heights = []
    for row in result:
        height = split_row(row, '/weight/quantity/value/')
        if height.endswith('G'):
            heights.append(height)
    return heights

def getAllMoves():
    query = """
    SELECT Distinct ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#isAbleToApply> ?object .
        }
    }
    """

    results = dataset.query(query)
    moves = []
    for row in results:
        moves.append(split_row(row, 'move/'))

    return moves

def getAllCatchRates():
    query = """
    SELECT Distinct ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {
            ?subject <https://pokemonkg.org/ontology#hasCatchRate> ?object .
        }
    }
    """

    result = dataset.query(query)
    catche_rates = []
    for row in result:
        catche_rates.append(split_row(row, 'Literal'))
    return catche_rates

class GameEngine:

    questionObjects = []
    totalPokemons = len(getAllPokemons())
    previousYesAnswersFilters = "" # when a question is answered yes, this string gets appended. It is used in the get_pokemon() query
    previousNoAnswersQueriesForExclusion = "" # when a question is answered no, this string gets appended. It is used in the get_excluded_pokemon() query
    excludedPokemons = [] # when a question is answered no, this property is set to the result of function get_excluded_pokemon()

    types = getAllTypes()
    colors = getAllColors()
    possibleAbilities = getAllPossibleAbilites()
    hiddenAbilities = getAllHiddenAbilites()
    shapes = getAllShapes()
    moves = getAllMoves()
    catchRates = getAllCatchRates()

    def get_excluded_pokemons(self):
        query = f"""
        SELECT DISTINCT ?subject
        WHERE {{
            {self.previousNoAnswersQueriesForExclusion}
        }}
        """
        results = dataset.query(query)
        return results

    def get_pokemons(self, targetPredicate, targetObject, graph):
        query = f"""
        SELECT DISTINCT ?subject
        WHERE {{
            GRAPH {graph} {{
                ?subject {targetPredicate} {targetObject} .
            }}
            {self.previousYesAnswersFilters}
        }}
        """
        results = dataset.query(query)
        return results

    def create_questions(self, question, objects, predicate, objectURI, graph):
        for item in objects:
            pokemons = self.get_pokemons(predicate, f'<{objectURI}{item}>', graph)
            relevant_pokemons = []
            for pokemon in pokemons:
                if i not in gameEngine.excludedPokemons:
                    relevant_pokemons.append(pokemon)
            count = len(relevant_pokemons)
            questionObject = QuestionObject(f'{question} {item}', [count, self.totalPokemons - count], graph, predicate, f'<{objectURI}{item}>', str(item))
            self.questionObjects.append(questionObject)

    def getQuestion(self):
        self.questionObjects = []

        self.create_questions('Is the pokemon of type', self.types, '<https://pokemonkg.org/ontology#hasType>', 'https://pokemonkg.org/ontology#PokéType:', "<https://pokemonkg.org/dataset/bulbapedia>")
        self.create_questions('Is the pokemon', self.colors, '<https://pokemonkg.org/ontology#hasColour>', 'http://dbpedia.org/resource/', "<https://pokemonkg.org/dataset/bulbapedia>")
        self.create_questions('Does the pokemon have the possible ability', self.possibleAbilities, '<https://pokemonkg.org/ontology#mayHaveAbility>', 'https://pokemonkg.org/instance/ability/', "<https://pokemonkg.org/dataset/bulbapedia>")
        self.create_questions('Does the pokemon have the hidden ability', self.hiddenAbilities, '<https://pokemonkg.org/ontology#mayHaveHiddenAbility>', 'https://pokemonkg.org/instance/ability/', "<https://pokemonkg.org/dataset/bulbapedia>")
        self.create_questions('Is the shape of the pokemon', self.shapes, '<https://pokemonkg.org/ontology#hasShape>', 'https://pokemonkg.org/ontology#Shape:', "<https://pokemonkg.org/dataset/bulbapedia>")
        self.create_questions('Does the pokemon know the move', self.moves, '<https://pokemonkg.org/ontology#isAbleToApply>', 'https://pokemonkg.org/instance/move/', "<https://pokemonkg.org/dataset/bulbapedia>")
        #self.create_questions('Does the pokemon have a catch rate of', self.catchRates, 'hasCatchRate', '^^<http://www.w3.org/2001/XMLSchema#integer>', True)

        bestValue = 1000
        for questionObject in self.questionObjects:
            if max(questionObject.yesNoArray) < bestValue:
                bestValue = max(questionObject.yesNoArray)
                bestQuestionObject = questionObject

        return bestQuestionObject



def waitForCorrectInput():
    answer = input()
    if answer not in ["y", "n"]:
        print("Sorry, answer only 'y' or 'n'.")
        waitForCorrectInput()
    else:
        return answer

print("Think of a pokemon...")
print("Answer the questions with 'y' or 'no'")

class QuestionObject:
    
    def __init__(self, question, yesNoArray, graph, predicate, objectTriple, item):
        self.question = question
        self.yesNoArray = yesNoArray
        self.graph = graph
        self.predicate = predicate
        self.objectTriple = objectTriple
        self.item = item

gameEngine = GameEngine()

for i in range(1, 15):
    if gameEngine.totalPokemons == 1:
        pokemons = gameEngine.get_pokemons("?predicate", "?object", "<https://pokemonkg.org/dataset/bulbapedia>")
        
        relevant_pokemons = []
        for pokemon in pokemons:
            if i not in gameEngine.excludedPokemons:
                relevant_pokemons.append(pokemon)
                
        if len(relevant_pokemons) == 1:
            print("Are you thinking of " + str(pokemon))
            answer = waitForCorrectInput()
            if answer == "y":
                print("Wohoo, I guessed right! Thank you for playing!")
            else:
                print("Oh! I must have done something wrong. You win! Congrats!")
        else:
            print("Error, more than one pokemon left when there should only be 1.")
        break

    questionObject = gameEngine.getQuestion()
    print(str(i) + ". " + questionObject.question + "? ("+str(questionObject.yesNoArray)+")")
    answer = waitForCorrectInput()
    
    if answer == "y":
        gameEngine.totalPokemons = questionObject.yesNoArray[0]
        gameEngine.previousYesAnswersFilters += f"GRAPH {questionObject.graph} {{ ?subject {questionObject.predicate} {questionObject.objectTriple} .}}\n"
    else:
        gameEngine.totalPokemons = questionObject.yesNoArray[1]
        gameEngine.previousNoAnswersQueriesForExclusion += f"GRAPH {questionObject.graph} {{ ?subject {questionObject.predicate} {questionObject.objectTriple} .}}\n"
        gameEngine.excludedPokemons = gameEngine.get_excluded_pokemons()

    if questionObject.predicate == '<https://pokemonkg.org/ontology#hasType>':
        if answer == "y":
            pass
        else:
            gameEngine.types.remove(questionObject.item)
    elif questionObject.predicate == '<https://pokemonkg.org/ontology#hasColour>':
        if answer == "y":
            gameEngine.colors = [questionObject.item]
        else:
            gameEngine.colors.remove(questionObject.item)
    elif questionObject.predicate == '<https://pokemonkg.org/ontology#mayHaveAbility>':
        if answer == "y":
            pass
        else:
            gameEngine.possibleAbilities.remove(questionObject.item)
    elif questionObject.predicate == '<https://pokemonkg.org/ontology#mayHaveHiddenAbility>':
        if answer == "y":
            pass
        else:
            gameEngine.hiddenAbilities.remove(questionObject.item)
    elif questionObject.predicate == '<https://pokemonkg.org/ontology#hasShape>':
        if answer == "y":
            gameEngine.shapes = [questionObject.item]
        else:
            gameEngine.shapes.remove(questionObject.item)
    elif questionObject.predicate == '<https://pokemonkg.org/ontology#isAbleToApply>':
        if answer == "y":
            pass
        else:
            gameEngine.moves.remove(questionObject.item)
    elif questionObject.predicate == 'hasCatchRate':
        if answer == "y":
            gameEngine.catchRates = [questionObject.item]
        else:
            gameEngine.catchRates.remove(questionObject.item)

if gameEngine.totalPokemons > 1:     
    print("You win, I couldn't figure out the pokemon you were thinking of. Congrats!")