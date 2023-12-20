import random

types = ['rock', 'electric', 'flying', 'ground', 'ice', 'grass', 'dragon', 'normal', 'ghost', 'poison', 'steel', 'fire', 'dark', 'bug', 'fairy', 'psychic', 'water', 'fighting']
colors = ['red', 'white', 'blue', 'brown', 'gray', 'purple', 'pink', 'black', 'green', 'yellow']
shapes = ['humanoid', 'blob', 'upright', 'armor', 'quadruped', 'arms', 'legs', 'heads', 'squiggle', 'bugwings', 'wings', 'fish', 'ball', 'tentacles']
heights = ['1m', '2m', '3m', '4m', '5m']
weights = ['20kg', '30kg', '40kg', '50kg', '80kg']
moves = ['tackle', 'leer', 'growl', 'take-down', 'bite', 'agility', 'crunch', 'quick-attack', 'slash']
catchRates = ['45', '255', '190', '3', '75']

def getRandomQuestion():
    questionAttribute = random.choice(["types", "colors", "shapes", "heights", "weights", "moves", "catchRates"])
    questionBase = "Is the pokemon you are thinking of "
    questionBase2 = "Does the pokemon you are thinking of "

    if questionAttribute == "types":
        question = questionBase + "a " + random.choice(types) + " type pokemon?"
        queryFilters = {"y": ""}
    elif questionAttribute == "colors":
        return questionBase + random.choice(colors) + "?"
    elif questionAttribute == "shapes":
        return questionBase + "a " + random.choice(shapes) + " shaped pokemon?"
    elif questionAttribute == "heights":
        if random.choice([True, False]):
            return questionBase + "taller than " + random.choice(heights) + "?"
        else:
            return questionBase + "shorter than " + random.choice(heights) + "?"
    elif questionAttribute == "weights":
        if random.choice([True, False]):
            return questionBase + "heavier than " + random.choice(weights) + "?"
        else:
            return questionBase + "lighter than " + random.choice(weights) + "?"
    elif questionAttribute == "moves":
        return questionBase2 + "know the move " + random.choice(moves) + "?"
    elif questionAttribute == "catchRates":
        return questionBase2 + "have a catch rate of " + random.choice(catchRates) + "?"
    else:
        print("ERROR")

    return (question, queryFilters)