from rdflib import Dataset
import random
import copy

dataset = Dataset()
try:
    dataset.parse("poke-a.nq")
except Exception as e:
    print(e)

def split_row(row, seperator):
    return str(row[0]).split(seperator)[-1]


def getTypeOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasType> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    types = [split_row(row, 'Type:') for row in results]

    return types


def getColorOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasColour> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'resource/') for row in results]
    if not items:
        return ''
    return items if len(items) > 1 else items[0]


def getHabitatOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#foundIn> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'Habitat:') for row in results]
    if not items:
        return ''
    return items if len(items) > 1 else items[0]


def getMovesOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#isAbleToApply> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'move/') for row in results]
    return items


def getShapeOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasShape> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'Shape:') for row in results]
    if not items:
        return ''
    return items if len(items) > 1 else items[0]


def getPossibleAbilitesOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#mayHaveAbility> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'ability/') for row in results]

    return items


def getHiddenAbilitesOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#mayHaveHiddenAbility> ?object .
        }}
    }}
    """
    results = dataset.query(query)
    items = [split_row(row, 'ability/') for row in results]
    return items


def getCatchRateOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasCatchRate> ?object .
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'Literal') for row in results]
    return items if len(items) > 1 else items[0]


def getHeightOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            ?object <http://qudt.org/schema/qudt/value> ?value .
            FILTER(CONTAINS(STR(?object), 'https://pokemonkg.org/instance/pokemon/{pokemon}/height'))
        }}
    }}
    """

    result = dataset.query(query)
    for row in result:
        return split_row(row, '/height/quantity/value/')
    return None


def getWeightOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            ?object <http://qudt.org/schema/qudt/value> ?value .
            FILTER(CONTAINS(STR(?object), 'https://pokemonkg.org/instance/pokemon/{pokemon}/weight'))
        }}
    }}
    """

    result = dataset.query(query)
    for row in result:
        return split_row(row, '/weight/quantity/value/')
    return None


def getGenusOf(pokemon):
    query = f"""
    SELECT ?object
    WHERE {{
        GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {{
            <https://pokemonkg.org/instance/pokemon/{pokemon}> <https://pokemonkg.org/ontology#hasGenus> ?object .
            FILTER (lang(?object) = "" || lang(?object) = "en")
        }}
    }}
    """

    results = dataset.query(query)
    items = [split_row(row, 'Shape:') for row in results]
    if not items:
        return ''
    return items if len(items) > 1 else items[0]


def getAllPokemons():
    query = """
    SELECT ?object
    WHERE {
        GRAPH <https://pokemonkg.org/dataset/pokewiki-de-pokemonlist> {
            ?subject <http://www.w3.org/2000/01/rdf-schema#label> ?object .
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


def getAllGenus():
    query = """
    SELECT ?object
    WHERE {
        GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {
            ?subject <https://pokemonkg.org/ontology#hasGenus> ?object .
            FILTER (lang(?object) = "" || lang(?object) = "en")
        }
    }
    """

    results = dataset.query(query)
    items = []
    for row in results:
        items.append(split_row(row, 'Literal'))

    return items


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
    return list(set(heights))


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
    weights = []
    for row in result:
        height = split_row(row, '/weight/quantity/value/')
        if height.endswith('G'):
            weights.append(height)
    return list(set(weights))


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


def getAllHabitats():
    query = """
    SELECT Distinct ?object
    WHERE {
        GRAPH <http://pokemon.outofbits.com/dataset/pokeapi-co> {
            ?subject <https://pokemonkg.org/ontology#foundIn> ?object .
        }
    }
    """

    results = dataset.query(query)
    habitat = []
    for row in results:
        habitat.append(split_row(row, 'Habitat:'))

    return habitat


def getAllCatchRate():
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


class Triple:
    def __init__(self, predicate_uri, object_uri, literal = False) -> None:
        self.predicate_uri = predicate_uri
        self.object_uri = object_uri
        self.literal = literal


class Question:
    def __init__(self, count_yes, count_no, rank, triple:Triple, matched_pokemons , excluded=False):
        self.count_yes = count_yes
        self.count_no = count_no
        self.rank = rank
        self.triple = Triple(triple.predicate_uri, triple.object_uri, triple.literal)
        self.matched_pokemons = set(matched_pokemons)
        self.excluded = excluded


def create_condition(targets: []):
    if not targets:
        return None
    else:
        conditions = []
        for triple in targets:
            obj = f'<{triple.object_uri}>' if not triple.literal else triple.object_uri
            conditions.append(f'?subject <{triple.predicate_uri}> {obj} .\n')
        concatenated_conditions = "".join(conditions)
        return concatenated_conditions


def get_pokemons_by_height_or_weight(value, attribute):
    query = f"""
    SELECT ?subject
    WHERE {{
        GRAPH <https://pokemonkg.org/dataset/bulbapedia> {{
            ?subject <http://qudt.org/schema/qudt/value> ?object .
        }}
    }}
    """
    results = dataset.query(query)
    pokemons = []
    sep = ''
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


def get_pokemons(include_in_query, graph):
    query_condition = create_condition(include_in_query)
    query = f"""
    SELECT ?subject
    WHERE {{
        GRAPH {graph} {{
            {query_condition}
        }}
    }}
    """
    results = dataset.query(query)
    pokemons = []
    for row in results:
        pokemons.append(split_row(row, '/pokemon/'))
    return pokemons


def create_initial_questions(questions, total_pokemons ,question_template, object_values, initial_triple, graph):
    for item in object_values:
        full_object_uri = f'"{item}"{initial_triple.object_uri}' if initial_triple.literal else f'{initial_triple.object_uri}{item}'
        tempTriple = Triple(initial_triple.predicate_uri, full_object_uri, initial_triple.literal)
        temp_pokemons = get_pokemons([tempTriple],graph)
        count_yes = len(temp_pokemons)
        count_no = abs(total_pokemons - count_yes)
        rank = abs(count_no - count_yes)
        question_details = Question(count_yes, count_no, rank, tempTriple, temp_pokemons)
        questions[f'{question_template}{item}'] = question_details


def create_initial_questions_for_height_weight(questions, total_pokemons ,question_template, object_values, attribute):
    for item in object_values:
        temp_pokemons = get_pokemons_by_height_or_weight(item, attribute)
        tempTriple = Triple(attribute, attribute)
        count_yes = len(temp_pokemons)
        count_no = abs(total_pokemons - count_yes)
        rank = abs(count_no - count_yes)
        question_details = Question(count_yes, count_no, rank, tempTriple, temp_pokemons)
        questions[f'{question_template}{item}'] = question_details


def generate_all_questions(total_pokemons):
    questions = dict()
    graph1 = '<https://pokemonkg.org/dataset/bulbapedia>'
    graph2 = '<http://pokemon.outofbits.com/dataset/pokeapi-co>' #habitat,genus

    create_initial_questions(questions, total_pokemons,
        'Is pokemon of type: ', 
        getAllTypes(), Triple('https://pokemonkg.org/ontology#hasType', 'https://pokemonkg.org/ontology#PokéType:'),graph1)

    create_initial_questions(questions, total_pokemons,
        'Is pokemon: ', 
        getAllColors(), 
        Triple('https://pokemonkg.org/ontology#hasColour', 'http://dbpedia.org/resource/'),graph1)

    create_initial_questions(questions, total_pokemons,
        'Has pokemon hidden ability: ', 
        getAllHiddenAbilites(), 
        Triple('https://pokemonkg.org/ontology#mayHaveHiddenAbility', 'https://pokemonkg.org/instance/ability/'),graph1)

    create_initial_questions(questions, total_pokemons,
        'Has pokemon possible ability: ', 
        getAllPossibleAbilites(), 
        Triple('https://pokemonkg.org/ontology#mayHaveAbility', 'https://pokemonkg.org/instance/ability/'),graph1)
    
    create_initial_questions(questions, total_pokemons,
        'Is the shape of pokemon: ', 
        getAllShapes(), 
        Triple('https://pokemonkg.org/ontology#hasShape', 'https://pokemonkg.org/ontology#Shape:'),graph1)
    
    create_initial_questions(questions, total_pokemons,
        'Has pokemon catch rate: ', 
        getAllCatchRate(), 
        Triple('https://pokemonkg.org/ontology#hasCatchRate', '^^<http://www.w3.org/2001/XMLSchema#integer>', True),graph1)
    
    create_initial_questions(questions, total_pokemons,
        'Is pokemon found in: ', 
        getAllHabitats(), 
        Triple('https://pokemonkg.org/ontology#foundIn', 'https://pokemonkg.org/ontology#Habitat:'),graph2)

    create_initial_questions(questions, total_pokemons,
        'Dose pokemon have genus: ', 
        getAllGenus(), 
        Triple('https://pokemonkg.org/ontology#hasGenus', '@en',True),graph2)
    
    create_initial_questions(questions, total_pokemons,
        'Has pokemon this move: ', 
        getAllMoves(), 
        Triple('https://pokemonkg.org/ontology#isAbleToApply', 'https://pokemonkg.org/instance/move/'), graph1)
    
    create_initial_questions_for_height_weight(questions, total_pokemons,'Has pokemon this Weight: ',getAllWeights(),'weight')
    create_initial_questions_for_height_weight(questions, total_pokemons,'Has pokemon this Height: ',getAllHeights(),'height')

    return questions

def waitForCorrectInput(message):
    answer = input(message)
    if answer not in ["y", "n"]:
        print("Sorry, answer only 'y' or 'n'.")
        waitForCorrectInput(message)
    else:
        return answer

class Game:
    def __init__(self, all_pokemons, questions) -> None:
        self.questions = dict(questions)
        self.relevant_pokemons = set(pokemon.lower() for pokemon in all_pokemons)
        self.selected_predicates = set()
        self.game_ended = False
        
    # Update relevant pokemons and exclude questions based on predicates
    def update_vid_yes_answer(self, target):
        self.relevant_pokemons &= target.matched_pokemons # Intersection
        for ques in self.questions.values():
            if ques.triple.predicate_uri == target.triple.predicate_uri:
                ques.excluded = True

    # Update relevant pokemons and exclude one question
    def update_vid_no_answer(self, target):
        target.excluded = True
        self.relevant_pokemons -= target.matched_pokemons

    # update yes/no count and rank 
    def update_questions(self):
        for ques in self.questions.values():
            if not ques.excluded:
                ques.matched_pokemons &= self.relevant_pokemons #reduce matched pokemons
                ques.count_yes = len(ques.matched_pokemons)
                ques.count_no = len(self.relevant_pokemons) - ques.count_yes
                ques.rank = ques.count_no - ques.count_yes
        # remove all excluded questions
        self.questions = {key: item for key, item in self.questions.items() 
                          if not item.excluded and not item.count_yes==0 and not item.count_no==0}

    # Lowest rank indicate best question
    def select_random_best_question(self):
        if not self.questions:
            return None
       # Lower is better
        lowest_rank = min(question.rank for question in self.questions.values())
        lowest_rank_keys = [key for key, question in self.questions.items() if question.rank == lowest_rank]
        return random.choice(lowest_rank_keys) if lowest_rank_keys else None
    
    ## pick best question of each grouped by predicate questiosns, and cyckle around when all picked
    # def select_random_best_question(self):
    #         if not self.questions:
    #             return None
    #         # Filter questions that have not been selected yet
    #         unselected_questions = {key: q for key, q in self.questions.items()
    #                                 if q.triple.predicate_uri not in self.selected_predicates}

    #         if not unselected_questions:  # If all predicates have been selected, reset
    #             self.selected_predicates = set()
    #             unselected_questions = self.questions

    #         # Get best ranked quesion
    #         lowest_rank = min(question.rank for question in unselected_questions.values())
    #         lowest_rank_keys = [key for key, question in unselected_questions.items() if question.rank == lowest_rank]
    #         selected_question = random.choice(lowest_rank_keys) if lowest_rank_keys else None
    #         # Update selected predicates
    #         if selected_question:
    #             self.selected_predicates.add(self.questions[selected_question].triple.predicate_uri)

    #         return selected_question

    def check_winner(self):
        if len(self.relevant_pokemons) == 1:
            print(f'You are thinking of this Pokemon: [{self.relevant_pokemons.pop()}]')
        elif self.game_ended:
            print('Game over! The possible Pokemons were: ' + ', '.join(self.relevant_pokemons))

    def start(self):
        max_iter = 16
        for counter in range(1,max_iter):
            question = self.select_random_best_question()
            if question:
                question_detail = self.questions[question]
                user_answer = waitForCorrectInput(f'{counter}.{question} [Y/N]: ({question_detail.count_yes},{question_detail.count_no}) :' )
                if user_answer == 'y':
                    self.update_vid_yes_answer(question_detail)
                else:
                    self.update_vid_no_answer(question_detail)
                self.update_questions()
            if counter == max_iter - 1:
                self.game_ended = True
            self.check_winner()
            if len(self.relevant_pokemons) <= 1:
                break



def getPokemonInfo(pokemon):
    print(f'Pokemon name: {pokemon}')
    print("Types:")
    for type in getTypeOf(pokemon):
        print("\t" + type)
    print("\nColor: " + getColorOf(pokemon))
    print("\nShape: " + getShapeOf(pokemon))
    print("\nCatch Rate: " + getCatchRateOf(pokemon))
    print("\nWeight: " + getWeightOf(pokemon))
    print("\nHeight: " + getHeightOf(pokemon))
    print("\nHabitat: " + getHabitatOf(pokemon))
    print("\nGenus: " + getGenusOf(pokemon))
    print("\nMoves:")
    for move in getMovesOf(pokemon):
        print("\t" + move)

    print("\nPossible abilities:")
    for possibleAbilities in getPossibleAbilitesOf(pokemon):
        print("\t" + possibleAbilities)

    print("\nHidden abilities:")
    for hiddenAbilities in getHiddenAbilitesOf(pokemon):
        print("\t" + hiddenAbilities)
    print('\n\n')


print("Preparing........")
all_pokemons = getAllPokemons()
questions = generate_all_questions(len(all_pokemons))
def play_game():
    getPokemonInfo('venusaur')
    print("Think of a Pokemon...")
    print("Answer the questions with 'y' for yes or 'n' for no.")
    questions_copy = copy.deepcopy(questions)
    game = Game(list(all_pokemons), questions_copy)
    game.start()

def main():
    while True:
        play_game()
        play_again = waitForCorrectInput("\n\nDo you want to play again? (y/n): ")
        if play_again != 'y':
            print("Thank you for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()