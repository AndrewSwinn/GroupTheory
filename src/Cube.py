#
# 1. Created cube
# 2. Animated a simple continuous rotation
# 3. Introduced control to stop rotation
# 4. Improved coding by introducing dictionaries to reduce code repetition
# 5. Added Queue to allow for multiple transforms to be executed
# 6. Added simple loop to mix up cube
# 7. Add X, Y, Z transforms to rotate whole cube
# 8  Hard codeed i=Sin and Cos values to speed up calculations.
# 9. Made cube a sub-class or Artist - and moved to its own file.
#
import numpy as np
import queue
import random
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from src.Matrix import *
from src.SimpleSolve import *
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

# sin (pi/20) = 0.156434465040231
# cos (pi/20) = 0.987688340595138

# Define global variables used throughout program

rotate_x = LambdaMatrix(4, 4).load([[lambda x: 1, lambda x: 0, lambda x: 0, lambda x: 0],
                                    [lambda x: 0, lambda x: 0.987688340595138, lambda x: -x * 0.156434465040231,
                                     lambda x: 0],
                                    [lambda x: 0, lambda x: x * 0.156434465040231, lambda x: 0.987688340595138,
                                     lambda x: 0],
                                    [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 1]])

rotate_y = LambdaMatrix(4, 4).load(
    [[lambda x: 0.987688340595138, lambda x: 0, lambda x: -x * 0.156434465040231, lambda x: 0],
     [lambda x: 0, lambda x: 1, lambda x: 0, lambda x: 0],
     [lambda x: x * 0.156434465040231, lambda x: 0, lambda x: 0.987688340595138, lambda x: 0],
     [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 1]])

rotate_z = LambdaMatrix(4, 4).load(
    [[lambda x: 0.987688340595138, lambda x: -x * 0.156434465040231, lambda x: 0, lambda x: 0],
     [lambda x: x * 0.156434465040231, lambda x: 0.987688340595138, lambda x: 0, lambda x: 0],
     [lambda x: 0, lambda x: 0, lambda x: 1, lambda x: 0],
     [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 1]])

transforms = {'x': rotate_x, 'y': rotate_y, 'z': rotate_z}

colours = {'red': 0, 'orange': 1, 'blue': 2, 'green': 3, 'yellow': 4, 'white': 5}


# Class to hold the initial and current position of each of cube stickers

class Sticker(Poly3DCollection):

    def __init__(self, coords, colour, id):

        self.init_coords = coords
        self.colour = colour
        self.id = id
        self.curr_coords = coords

        super().__init__(self.verticies())

        self.set_color(self.colour)
        self.set_linewidth(.5)
        self.set_edgecolor('black')

    def verticies(self):

        x, y, z = [], [], []

        for coord in self.curr_coords:
            x.append(coord.getelement(0, 0))
            y.append(coord.getelement(1, 0))
            z.append(coord.getelement(2, 0))

        return [list(zip(x, y, z))]

    def centre(self):

        x, y, z = 0, 0, 0

        # Find coordinates of the sticker centre.

        for v in self.curr_coords:
            x, y, z = x + v.getelement(0, 0) / 4, y + v.getelement(1, 0) / 4, z + v.getelement(2, 0) / 4

        return {'x': round(x, 1), 'y': round(y, 1), 'z': round(z, 1)}

    def transform(self, axis, layer, direction):

        new_coords = []

        for v in self.curr_coords:
            v = transforms[axis].setMatrix(direction).multiply(v)

            new_coords.append(v)

        self.curr_coords = new_coords

        self.set_verts(self.verticies())


class Cube(Artist):

    def __init__(self, size, fig):

        super().__init__()

        #self.ax = fig.gca(projection='3d')
        self.ax = fig.add_subplot(projection='3d')

        self.target_azim, self.target_elev = -60, 30
        self.ax.view_init(azim=self.target_azim, elev=self.target_elev)

        self.ax.set_xlim3d(size * -0.50, size * 0.50)
        self.ax.set_ylim3d(size * -0.50, size * 0.50)
        self.ax.set_zlim3d(size * -0.50, size * 0.50)
        self.ax.set_axis_off()

        self.size = size

        self.move_queue = queue.Queue()

        self.current_move = {}

        # Create the sticker model of the cube - used for the display

        self.moving = False

        self.move_step = 0

        self.Stickers = []

        s_id = 0

        # indexes i and j correspond to the coordinates of a sticker on a face

        # This code must be sortable out to remove the six sticker definitions.
        # I wasted a morning failing to sort it out.

        for i, j in product(range(size), range(size)):
            x, y, z = i - size / 2, j - size / 2, size / 2

            #             for k in range(6):
            #
            #                 self.cubie[k][i][j] = k

            self.Stickers.append(Sticker(
                [FourVector().load([[x], [y], [z], [1]]), FourVector().load([[x + 1], [y], [z], [1]]),
                 FourVector().load([[x + 1], [y + 1], [z], [1]]), FourVector().load([[x], [y + 1], [z], [1]])], 'white',
                s_id))
            self.Stickers.append(Sticker(
                [FourVector().load([[x], [y], [-z], [1]]), FourVector().load([[x + 1], [y], [-z], [1]]),
                 FourVector().load([[x + 1], [y + 1], [-z], [1]]), FourVector().load([[x], [y + 1], [-z], [1]])],
                'yellow', s_id + 1))
            self.Stickers.append(Sticker(
                [FourVector().load([[z], [x], [y], [1]]), FourVector().load([[z], [x + 1], [y], [1]]),
                 FourVector().load([[z], [x + 1], [y + 1], [1]]), FourVector().load([[z], [x], [y + 1], [1]])], 'blue',
                s_id + 2))
            self.Stickers.append(Sticker(
                [FourVector().load([[-z], [x], [y], [1]]), FourVector().load([[-z], [x + 1], [y], [1]]),
                 FourVector().load([[-z], [x + 1], [y + 1], [1]]), FourVector().load([[-z], [x], [y + 1], [1]])],
                'green', s_id + 3))
            self.Stickers.append(Sticker(
                [FourVector().load([[x], [z], [y], [1]]), FourVector().load([[x + 1], [z], [y], [1]]),
                 FourVector().load([[x + 1], [z], [y + 1], [1]]), FourVector().load([[x], [z], [y + 1], [1]])], 'orange',
                s_id + 4))
            self.Stickers.append(Sticker(
                [FourVector().load([[x], [-z], [y], [1]]), FourVector().load([[x + 1], [-z], [y], [1]]),
                 FourVector().load([[x + 1], [-z], [y + 1], [1]]), FourVector().load([[x], [-z], [y + 1], [1]])],
                'red', s_id + 5))

            s_id = s_id + 6

    def plot_cube(self):

        for f in self.Stickers:
            self.ax.add_collection3d(f)

    def twist(self, axis, layer, direction):

        #       Check each sticker to see if it needs to be twisted, and twist those affected

        for f in self.Stickers:

            if (min(int(f.centre()[axis] + self.size / 2.0) + 1, self.size) == layer) or layer == 0:
                f.transform(axis, layer, direction)

    def control_cube(self, frame):

        # The cube is fixed in the x,y,z coordinate frame.
        # To see the cube from different perspectives we change the viewing angle not the cube.

        delta_azim, delta_elev = self.ax.azim - self.target_azim, self.ax.elev - self.target_elev

        if abs(delta_azim) > 0: self.ax.azim -= int(delta_azim>0) - int(delta_azim<0)
        if abs(delta_elev) > 0: self.ax.elev -= int(delta_elev>0) - int(delta_elev<0)

        # Not moving and no moves pending
        if self.moving == False and self.move_queue.empty():

            self.moving = False
            self.move_step = 0
            s = []

        # Not moving and a move waits in the queue
        elif self.moving == False and self.move_queue.empty() == False:

            self.current_move = self.move_queue.get()
            self.moving = True
            self.move_step = 0
            s = []

            # Moving, and the move is incomplete

        elif self.moving == True and self.move_step < 10:

            s = self.twist(self.current_move['axis'], self.current_move['layer'], self.current_move['direction'])

            self.move_step = self.move_step + 1

            # Moving and move complete

        else:

            self.moving = False
            self.move_step = 0
            self.current_move = {}

            s = []

        return s

    def cubie_array(self):

        # At the end of each move update the cubie_array to reflect the new configuration.

        c = SimpleSolve()

        for s in self.Stickers:

            x, y, z = s.centre()['x'] + self.size / 2, s.centre()['y'] + self.size / 2, s.centre()['z'] + self.size / 2

            if z == 3.0:
                face, fx, fy, a = 0, x, y, 'a'

            elif z == 0.0:
                face, fx, fy, a = 1, x, y, 'b'

            elif x == 3.0:
                face, fx, fy, a = 2, y, z, 'c'

            elif x == 0.0:
                face, fx, fy, a = 3, y, z, 'd'

            elif y == 3.0:
                face, fx, fy, a = 5, x, z, 'e'

            elif y == 0.0:
                face, fx, fy, a = 4, x, z, 'f'

            # print(face, int(fx), int(fy), s.id, s.colour)

            c[face, int(fx), int(fy)] = {'col': colours[s.colour], 'id': s.id}

        return c


