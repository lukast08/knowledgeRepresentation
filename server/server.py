from flask import Flask, render_template
from game.game import game_api

app = Flask(__name__)


@app.route('/')
def home():
    pokemon = game_api.draw_pokemon()

    return render_template('home.html', title="Guess the pokemon!", pokemon=pokemon)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
