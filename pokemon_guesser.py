from game.game import Game
from sparql.sparql_api import sparql_api


def main():
    sparql_api.get_pokemon_info('mew')
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
