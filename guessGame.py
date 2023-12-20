from rdflib import Dataset
from questions import getRandomQuestion

dataset = Dataset()
try:
    dataset.parse("poke-a.nq")
except Exception as e:
    print(e)

def waitForCorrectInput():
    answer = input()
    if answer not in ["y", "n"]:
        print("Sorry, answer only 'y' or 'n'.")
        waitForCorrectInput()
    else:
        return answer

print("Think of a pokemon")

for i in range(1, 10):
    question = getRandomQuestion()
    print(str(i) + ". " + question)
    waitForCorrectInput()
        
print("Is the pokemon you are thinking of Pikachu?")