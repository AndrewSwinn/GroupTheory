from src.ThistleCube import ThistleCube

c = ThistleCube()
move = 'RfLbDRdrluVrdfr'
c.move_cube(move)

print(c.cube)
solved = c.solve()
print('Solution: ', solved)




