from copy import deepcopy
import random

from game.question import generate_all_questions
from sparql.sparql_api import sparql_api

POSSIBLE_ANSWERS = ["y", "n"]


def wait_for_correct_input(message):
    answer = input(message)
    if answer not in POSSIBLE_ANSWERS:
        print("Sorry, answer only 'y' or 'n'.")
        wait_for_correct_input(message)
    else:
        return answer


# TODO: This will be done on server initialization (in production very rarely)
print("Preparing........")
all_pokemons = sparql_api.get_all_pokemons()
all_questions = generate_all_questions(len(all_pokemons))


class Game:
    def __init__(self) -> None:
        self.questions = deepcopy(all_questions)
        self.relevant_pokemons = set(pokemon.lower() for pokemon in all_pokemons)
        self.selected_predicates = set()
        self.game_ended = False

    def restart_game(self):
        self.__init__()

    @staticmethod
    def draw_pokemon():
        pokemons = sparql_api.list_pokemons()
        return random.choice(pokemons).lower()

    # Update relevant pokemons and exclude questions based on predicates
    def update_vid_yes_answer(self, target):
        self.relevant_pokemons &= target.matched_pokemons  # Intersection
        # TODO can we implement this without the search?
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
                ques.matched_pokemons &= self.relevant_pokemons  # reduce matched pokemons
                ques.count_yes = len(ques.matched_pokemons)
                ques.count_no = len(self.relevant_pokemons) - ques.count_yes
                ques.rank = ques.count_no - ques.count_yes
        # remove all excluded questions
        self.questions = {key: item for key, item in self.questions.items()
                          if not item.excluded and not item.count_yes == 0 and not item.count_no == 0}

    # Lowest rank indicate best question
    def select_random_best_question(self):
        if not self.questions:
            return None
        # Lower is better
        lowest_rank = min(question.rank for question in self.questions.values())
        lowest_rank_keys = [key for key, question in self.questions.items() if question.rank == lowest_rank]
        return random.choice(lowest_rank_keys) if lowest_rank_keys else None

    def check_winner(self):
        if len(self.relevant_pokemons) == 1:
            print(f'You are thinking of this Pokemon: [{self.relevant_pokemons.pop()}]')
        elif self.game_ended:
            print('Game over! The possible Pokemons were: ' + ', '.join(self.relevant_pokemons))

    def start(self):
        while True:
            print("Think of a Pokemon...")
            print("Answer the questions with 'y' for yes or 'n' for no.")
            max_iter = 16  # TODO why 16?
            for counter in range(1, max_iter):
                question = self.select_random_best_question()
                if question:
                    question_detail = self.questions[question]
                    user_answer = wait_for_correct_input(
                        f'{counter}.{question} [Y/N]: ({question_detail.count_yes},{question_detail.count_no}) :')
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

            play_again = wait_for_correct_input("\n\nDo you want to play again? (y/n): ")
            if play_again != 'y':
                print("Thank you for playing! Goodbye.")
                break

            self.restart_game()
