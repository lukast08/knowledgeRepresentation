import threading
from typing import Callable
import random

from sparql.sparql_api import sparql_api


class Game:
    def draw_pokemon(self):
        pokemons = sparql_api.list_pokemons()
        return random.choice(pokemons).lower()

    def question_function(self):
        print(self.draw_pokemon())
        return 100, 200

    @staticmethod
    def pick_question(question_functions: list[Callable]) -> Callable:
        smallest_max = 10_000
        index = 0
        for i, function in enumerate(question_functions):
            result = function()
            if max(result) > smallest_max:
                smallest_max = max(result)
                index = i

        return question_functions[index]

    def question_function_thread(self, result: list[any], index: int):
        self.draw_pokemon()
        result[index] = (index, (random.randint(100, 500), random.randint(100, 500)))

    @staticmethod
    def pick_question_parallel(question_functions: list[Callable]) -> Callable:
        threads = []
        results = [any] * len(question_functions)
        for i, function in enumerate(question_functions):
            thread = threading.Thread(target=function, args=(results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        smallest_max = 10_000
        index = 0
        for res in results:
            if max(res[1]) < smallest_max:
                smallest_max = max(res[1])
                index = res[0]

        return question_functions[index]


game_api = Game()
game_api.pick_question([game_api.question_function, game_api.question_function, game_api.question_function,
                        game_api.question_function, game_api.question_function])()

# game_api.pick_question_parallel([game_api.question_function])()
