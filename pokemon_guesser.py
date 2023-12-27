from game.game import Game
from sparql.sparql_api import sparql_api


def main():
    sparql_api.get_pokemon_info('onix')
    print("Think of a Pokemon...")
    print("Answer the questions with 'y' for yes or 'n' for no.")
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
