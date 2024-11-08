import random
import datetime
from src.ThistleCube import ThistleCube

identity = ThistleCube()
moves = [move for move in identity.moves_dict.keys()]

for i in range(10):
    scramble = ''
    for i in range(40):
        scramble+=random.choice(moves)
    c = ThistleCube()
    c.move_cube(scramble)
    current= datetime.datetime.now()
    optimal, nodes = c.optimal()
    elapsed = datetime.datetime.now() - current
    print(scramble, optimal, nodes, elapsed)