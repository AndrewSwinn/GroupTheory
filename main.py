#
# 1. Created cube
# 2. Animated a simple continuous rotation
# 3. Introduced control to stop rotation
# 4. Improved coding by introducing dictionaries to reduce code repetition
# 5. Added Queue to allow for multiple transforms to be executed
# 6. Added simple loop to mix up cube
# 7. Add X, Y, Z transforms to rotate whole cube
# 8. Hard coded i=Sin and Cos values to speed up calculations.
#

from src.Cube import *
from src.SimpleSolve import *
from src.ThistleSolve import *
from src.ThistleCube import ThistleCube
import random


totalmoves = " "

def move_cube(moves):

    global totalmoves

    totalmoves = totalmoves + moves

    if moves != '':

        for m in moves:

            if m == 'R': c.move_queue.put({'axis': 'x', 'layer': 3, 'direction': -1})
            if m == 'r': c.move_queue.put({'axis': 'x', 'layer': 3, 'direction': 1})
            if m == 'S': c.move_queue.put({'axis': 'x', 'layer': 3, 'direction': 1});c.move_queue.put(
                {'axis': 'x', 'layer': 3, 'direction': 1})

            if m == 'L': c.move_queue.put({'axis': 'x', 'layer': 1, 'direction': 1})
            if m == 'l': c.move_queue.put({'axis': 'x', 'layer': 1, 'direction': -1})
            if m == 'M': c.move_queue.put({'axis': 'x', 'layer': 1, 'direction': -1});c.move_queue.put(
                {'axis': 'x', 'layer': 1, 'direction': -1})

            if m == 'X': c.move_queue.put({'axis': 'x', 'layer': 0, 'direction': 1})
            if m == 'x': c.move_queue.put({'axis': 'x', 'layer': 0, 'direction': -1})

            if m == 'B': c.move_queue.put({'axis': 'y', 'layer': 3, 'direction': 1})
            if m == 'b': c.move_queue.put({'axis': 'y', 'layer': 3, 'direction': -1})
            if m == 'C': c.move_queue.put({'axis': 'y', 'layer': 3, 'direction': -1}); c.move_queue.put(
                {'axis': 'y', 'layer': 3, 'direction': -1})

            if m == 'F': c.move_queue.put({'axis': 'y', 'layer': 1, 'direction': -1})
            if m == 'f': c.move_queue.put({'axis': 'y', 'layer': 1, 'direction': 1})
            if m == 'G': c.move_queue.put({'axis': 'y', 'layer': 1, 'direction': 1}); c.move_queue.put(
                {'axis': 'y', 'layer': 1, 'direction': 1})

            if m == 'Y': c.move_queue.put({'axis': 'y', 'layer': 0, 'direction': 1})
            if m == 'y': c.move_queue.put({'axis': 'y', 'layer': 0, 'direction': -1})

            if m == 'U': c.move_queue.put({'axis': 'z', 'layer': 3, 'direction': -1})
            if m == 'u': c.move_queue.put({'axis': 'z', 'layer': 3, 'direction': 1})
            if m == 'V': c.move_queue.put({'axis': 'z', 'layer': 3, 'direction': 1}); c.move_queue.put(
                {'axis': 'z', 'layer': 3, 'direction': 1})

            if m == 'D': c.move_queue.put({'axis': 'z', 'layer': 1, 'direction': 1})
            if m == 'd': c.move_queue.put({'axis': 'z', 'layer': 1, 'direction': -1})
            if m == 'E': c.move_queue.put({'axis': 'z', 'layer': 1, 'direction': -1});c.move_queue.put(
                {'axis': 'z', 'layer': 1, 'direction': -1})

            if m == 'Z': c.move_queue.put({'axis': 'z', 'layer': 0, 'direction': 1})
            if m == 'z': c.move_queue.put({'axis': 'z', 'layer': 0, 'direction': -1})


def scramble_cube():
    moves = ""
    for m in range(20):
        moves = moves + random.choice('RrLlUuDdFfBb')
    move_cube(moves)

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

def on_key(event):

    global totalmoves

    if event.key == 'R': move_cube('R')
    if event.key == 'r': move_cube('r')
    if event.key == 'L': move_cube('L')
    if event.key == 'l': move_cube('l')
    if event.key == 'B':  move_cube('B')
    if event.key == 'b':  move_cube('b')
    if event.key == 'F':  move_cube('F')
    if event.key == 'f':  move_cube('f')
    if event.key == 'U':  move_cube('U')
    if event.key == 'u':  move_cube('u')
    if event.key == 'D':  move_cube('D')
    if event.key == 'd':  move_cube('d')


    if event.key == 'S':

        d.twist(totalmoves)
        move_cube(d.solve())
        totalmoves=""

    if event.key == 'T':

        t.twist(totalmoves)
        print(t.print_cube())
        move_cube(t.solve())
        print(t.print_cube())

    if event.key == 't':

        print(t.print_cube())

    if event.key == 'Y':
       # moves = 'rRCrFSUVrCSuUrM  DCDUCd-BFRlFRLF-RGRGERVrGL-ECVEMVGVC'
        moves  = 'UUUFdldDBrfrdrLlRlrD  VRfu-LfrBVrBl'
        move_cube(moves)
        t.twist(moves)
        print(t.print_cube())

    if event.key == 'Q':  scramble_cube();

    if event.key == 'X':  plt.close()





if __name__ == "__main__":

    size = 3
    fig = plt.figure()
    c = Cube(size, fig)

    t = ThistleSolve()
    #t.BuildTables()

    d = SimpleSolve()

    #moves = d.scramble()

    #move_cube(moves)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    cid = fig.canvas.mpl_connect('key_press_event', on_key)

    ani = FuncAnimation(fig, c.control_cube, frames=range(9), interval=1,
                        init_func=c.plot_cube(), repeat=True, blit=False)

    plt.show()








#
#
#
# def scramble_cube():
#     moves = ""
#     for m in range(20):
#         moves = moves + random.choice('RrLlUuDdFfBb')
#     return moves
#
# for i in range(100):
#
#     move = scramble_cube()
#     c = ThistleCube()
#     c.move_cube(move)
#     solved = c.solve()
#
#
#     print(i, 'Scramble :', move, 'Solution :', solved, move+' '+solved)









