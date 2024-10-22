'''
Created on 23 Feb 2021

@author: aswinn
'''
# Crude hard coding of array translations.
# Mappings generated automatically by tagging each sticker and checking array to see how it changes.
# A million cube rotations took 45s, and a million side rotations took 20s
#

import numpy as np
from itertools import product
import copy
import random


class SimpleSolve(np.ndarray):

    def __new__(cls):

        obj = super().__new__(cls, shape=(6, 3, 3), dtype=dict)

        return obj

    def __init__(self, *args):

        super().__init__()


        # Initialise cube with starting parameters. Each sticker has a colour and an id.
        # The ID is useful for generating the transformations reliably

        s_id = 0

        # indexes i and j correspond to the coordinates of a sticker on a face

        for i, j in product(range(3), range(3)):
            self[0][i][j] = {'col': 0, 'id': s_id + 0}
            self[1][i][j] = {'col': 1, 'id': s_id + 1}
            self[2][i][j] = {'col': 2, 'id': s_id + 2}
            self[3][i][j] = {'col': 3, 'id': s_id + 3}
            self[4][i][j] = {'col': 4, 'id': s_id + 4}
            self[5][i][j] = {'col': 5, 'id': s_id + 5}

            s_id = s_id + 6

    def R(self):

        cp = copy.copy(self)

        self[5][2][2] = cp[0][2][0];
        self[5][2][1] = cp[0][2][1];
        self[5][2][0] = cp[0][2][2];
        self[4][2][2] = cp[1][2][0];
        self[4][2][1] = cp[1][2][1];
        self[4][2][0] = cp[1][2][2];
        self[2][0][2] = cp[2][0][0];
        self[2][1][2] = cp[2][0][1];
        self[2][2][2] = cp[2][0][2];
        self[2][0][1] = cp[2][1][0];
        self[2][2][1] = cp[2][1][2];
        self[2][0][0] = cp[2][2][0];
        self[2][1][0] = cp[2][2][1];
        self[2][2][0] = cp[2][2][2];
        self[0][2][0] = cp[4][2][0];
        self[0][2][1] = cp[4][2][1];
        self[0][2][2] = cp[4][2][2];
        self[1][2][0] = cp[5][2][0];
        self[1][2][1] = cp[5][2][1];
        self[1][2][2] = cp[5][2][2]

    def r(self):

        cp = copy.copy(self)

        self[4][2][0] = cp[0][2][0];
        self[4][2][1] = cp[0][2][1];
        self[4][2][2] = cp[0][2][2];
        self[5][2][0] = cp[1][2][0];
        self[5][2][1] = cp[1][2][1];
        self[5][2][2] = cp[1][2][2];
        self[2][2][0] = cp[2][0][0];
        self[2][1][0] = cp[2][0][1];
        self[2][0][0] = cp[2][0][2];
        self[2][2][1] = cp[2][1][0];
        self[2][0][1] = cp[2][1][2];
        self[2][2][2] = cp[2][2][0];
        self[2][1][2] = cp[2][2][1];
        self[2][0][2] = cp[2][2][2];
        self[1][2][2] = cp[4][2][0];
        self[1][2][1] = cp[4][2][1];
        self[1][2][0] = cp[4][2][2];
        self[0][2][2] = cp[5][2][0];
        self[0][2][1] = cp[5][2][1];
        self[0][2][0] = cp[5][2][2]

    def L(self):

        cp = copy.copy(self)

        self[4][0][0] = cp[0][0][0];
        self[4][0][1] = cp[0][0][1];
        self[4][0][2] = cp[0][0][2];
        self[5][0][0] = cp[1][0][0];
        self[5][0][1] = cp[1][0][1];
        self[5][0][2] = cp[1][0][2];
        self[3][2][0] = cp[3][0][0];
        self[3][1][0] = cp[3][0][1];
        self[3][0][0] = cp[3][0][2];
        self[3][2][1] = cp[3][1][0];
        self[3][0][1] = cp[3][1][2];
        self[3][2][2] = cp[3][2][0];
        self[3][1][2] = cp[3][2][1];
        self[3][0][2] = cp[3][2][2];
        self[1][0][2] = cp[4][0][0];
        self[1][0][1] = cp[4][0][1];
        self[1][0][0] = cp[4][0][2];
        self[0][0][2] = cp[5][0][0];
        self[0][0][1] = cp[5][0][1];
        self[0][0][0] = cp[5][0][2];

    def l(self):

        cp = copy.copy(self)

        self[5][0][2] = cp[0][0][0];
        self[5][0][1] = cp[0][0][1];
        self[5][0][0] = cp[0][0][2];
        self[4][0][2] = cp[1][0][0];
        self[4][0][1] = cp[1][0][1];
        self[4][0][0] = cp[1][0][2];
        self[3][0][2] = cp[3][0][0];
        self[3][1][2] = cp[3][0][1];
        self[3][2][2] = cp[3][0][2];
        self[3][0][1] = cp[3][1][0];
        self[3][2][1] = cp[3][1][2];
        self[3][0][0] = cp[3][2][0];
        self[3][1][0] = cp[3][2][1];
        self[3][2][0] = cp[3][2][2];
        self[0][0][0] = cp[4][0][0];
        self[0][0][1] = cp[4][0][1];
        self[0][0][2] = cp[4][0][2];
        self[1][0][0] = cp[5][0][0];
        self[1][0][1] = cp[5][0][1];
        self[1][0][2] = cp[5][0][2];

    def U(self):

        cp = copy.copy(self)

        self[0][0][2] = cp[0][0][0];
        self[0][1][2] = cp[0][0][1];
        self[0][2][2] = cp[0][0][2];
        self[0][0][1] = cp[0][1][0];
        self[0][2][1] = cp[0][1][2];
        self[0][0][0] = cp[0][2][0];
        self[0][1][0] = cp[0][2][1];
        self[0][2][0] = cp[0][2][2];
        self[4][0][2] = cp[2][0][2];
        self[4][1][2] = cp[2][1][2];
        self[4][2][2] = cp[2][2][2];
        self[5][0][2] = cp[3][0][2];
        self[5][1][2] = cp[3][1][2];
        self[5][2][2] = cp[3][2][2];
        self[3][2][2] = cp[4][0][2];
        self[3][1][2] = cp[4][1][2];
        self[3][0][2] = cp[4][2][2];
        self[2][2][2] = cp[5][0][2];
        self[2][1][2] = cp[5][1][2];
        self[2][0][2] = cp[5][2][2];

    def u(self):

        cp = copy.copy(self)

        self[0][2][0] = cp[0][0][0];
        self[0][1][0] = cp[0][0][1];
        self[0][0][0] = cp[0][0][2];
        self[0][2][1] = cp[0][1][0];
        self[0][0][1] = cp[0][1][2];
        self[0][2][2] = cp[0][2][0];
        self[0][1][2] = cp[0][2][1];
        self[0][0][2] = cp[0][2][2];
        self[5][2][2] = cp[2][0][2];
        self[5][1][2] = cp[2][1][2];
        self[5][0][2] = cp[2][2][2];
        self[4][2][2] = cp[3][0][2];
        self[4][1][2] = cp[3][1][2];
        self[4][0][2] = cp[3][2][2];
        self[2][0][2] = cp[4][0][2];
        self[2][1][2] = cp[4][1][2];
        self[2][2][2] = cp[4][2][2];
        self[3][0][2] = cp[5][0][2];
        self[3][1][2] = cp[5][1][2];
        self[3][2][2] = cp[5][2][2];

    def d(self):

        cp = copy.copy(self)

        self[1][0][2] = cp[1][0][0];
        self[1][1][2] = cp[1][0][1];
        self[1][2][2] = cp[1][0][2];
        self[1][0][1] = cp[1][1][0];
        self[1][2][1] = cp[1][1][2];
        self[1][0][0] = cp[1][2][0];
        self[1][1][0] = cp[1][2][1];
        self[1][2][0] = cp[1][2][2];
        self[4][0][0] = cp[2][0][0];
        self[4][1][0] = cp[2][1][0];
        self[4][2][0] = cp[2][2][0];
        self[5][0][0] = cp[3][0][0];
        self[5][1][0] = cp[3][1][0];
        self[5][2][0] = cp[3][2][0];
        self[3][2][0] = cp[4][0][0];
        self[3][1][0] = cp[4][1][0];
        self[3][0][0] = cp[4][2][0];
        self[2][2][0] = cp[5][0][0];
        self[2][1][0] = cp[5][1][0];
        self[2][0][0] = cp[5][2][0];

    def D(self):

        cp = copy.copy(self)

        self[1][2][0] = cp[1][0][0];
        self[1][1][0] = cp[1][0][1];
        self[1][0][0] = cp[1][0][2];
        self[1][2][1] = cp[1][1][0];
        self[1][0][1] = cp[1][1][2];
        self[1][2][2] = cp[1][2][0];
        self[1][1][2] = cp[1][2][1];
        self[1][0][2] = cp[1][2][2];
        self[5][2][0] = cp[2][0][0];
        self[5][1][0] = cp[2][1][0];
        self[5][0][0] = cp[2][2][0];
        self[4][2][0] = cp[3][0][0];
        self[4][1][0] = cp[3][1][0];
        self[4][0][0] = cp[3][2][0];
        self[2][0][0] = cp[4][0][0];
        self[2][1][0] = cp[4][1][0];
        self[2][2][0] = cp[4][2][0];
        self[3][0][0] = cp[5][0][0];
        self[3][1][0] = cp[5][1][0];
        self[3][2][0] = cp[5][2][0];

    def F(self):

        cp = copy.copy(self)

        self[2][0][2] = cp[0][0][0];
        self[2][0][1] = cp[0][1][0];
        self[2][0][0] = cp[0][2][0];
        self[3][0][2] = cp[1][0][0];
        self[3][0][1] = cp[1][1][0];
        self[3][0][0] = cp[1][2][0];
        self[1][0][0] = cp[2][0][0];
        self[1][1][0] = cp[2][0][1];
        self[1][2][0] = cp[2][0][2];
        self[0][0][0] = cp[3][0][0];
        self[0][1][0] = cp[3][0][1];
        self[0][2][0] = cp[3][0][2];
        self[4][0][2] = cp[4][0][0];
        self[4][1][2] = cp[4][0][1];
        self[4][2][2] = cp[4][0][2];
        self[4][0][1] = cp[4][1][0];
        self[4][2][1] = cp[4][1][2];
        self[4][0][0] = cp[4][2][0];
        self[4][1][0] = cp[4][2][1];
        self[4][2][0] = cp[4][2][2];

    def f(self):

        cp = copy.copy(self)

        self[3][0][0] = cp[0][0][0];
        self[3][0][1] = cp[0][1][0];
        self[3][0][2] = cp[0][2][0];
        self[2][0][0] = cp[1][0][0];
        self[2][0][1] = cp[1][1][0];
        self[2][0][2] = cp[1][2][0];
        self[0][2][0] = cp[2][0][0];
        self[0][1][0] = cp[2][0][1];
        self[0][0][0] = cp[2][0][2];
        self[1][2][0] = cp[3][0][0];
        self[1][1][0] = cp[3][0][1];
        self[1][0][0] = cp[3][0][2];
        self[4][2][0] = cp[4][0][0];
        self[4][1][0] = cp[4][0][1];
        self[4][0][0] = cp[4][0][2];
        self[4][2][1] = cp[4][1][0];
        self[4][0][1] = cp[4][1][2];
        self[4][2][2] = cp[4][2][0];
        self[4][1][2] = cp[4][2][1];
        self[4][0][2] = cp[4][2][2];

    def B(self):

        cp = copy.copy(self)

        self[3][2][0] = cp[0][0][2];
        self[3][2][1] = cp[0][1][2];
        self[3][2][2] = cp[0][2][2];
        self[2][2][0] = cp[1][0][2];
        self[2][2][1] = cp[1][1][2];
        self[2][2][2] = cp[1][2][2];
        self[0][2][2] = cp[2][2][0];
        self[0][1][2] = cp[2][2][1];
        self[0][0][2] = cp[2][2][2];
        self[1][2][2] = cp[3][2][0];
        self[1][1][2] = cp[3][2][1];
        self[1][0][2] = cp[3][2][2];
        self[5][2][0] = cp[5][0][0];
        self[5][1][0] = cp[5][0][1];
        self[5][0][0] = cp[5][0][2];
        self[5][2][1] = cp[5][1][0];
        self[5][0][1] = cp[5][1][2];
        self[5][2][2] = cp[5][2][0];
        self[5][1][2] = cp[5][2][1];
        self[5][0][2] = cp[5][2][2];

    def b(self):

        cp = copy.copy(self)

        self[2][2][2] = cp[0][0][2];
        self[2][2][1] = cp[0][1][2];
        self[2][2][0] = cp[0][2][2];
        self[3][2][2] = cp[1][0][2];
        self[3][2][1] = cp[1][1][2];
        self[3][2][0] = cp[1][2][2];
        self[1][0][2] = cp[2][2][0];
        self[1][1][2] = cp[2][2][1];
        self[1][2][2] = cp[2][2][2];
        self[0][0][2] = cp[3][2][0];
        self[0][1][2] = cp[3][2][1];
        self[0][2][2] = cp[3][2][2];
        self[5][0][2] = cp[5][0][0];
        self[5][1][2] = cp[5][0][1];
        self[5][2][2] = cp[5][0][2];
        self[5][0][1] = cp[5][1][0];
        self[5][2][1] = cp[5][1][2];
        self[5][0][0] = cp[5][2][0];
        self[5][1][0] = cp[5][2][1];
        self[5][2][0] = cp[5][2][2];

    def X(self):

        cp = copy.copy(self)
        self[4][0][0] = cp[0][0][0];
        self[4][0][1] = cp[0][0][1];
        self[4][0][2] = cp[0][0][2];
        self[4][1][0] = cp[0][1][0];
        self[4][1][1] = cp[0][1][1];
        self[4][1][2] = cp[0][1][2];
        self[4][2][0] = cp[0][2][0];
        self[4][2][1] = cp[0][2][1];
        self[4][2][2] = cp[0][2][2];
        self[5][0][0] = cp[1][0][0];
        self[5][0][1] = cp[1][0][1];
        self[5][0][2] = cp[1][0][2];
        self[5][1][0] = cp[1][1][0];
        self[5][1][1] = cp[1][1][1];
        self[5][1][2] = cp[1][1][2];
        self[5][2][0] = cp[1][2][0];
        self[5][2][1] = cp[1][2][1];
        self[5][2][2] = cp[1][2][2];
        self[2][2][0] = cp[2][0][0];
        self[2][1][0] = cp[2][0][1];
        self[2][0][0] = cp[2][0][2];
        self[2][2][1] = cp[2][1][0];
        self[2][0][1] = cp[2][1][2];
        self[2][2][2] = cp[2][2][0];
        self[2][1][2] = cp[2][2][1];
        self[2][0][2] = cp[2][2][2];
        self[3][2][0] = cp[3][0][0];
        self[3][1][0] = cp[3][0][1];
        self[3][0][0] = cp[3][0][2];
        self[3][2][1] = cp[3][1][0];
        self[3][0][1] = cp[3][1][2];
        self[3][2][2] = cp[3][2][0];
        self[3][1][2] = cp[3][2][1];
        self[3][0][2] = cp[3][2][2];
        self[1][0][2] = cp[4][0][0];
        self[1][0][1] = cp[4][0][1];
        self[1][0][0] = cp[4][0][2];
        self[1][1][2] = cp[4][1][0];
        self[1][1][1] = cp[4][1][1];
        self[1][1][0] = cp[4][1][2];
        self[1][2][2] = cp[4][2][0];
        self[1][2][1] = cp[4][2][1];
        self[1][2][0] = cp[4][2][2];
        self[0][0][2] = cp[5][0][0];
        self[0][0][1] = cp[5][0][1];
        self[0][0][0] = cp[5][0][2];
        self[0][1][2] = cp[5][1][0];
        self[0][1][1] = cp[5][1][1];
        self[0][1][0] = cp[5][1][2];
        self[0][2][2] = cp[5][2][0];
        self[0][2][1] = cp[5][2][1];
        self[0][2][0] = cp[5][2][2];

    def x(self):

        cp = copy.copy(self)
        self[5][0][2] = cp[0][0][0];
        self[5][0][1] = cp[0][0][1];
        self[5][0][0] = cp[0][0][2];
        self[5][1][2] = cp[0][1][0];
        self[5][1][1] = cp[0][1][1];
        self[5][1][0] = cp[0][1][2];
        self[5][2][2] = cp[0][2][0];
        self[5][2][1] = cp[0][2][1];
        self[5][2][0] = cp[0][2][2];
        self[4][0][2] = cp[1][0][0];
        self[4][0][1] = cp[1][0][1];
        self[4][0][0] = cp[1][0][2];
        self[4][1][2] = cp[1][1][0];
        self[4][1][1] = cp[1][1][1];
        self[4][1][0] = cp[1][1][2];
        self[4][2][2] = cp[1][2][0];
        self[4][2][1] = cp[1][2][1];
        self[4][2][0] = cp[1][2][2];
        self[2][0][2] = cp[2][0][0];
        self[2][1][2] = cp[2][0][1];
        self[2][2][2] = cp[2][0][2];
        self[2][0][1] = cp[2][1][0];
        self[2][2][1] = cp[2][1][2];
        self[2][0][0] = cp[2][2][0];
        self[2][1][0] = cp[2][2][1];
        self[2][2][0] = cp[2][2][2];
        self[3][0][2] = cp[3][0][0];
        self[3][1][2] = cp[3][0][1];
        self[3][2][2] = cp[3][0][2];
        self[3][0][1] = cp[3][1][0];
        self[3][2][1] = cp[3][1][2];
        self[3][0][0] = cp[3][2][0];
        self[3][1][0] = cp[3][2][1];
        self[3][2][0] = cp[3][2][2];
        self[0][0][0] = cp[4][0][0];
        self[0][0][1] = cp[4][0][1];
        self[0][0][2] = cp[4][0][2];
        self[0][1][0] = cp[4][1][0];
        self[0][1][1] = cp[4][1][1];
        self[0][1][2] = cp[4][1][2];
        self[0][2][0] = cp[4][2][0];
        self[0][2][1] = cp[4][2][1];
        self[0][2][2] = cp[4][2][2];
        self[1][0][0] = cp[5][0][0];
        self[1][0][1] = cp[5][0][1];
        self[1][0][2] = cp[5][0][2];
        self[1][1][0] = cp[5][1][0];
        self[1][1][1] = cp[5][1][1];
        self[1][1][2] = cp[5][1][2];
        self[1][2][0] = cp[5][2][0];
        self[1][2][1] = cp[5][2][1];
        self[1][2][2] = cp[5][2][2];

    def Y(self):

        cp = copy.copy(self)

        self[3][0][0] = cp[0][0][0];
        self[3][1][0] = cp[0][0][1];
        self[3][2][0] = cp[0][0][2];
        self[3][0][1] = cp[0][1][0];
        self[3][1][1] = cp[0][1][1];
        self[3][2][1] = cp[0][1][2];
        self[3][0][2] = cp[0][2][0];
        self[3][1][2] = cp[0][2][1];
        self[3][2][2] = cp[0][2][2];
        self[2][0][0] = cp[1][0][0];
        self[2][1][0] = cp[1][0][1];
        self[2][2][0] = cp[1][0][2];
        self[2][0][1] = cp[1][1][0];
        self[2][1][1] = cp[1][1][1];
        self[2][2][1] = cp[1][1][2];
        self[2][0][2] = cp[1][2][0];
        self[2][1][2] = cp[1][2][1];
        self[2][2][2] = cp[1][2][2];
        self[0][2][0] = cp[2][0][0];
        self[0][1][0] = cp[2][0][1];
        self[0][0][0] = cp[2][0][2];
        self[0][2][1] = cp[2][1][0];
        self[0][1][1] = cp[2][1][1];
        self[0][0][1] = cp[2][1][2];
        self[0][2][2] = cp[2][2][0];
        self[0][1][2] = cp[2][2][1];
        self[0][0][2] = cp[2][2][2];
        self[1][2][0] = cp[3][0][0];
        self[1][1][0] = cp[3][0][1];
        self[1][0][0] = cp[3][0][2];
        self[1][2][1] = cp[3][1][0];
        self[1][1][1] = cp[3][1][1];
        self[1][0][1] = cp[3][1][2];
        self[1][2][2] = cp[3][2][0];
        self[1][1][2] = cp[3][2][1];
        self[1][0][2] = cp[3][2][2];
        self[4][2][0] = cp[4][0][0];
        self[4][1][0] = cp[4][0][1];
        self[4][0][0] = cp[4][0][2];
        self[4][2][1] = cp[4][1][0];
        self[4][0][1] = cp[4][1][2];
        self[4][2][2] = cp[4][2][0];
        self[4][1][2] = cp[4][2][1];
        self[4][0][2] = cp[4][2][2];
        self[5][2][0] = cp[5][0][0];
        self[5][1][0] = cp[5][0][1];
        self[5][0][0] = cp[5][0][2];
        self[5][2][1] = cp[5][1][0];
        self[5][0][1] = cp[5][1][2];
        self[5][2][2] = cp[5][2][0];
        self[5][1][2] = cp[5][2][1];
        self[5][0][2] = cp[5][2][2];

    def y(self):

        cp = copy.copy(self)

        self[2][0][2] = cp[0][0][0];
        self[2][1][2] = cp[0][0][1];
        self[2][2][2] = cp[0][0][2];
        self[2][0][1] = cp[0][1][0];
        self[2][1][1] = cp[0][1][1];
        self[2][2][1] = cp[0][1][2];
        self[2][0][0] = cp[0][2][0];
        self[2][1][0] = cp[0][2][1];
        self[2][2][0] = cp[0][2][2];
        self[3][0][2] = cp[1][0][0];
        self[3][1][2] = cp[1][0][1];
        self[3][2][2] = cp[1][0][2];
        self[3][0][1] = cp[1][1][0];
        self[3][1][1] = cp[1][1][1];
        self[3][2][1] = cp[1][1][2];
        self[3][0][0] = cp[1][2][0];
        self[3][1][0] = cp[1][2][1];
        self[3][2][0] = cp[1][2][2];
        self[1][0][0] = cp[2][0][0];
        self[1][1][0] = cp[2][0][1];
        self[1][2][0] = cp[2][0][2];
        self[1][0][1] = cp[2][1][0];
        self[1][1][1] = cp[2][1][1];
        self[1][2][1] = cp[2][1][2];
        self[1][0][2] = cp[2][2][0];
        self[1][1][2] = cp[2][2][1];
        self[1][2][2] = cp[2][2][2];
        self[0][0][0] = cp[3][0][0];
        self[0][1][0] = cp[3][0][1];
        self[0][2][0] = cp[3][0][2];
        self[0][0][1] = cp[3][1][0];
        self[0][1][1] = cp[3][1][1];
        self[0][2][1] = cp[3][1][2];
        self[0][0][2] = cp[3][2][0];
        self[0][1][2] = cp[3][2][1];
        self[0][2][2] = cp[3][2][2];
        self[4][0][2] = cp[4][0][0];
        self[4][1][2] = cp[4][0][1];
        self[4][2][2] = cp[4][0][2];
        self[4][0][1] = cp[4][1][0];
        self[4][2][1] = cp[4][1][2];
        self[4][0][0] = cp[4][2][0];
        self[4][1][0] = cp[4][2][1];
        self[4][2][0] = cp[4][2][2];
        self[5][0][2] = cp[5][0][0];
        self[5][1][2] = cp[5][0][1];
        self[5][2][2] = cp[5][0][2];
        self[5][0][1] = cp[5][1][0];
        self[5][2][1] = cp[5][1][2];
        self[5][0][0] = cp[5][2][0];
        self[5][1][0] = cp[5][2][1];
        self[5][2][0] = cp[5][2][2];

    def Z(self):

        cp = copy.copy(self)

        self[0][2][0] = cp[0][0][0];
        self[0][1][0] = cp[0][0][1];
        self[0][0][0] = cp[0][0][2];
        self[0][2][1] = cp[0][1][0];
        self[0][0][1] = cp[0][1][2];
        self[0][2][2] = cp[0][2][0];
        self[0][1][2] = cp[0][2][1];
        self[0][0][2] = cp[0][2][2];
        self[1][2][0] = cp[1][0][0];
        self[1][1][0] = cp[1][0][1];
        self[1][0][0] = cp[1][0][2];
        self[1][2][1] = cp[1][1][0];
        self[1][0][1] = cp[1][1][2];
        self[1][2][2] = cp[1][2][0];
        self[1][1][2] = cp[1][2][1];
        self[1][0][2] = cp[1][2][2];
        self[5][2][0] = cp[2][0][0];
        self[5][2][1] = cp[2][0][1];
        self[5][2][2] = cp[2][0][2];
        self[5][1][0] = cp[2][1][0];
        self[5][1][1] = cp[2][1][1];
        self[5][1][2] = cp[2][1][2];
        self[5][0][0] = cp[2][2][0];
        self[5][0][1] = cp[2][2][1];
        self[5][0][2] = cp[2][2][2];
        self[4][2][0] = cp[3][0][0];
        self[4][2][1] = cp[3][0][1];
        self[4][2][2] = cp[3][0][2];
        self[4][1][0] = cp[3][1][0];
        self[4][1][1] = cp[3][1][1];
        self[4][1][2] = cp[3][1][2];
        self[4][0][0] = cp[3][2][0];
        self[4][0][1] = cp[3][2][1];
        self[4][0][2] = cp[3][2][2];
        self[2][0][0] = cp[4][0][0];
        self[2][0][1] = cp[4][0][1];
        self[2][0][2] = cp[4][0][2];
        self[2][1][0] = cp[4][1][0];
        self[2][1][1] = cp[4][1][1];
        self[2][1][2] = cp[4][1][2];
        self[2][2][0] = cp[4][2][0];
        self[2][2][1] = cp[4][2][1];
        self[2][2][2] = cp[4][2][2];
        self[3][0][0] = cp[5][0][0];
        self[3][0][1] = cp[5][0][1];
        self[3][0][2] = cp[5][0][2];
        self[3][1][0] = cp[5][1][0];
        self[3][1][1] = cp[5][1][1];
        self[3][1][2] = cp[5][1][2];
        self[3][2][0] = cp[5][2][0];
        self[3][2][1] = cp[5][2][1];
        self[3][2][2] = cp[5][2][2];

    def z(self):

        cp = copy.copy(self)

        self[0][0][2] = cp[0][0][0];
        self[0][1][2] = cp[0][0][1];
        self[0][2][2] = cp[0][0][2];
        self[0][0][1] = cp[0][1][0];
        self[0][2][1] = cp[0][1][2];
        self[0][0][0] = cp[0][2][0];
        self[0][1][0] = cp[0][2][1];
        self[0][2][0] = cp[0][2][2];
        self[1][0][2] = cp[1][0][0];
        self[1][1][2] = cp[1][0][1];
        self[1][2][2] = cp[1][0][2];
        self[1][0][1] = cp[1][1][0];
        self[1][2][1] = cp[1][1][2];
        self[1][0][0] = cp[1][2][0];
        self[1][1][0] = cp[1][2][1];
        self[1][2][0] = cp[1][2][2];
        self[4][0][0] = cp[2][0][0];
        self[4][0][1] = cp[2][0][1];
        self[4][0][2] = cp[2][0][2];
        self[4][1][0] = cp[2][1][0];
        self[4][1][1] = cp[2][1][1];
        self[4][1][2] = cp[2][1][2];
        self[4][2][0] = cp[2][2][0];
        self[4][2][1] = cp[2][2][1];
        self[4][2][2] = cp[2][2][2];
        self[5][0][0] = cp[3][0][0];
        self[5][0][1] = cp[3][0][1];
        self[5][0][2] = cp[3][0][2];
        self[5][1][0] = cp[3][1][0];
        self[5][1][1] = cp[3][1][1];
        self[5][1][2] = cp[3][1][2];
        self[5][2][0] = cp[3][2][0];
        self[5][2][1] = cp[3][2][1];
        self[5][2][2] = cp[3][2][2];
        self[3][2][0] = cp[4][0][0];
        self[3][2][1] = cp[4][0][1];
        self[3][2][2] = cp[4][0][2];
        self[3][1][0] = cp[4][1][0];
        self[3][1][1] = cp[4][1][1];
        self[3][1][2] = cp[4][1][2];
        self[3][0][0] = cp[4][2][0];
        self[3][0][1] = cp[4][2][1];
        self[3][0][2] = cp[4][2][2];
        self[2][2][0] = cp[5][0][0];
        self[2][2][1] = cp[5][0][1];
        self[2][2][2] = cp[5][0][2];
        self[2][1][0] = cp[5][1][0];
        self[2][1][1] = cp[5][1][1];
        self[2][1][2] = cp[5][1][2];
        self[2][0][0] = cp[5][2][0];
        self[2][0][1] = cp[5][2][1];
        self[2][0][2] = cp[5][2][2];

    def twist(self, moves):

        for move in moves:

            if move == 'R':
                self.R()
            elif move == 'r':
                self.r()
            elif move == 'L':
                self.L()
            elif move == 'l':
                self.l()
            elif move == 'U':
                self.U()
            elif move == 'u':
                self.u()
            elif move == 'D':
                self.D()
            elif move == 'd':
                self.d()
            elif move == 'F':
                self.F()
            elif move == 'f':
                self.f()
            elif move == 'B':
                self.B()
            elif move == 'b':
                self.b()
            elif move == 'X':
                self.X()
            elif move == 'x':
                self.x()
            elif move == 'Y':
                self.Y()
            elif move == 'y':
                self.y()
            elif move == 'Z':
                self.Z()
            elif move == 'z':
                self.z()
            elif move == '':
                pass

        return self

    def solve(self):

        def solve_centers():

            possible_moves = ['x', 'y', 'z', 'X', 'Y', 'Z', '']

            current_moves = ['']

            unsolved = True

            while unsolved:

                for i, j in product(possible_moves, current_moves):

                    t = copy.copy(self)

                    t = t.twist(i + j)

                    current_moves.append(i + j)

                    if (t[0][1][1]['col'] == 0) and (t[4][1][1]['col'] == 4):
                        unsolved = False

                        self.twist(i + j)

                        break

            return (i + j)

        def clear_cross():

            #               RY       RB         RW       RB
            red_edges = {6, 35, 42, 32, 30, 34, 18, 33}

            possible_moves = ['r', 'l', 'u', 'd', 'f', 'b', 'R', 'L', 'U', 'D', 'F', 'B', '']

            current_moves = ['']

            # Remove any red edges from the top layer

            unsolved = True

            q = 0

            while unsolved:

                q = q + 1

                for i, j in product(possible_moves, current_moves):

                    t = copy.copy(self)

                    t = t.twist(i + j)

                    current_moves.append(i + j)

                    if (t[0][0][1]['id'] not in red_edges
                            and t[0][2][1]['id'] not in red_edges
                            and t[0][1][0]['id'] not in red_edges
                            and t[0][1][2]['id'] not in red_edges):
                        unsolved = False

                        break

            moves = i + j

            self.twist(moves)

            return (moves)

        def solve_cross():

            possible_moves = ['f', 'F', 'uRU', 'Ulu', 'FF', 'DRfr', 'D', 'RdFFr', 'RRfrr', 'lDFFL', 'llFLL', '']

            current_moves = ['']

            moves = ''

            # Remove any red edges from the top layer

            q = 0

            for z in range(4):

                unsolved = True

                while unsolved:

                    q = q + 1

                    for i, j in product(possible_moves, current_moves):

                        t = copy.copy(self)

                        t = t.twist(moves + i + j)

                        current_moves.append(i + j)

                        if (t[0][1][0]['col'] == 0 and t[4][1][1]['col'] == t[4][1][2]['col']):
                            unsolved = False

                            break

                moves = moves + i + j + 'z'

            self.twist(moves)

            return (moves)

        def clear_corners():

            #               RYG             RYB         RWG       RWB
            red_corners = {0, 17, 15, 12, 53, 14, 36, 16, 51, 48, 52, 50}

            possible_moves = ['LDl', 'Z']

            current_moves = ['']

            # Remove any red edges from the top layer

            unsolved = True

            q = 0

            while unsolved:

                q = q + 1

                for i, j in product(possible_moves, current_moves):

                    t = copy.copy(self)

                    t = t.twist(i + j)

                    current_moves.append(i + j)

                    if (t[0][0][0]['id'] not in red_corners
                            and t[0][2][0]['id'] not in red_corners
                            and t[0][0][2]['id'] not in red_corners
                            and t[0][2][2]['id'] not in red_corners):
                        unsolved = False

                        break

            moves = i + j

            self.twist(moves)

            return (moves)

        def solve_corners():

            possible_moves = ['D', 'Ldl', 'dLDl', 'LdlfDDF', '']

            current_moves = ['']

            moves = ''

            q = 0

            for z in range(4):

                unsolved = True

                while unsolved:

                    q = q + 1

                    for i, j in product(possible_moves, current_moves):

                        t = copy.copy(self)

                        t = t.twist(moves + i + j)

                        current_moves.append(i + j)

                        if (t[0][0][0]['col'] == 0
                                and t[4][0][2]['col'] == t[4][1][1]['col']):
                            #    and t[3][2][0]['col'] == t[3][1][1]['col']):

                            unsolved = False

                            break

                moves = moves + i + j + 'z'

            self.twist(moves)

            return (moves)

        def invert_cube():

            moves = 'xx'

            self.twist(moves)

            return (moves)

        def solve_middle():

            possible_moves = ['', 'U', 'u', 'ulULUFuf', 'URurufUF', 'UFufulUL',
                              'zulULUFufZ', 'zURurufUFZ', 'zUFufulULZ',
                              'zzulULUFufZZ', 'zzURurufUFZZ', 'zzUFufulULZZ',
                              'ZulULUFufz', 'ZURurufUFz', 'ZUFufulULz', ]

            current_moves = ['']

            moves = ''

            q = 0

            t = copy.copy(self)

            while (t[2][0][1]['col'] == t[2][1][1]['col'] and t[2][2][1]['col'] == t[2][1][1]['col']
                   and t[3][0][1]['col'] == t[3][1][1]['col'] and t[3][2][1]['col'] == t[3][1][1]['col']
                   and t[4][0][1]['col'] == t[4][1][1]['col'] and t[4][2][1]['col'] == t[4][1][1]['col']
                   and t[5][0][1]['col'] == t[5][1][1]['col'] and t[5][2][1]['col'] == t[5][1][1]['col']) is False:

                for z in range(4):

                    # Record the right front edge to prevent later edges mucking up already solved edges.

                    unsolved = True

                    while unsolved:

                        for i, j in product(possible_moves, current_moves):

                            t = copy.copy(self)

                            t = t.twist(moves + i + j)

                            current_moves.append(i + j)

                            if (t[4][0][1]['col'] == t[4][1][1]['col']
                                    and t[3][0][1]['col'] == t[3][1][1]['col']):
                                unsolved = False

                                moves = moves + i + j + 'z'

                                break

            self.twist(moves)

            return (moves)

        def top_cross():

            possible_moves = ['FRUruf', 'U', '']

            current_moves = ['']

            moves = ''

            q = 0

            unsolved = True

            while unsolved:

                q = q + 1

                for i, j in product(possible_moves, current_moves):

                    t = copy.copy(self)

                    t = t.twist(moves + i + j)

                    current_moves.append(i + j)

                    if (t[0][0][1]['col'] == 1 and t[0][2][1]['col'] == 1 and t[0][1][0]['col'] == 1 and t[0][1][2][
                        'col'] == 1):
                        moves = moves + i + j

                        unsolved = False

                        break

            self.twist(moves)

            return (moves)

        def fix_cross():

            possible_moves = ['', 'U', 'RUrURUUr']

            current_moves = ['']

            moves = ''

            q = 0

            unsolved = True

            while unsolved:

                q = q + 1

                for i, j in product(possible_moves, current_moves):

                    t = copy.copy(self)

                    t = t.twist(moves + i + j)

                    current_moves.append(i + j)

                    if (t[5][1][2]['col'] == t[5][1][1]['col']
                            and t[4][1][2]['col'] == t[4][1][1]['col']
                            and t[3][1][2]['col'] == t[3][1][1]['col']):
                        #                 and t[5][1][2]['col'] == t[5][1][1]['col']):

                        moves = moves + i + j

                        unsolved = False

                        break

            self.twist(moves)

            return (moves)

        def final_corners():

            possible_moves = ['', 'U', 'URulUruL']

            current_moves = ['']

            moves = ''

            q = 0

            unsolved = True

            while unsolved:

                q = q + 1

                for i, j in product(possible_moves, current_moves):

                    t = copy.copy(self)

                    t = t.twist(moves + i + j)

                    current_moves.append(i + j)

                    if (t[4][2][2]['col'] in (t[0][1][1]['col'], t[4][1][1]['col'], t[2][1][1]['col'])
                            and t[0][2][0]['col'] in (t[0][1][1]['col'], t[4][1][1]['col'], t[2][1][1]['col'])
                            and t[2][0][2]['col'] in (t[0][1][1]['col'], t[4][1][1]['col'], t[2][1][1]['col'])
                            and t[4][0][2]['col'] in (t[0][1][1]['col'], t[3][1][1]['col'], t[3][1][1]['col'])
                            and t[0][0][0]['col'] in (t[0][1][1]['col'], t[3][1][1]['col'], t[4][1][1]['col'])
                            and t[3][0][2]['col'] in (t[0][1][1]['col'], t[3][1][1]['col'], t[4][1][1]['col'])
                            and t[4][1][2]['col'] == t[4][1][1]['col']):
                        moves = moves + i + j

                        unsolved = False

                        break

            self.twist(moves)

            return (moves)

        def turn_corners():

            possible_moves = ['', 'rdRD']

            current_moves = ['']

            moves = ''

            for z in range(4):

                unsolved = True

                while unsolved:

                    for i, j in product(possible_moves, current_moves):

                        t = copy.copy(self)

                        t = t.twist(moves + i + j)

                        current_moves.append(i + j)

                        if (t[0][2][0]['col'] == t[0][1][1]['col']):
                            unsolved = False

                            moves = moves + i + j + 'U'

                            break

            self.twist(moves)

            return (moves)

        solution = solve_centers()
        solution = solution + clear_cross()
        solution = solution + solve_cross()
        solution = solution + clear_corners()
        solution = solution + solve_corners()
        solution = solution + invert_cube()
        solution = solution + solve_middle()
        solution = solution + top_cross()
        solution = solution + fix_cross()
        solution = solution + final_corners()
        solution = solution + turn_corners()

        return solution

    def scramble(self):

        moves = ""

        for m in range(20):
            moves = moves + random.choice('RrLlUuDdFfBb')

        self.twist(moves)

        return (moves)


if __name__ == "__main__":

    cube = SimpleSolve()

    for z in range(1000):
        print(cube.scramble(), end="")

        solved = cube.solve()

        print('  Cube ', z, 'solved with ', len(solved), 'moves.')



