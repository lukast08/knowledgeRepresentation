from game.game import Game
from sparql.sparql_api import sparql_api


def main():
    sparql_api.get_pokemon_info('onix')
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
