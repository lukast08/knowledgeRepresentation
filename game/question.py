from game.triple import Triple
from sparql.sparql_api import sparql_api


class Question:
    def __init__(self, count_yes, count_no, rank, triple: Triple, matched_pokemons, excluded=False):
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


def create_initial_questions(questions, total_pokemons, question_template, object_values, initial_triple, graph):
    for item in object_values:
        full_object_uri = f'"{item}"{initial_triple.object_uri}' if initial_triple.literal else f'{initial_triple.object_uri}{item}'
        tempTriple = Triple(initial_triple.predicate_uri, full_object_uri, initial_triple.literal)
        temp_pokemons = sparql_api.get_pokemons_matching_condition(create_condition([tempTriple]), graph)
        count_yes = len(temp_pokemons)
        count_no = abs(total_pokemons - count_yes)
        rank = abs(count_no - count_yes)
        question_details = Question(count_yes, count_no, rank, tempTriple, temp_pokemons)
        questions[f'{question_template}{item}'] = question_details


def create_initial_questions_for_height_weight(questions, total_pokemons, question_template, object_values, attribute):
    for item in object_values:
        temp_pokemons = sparql_api.get_pokemons_by_height_or_weight(item, attribute)
        tempTriple = Triple(attribute, attribute)
        count_yes = len(temp_pokemons)
        count_no = abs(total_pokemons - count_yes)
        rank = abs(count_no - count_yes)
        question_details = Question(count_yes, count_no, rank, tempTriple, temp_pokemons)
        questions[f'{question_template}{item}'] = question_details


def generate_all_questions(total_pokemons):
    questions = dict()
    graph1 = '<https://pokemonkg.org/dataset/bulbapedia>'
    graph2 = '<http://pokemon.outofbits.com/dataset/pokeapi-co>'  # habitat,genus

    create_initial_questions(questions, total_pokemons,
                             'Is pokemon of type: ',
                             sparql_api.get_all_types(), Triple('https://pokemonkg.org/ontology#hasType',
                                                   'https://pokemonkg.org/ontology#PokéType:'), graph1)

    create_initial_questions(questions, total_pokemons,
                             'Is pokemon: ',
                             sparql_api.get_all_colors(),
                             Triple('https://pokemonkg.org/ontology#hasColour', 'http://dbpedia.org/resource/'), graph1)

    create_initial_questions(questions, total_pokemons,
                             'Has pokemon hidden ability: ',
                             sparql_api.get_all_hidden_abilites(),
                             Triple('https://pokemonkg.org/ontology#mayHaveHiddenAbility',
                                    'https://pokemonkg.org/instance/ability/'), graph1)

    create_initial_questions(questions, total_pokemons,
                             'Has pokemon possible ability: ',
                             sparql_api.get_all_possible_abilites(),
                             Triple('https://pokemonkg.org/ontology#mayHaveAbility',
                                    'https://pokemonkg.org/instance/ability/'), graph1)

    create_initial_questions(questions, total_pokemons,
                             'Is the shape of pokemon: ',
                             sparql_api.get_all_shapes(),
                             Triple('https://pokemonkg.org/ontology#hasShape', 'https://pokemonkg.org/ontology#Shape:'),
                             graph1)

    create_initial_questions(questions, total_pokemons,
                             'Has pokemon catch rate: ',
                             sparql_api.get_all_catch_rate(),
                             Triple('https://pokemonkg.org/ontology#hasCatchRate',
                                    '^^<http://www.w3.org/2001/XMLSchema#integer>', True), graph1)

    create_initial_questions(questions, total_pokemons,
                             'Is pokemon found in: ',
                             sparql_api.get_all_habitats(),
                             Triple('https://pokemonkg.org/ontology#foundIn',
                                    'https://pokemonkg.org/ontology#Habitat:'), graph2)

    create_initial_questions(questions, total_pokemons,
                             'Dose pokemon have genus: ',
                             sparql_api.get_all_genus(),
                             Triple('https://pokemonkg.org/ontology#hasGenus', '@en', True), graph2)

    create_initial_questions(questions, total_pokemons,
                             'Has pokemon this move: ',
                             sparql_api.get_all_moves(),
                             Triple('https://pokemonkg.org/ontology#isAbleToApply',
                                    'https://pokemonkg.org/instance/move/'), graph1)

    create_initial_questions_for_height_weight(questions, total_pokemons, 'Has pokemon this Weight: ', sparql_api.get_all_weights(),
                                               'weight')
    create_initial_questions_for_height_weight(questions, total_pokemons, 'Has pokemon this Height: ', sparql_api.get_all_heights(),
                                               'height')

    return questions
