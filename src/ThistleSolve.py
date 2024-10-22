import threading
import itertools

from copy import deepcopy
from datetime import datetime


class BuildTable():

   def __init__(self, group, depth):

        group = group
        self.depth = depth
        groupmoves = ["RrSLlMUuVDdEFfGBbC", "RrSLlMVEFfGBbC", "RrSLlMVEGC", "SMVEGC"]
        self.table = []

        moves = groupmoves[group - 1]

        dup_cube = False

        start = ThistleSolve()

        self.table.append([start," "])
        level = 1

        while level <= depth:
            for i in range(0, len(self.table)):
                node = self.table[i]
                for move in moves:
                    new_node = deepcopy(node[0])
                    new_node.twist(move)
                    new_moves = node[1] + move
                    dup_cube = False
                    for test_node in self.table:

                        if new_node.isGroupEqual(group,test_node[0]): dup_cube = True

                    if dup_cube == False:
                        self.table.append([new_node, new_moves])

            print(group, level, len(self.table))

            level = level + 1

class ThistleSolve:

    def __init__(self, *args):

        super().__init__()

        # Used to record the turns used to trnsfrm the cube from base state

        self.moves = ""
        # Used to record the position and orientation of edges[0] and corners[1]
        self.cube = []
        self.cube.append([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C])
        self.cube.append([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

        # Used to hold transformation tables used by the solution
        self.tables = []

    def BuildTables(self):

        now = datetime.now()

        self.tables.append(BuildTable(1, 3).table)
        self.tables.append(BuildTable(2, 5).table)
        self.tables.append(BuildTable(3, 5).table)
        self.tables.append(BuildTable(4, 6).table)

        elapsed = datetime.now() - now

        print("Time Taken :", elapsed)
    def twist(self, moves):

        #  The twist function acts on the cube object passed to it.

        def rotate(cubie, direction):

            cubie_num = cubie & 0x0F
            cubie_dir = cubie & 0xF0

            if   direction == 'A':

                if   cubie_dir == 0x00: cubie_dir = 0x80
                elif cubie_dir == 0x40: cubie_dir = 0x00
                elif cubie_dir == 0x80: cubie_dir = 0x40

            elif direction == 'C':

                if   cubie_dir == 0x00: cubie_dir = 0x40;
                elif cubie_dir == 0x40: cubie_dir = 0x80;
                elif cubie_dir == 0x80: cubie_dir = 0x00;

            return cubie_num ^ cubie_dir
        def F():
            tmp              = self.cube[0][9]
            self.cube[0][9]  = self.cube[0][6]
            self.cube[0][6]  = self.cube[0][10]
            self.cube[0][10] = self.cube[0][7]
            self.cube[0][7]  = tmp

            tmp              = self.cube[1][4]
            self.cube[1][4]  = rotate(self.cube[1][5], 'A')
            self.cube[1][5]  = rotate(self.cube[1][2], 'C')
            self.cube[1][2]  = rotate(self.cube[1][7], 'A')
            self.cube[1][7]  = rotate(tmp, 'C')
        def B():

            tmp              = self.cube[0][12]
            self.cube[0][12] = self.cube[0][8]
            self.cube[0][8]  = self.cube[0][11]
            self.cube[0][11] = self.cube[0][5]
            self.cube[0][5]  = tmp

            tmp =self.cube[1][1]
            self.cube[1][1] = rotate(self.cube[1][8], 'A')
            self.cube[1][8] = rotate(self.cube[1][3], 'C')
            self.cube[1][3] = rotate(self.cube[1][6], 'A')
            self.cube[1][6] = rotate(tmp, 'C')
        def L():

            tmp             = self.cube[0][6]
            self.cube[0][6] = self.cube[0][1]
            self.cube[0][1] = self.cube[0][5]
            self.cube[0][5] = self.cube[0][2]
            self.cube[0][2] = tmp

            tmp             = self.cube[1][5]
            self.cube[1][5] = self.cube[1][1]
            self.cube[1][1] = self.cube[1][6]
            self.cube[1][6] = self.cube[1][2]
            self.cube[1][2] = tmp
        def R():

            tmp             = self.cube[0][3]
            self.cube[0][3] = self.cube[0][8]
            self.cube[0][8] = self.cube[0][4]
            self.cube[0][4] = self.cube[0][7]
            self.cube[0][7] = tmp

            tmp             = self.cube[1][8]
            self.cube[1][8] = self.cube[1][4]
            self.cube[1][4] = self.cube[1][7]
            self.cube[1][7] = self.cube[1][3]
            self.cube[1][3] = tmp
        def U():

            tmp              = self.cube[0][12]
            self.cube[0][12] = self.cube[0][1] ^ 0x80
            self.cube[0][1]  = self.cube[0][9] ^ 0x80
            self.cube[0][9]  = self.cube[0][4] ^ 0x80
            self.cube[0][4]  = tmp ^ 0x80

            tmp              = self.cube[1][1]
            self.cube[1][1]  =rotate(self.cube[1][5], 'C')
            self.cube[1][5]  =rotate(self.cube[1][4], 'A')
            self.cube[1][4]  =rotate(self.cube[1][8], 'C')
            self.cube[1][8]  = rotate(tmp, 'A')
        def D():

            tmp              = self.cube[0][10]
            self.cube[0][10] = self.cube[0][2] ^ 0x80
            self.cube[0][2]  = self.cube[0][11] ^ 0x80
            self.cube[0][11] = self.cube[0][3] ^ 0x80
            self.cube[0][3]  = tmp ^ 0x80

            tmp              = self.cube[1][2]
            self.cube[1][2]  =rotate(self.cube[1][6], 'C')
            self.cube[1][6]  =rotate(self.cube[1][3], 'A')
            self.cube[1][3]  =rotate(self.cube[1][7], 'C')
            self.cube[1][7]  = rotate(tmp, 'A')

        for move in moves:
            if   move == 'R': R()
            elif move == 'r': R(); R(); R()
            elif move == 'S': R(); R()
            elif move == 'L': L()
            elif move == 'l': L(); L(); L()
            elif move == 'M': L(); L()
            elif move == 'U': U()
            elif move == 'u': U(); U(); U()
            elif move == 'V': U(); U()
            elif move == 'D': D()
            elif move == 'd': D(); D(); D()
            elif move == 'E': D(); D()
            elif move == 'F': F()
            elif move == 'f': F(); F(); F()
            elif move == 'G': F(); F()
            elif move == 'B': B()
            elif move == 'b': B(); B(); B()
            elif move == 'C': B(); B();
            else: pass

        return self
    def print_cube(self):

        cube_text = ""

        for i in range(1,13):

            if ((self.cube[0][i] & 0xF0) != 0x00): cube_text = cube_text + "*"

            cube_text = cube_text + str(self.cube[0][i] & 0x0F) + " "

        for i in range (1,9):

            if   (self.cube[1][i] & 0xF0)  == 0xC0: cube_text = cube_text + "x"
            elif ((self.cube[1][i] & 0xF0) == 0x40): cube_text = cube_text + "c"
            elif ((self.cube[1][i] & 0xF0) == 0x80): cube_text = cube_text + "a"
            else: cube_text = cube_text + " "

            cube_text = cube_text + str(self.cube[1][i] & 0x0F) + " "

        return cube_text

    def __str__(self):
        return self.print_cube()

    def isEqual(self, testCube):

        equal = True

        for i in range (0,13):

            if (testCube.cube[0][i] != self.cube[0][i]) & (testCube.cube[0][min(8, i)] != self.cube[0][min(8,i)]):

                equal = False

                break

        return equal

    def corner_twist(self):

        # Twist: given a configuration of corners in tetrad 1, there are only 3 possible configurations in tetrad 2.
        # This function returns 1, 2 or 3 depending on which configuration

        tetrad_2 =[i for i in self.cube[1][5:9]]

        min_pos  = tetrad_2.index(min(tetrad_2))

        rotated  = tetrad_2[min_pos:] + tetrad_2[:min_pos]

        return rotated.index(max(rotated))

    def tetrad_1(self):

        return self.cube[1][1:5]

    def edge_parity(self):

        changes, edge_list = 0, [i for i in self.cube[0]]
        for p in range(len(edge_list)):
            min = 13
            for i, item in enumerate(edge_list[p:]):
                if item < min: argmin, min = i + p, item;
            if argmin > p:
                edge_list[p], edge_list[argmin] = edge_list[argmin], edge_list[p]
                changes += 1
        parity = changes % 2

        return parity


    def isGroupEqual(self, group, testCube):

        def slice(i):
            if   (i in [1,2,3,4]): slice = 1
            elif (i in [5,6,7,8]): slice = 2
            else: slice = 3
            return(slice)

        def tetrad(i):
            tetrad = 2
            if   (i <= 4): tetrad = 1
            return(tetrad)

        equal = True

        if   group == 1:
            #2028 = 2**(12-1) ways of orienting the 12 edge pieces
            for i in range(1,13):
                if ((self.cube[0][i] & 0x80) != (testCube.cube[0][i] & 0x80)): equal = False

        elif group == 2:
           # for i in [5,6,7,8]:
           #     if slice(self.cube[0][i])  != slice(testCube.cube[0][i]):
           #         equal = False
           #         break
            if equal:
                for i in range(0,9):
                    if self.cube[1][i] & 0xc0 != testCube.cube[1][i] & 0xc0:
                        equal = False
                        break

        elif group == 3:

            #
            for i in range(1,13):
                if slice(self.cube[0][i])  != slice(testCube.cube[0][i]) :
                    equal = False
                    break
            if equal:
                for i in range(1,9):
                    if tetrad(self.cube[1][i]) != tetrad(testCube.cube[1][i]):
                        equal = False
                        break
            if equal:
                if self.edge_parity() != testCube.edge_parity():
                    equal = False
            if equal:
                if self.corner_twist()!= testCube.corner_twist():
                    equal = False
            if equal:
                if self.tetrad_1() != testCube.tetrad_1():
                    equal = False


        elif group == 4:
            for i in range(1, 13):
                if self.cube[0][i]  != testCube.cube[0][i]:
                    equal = False
                    break
            if equal:
                for i in range(0,9):
                    if self.cube[1][i] != testCube.cube[1][i]:
                        equal = False
                        break


        return equal

    def solve(self):

        solution = ""

        tryCube = ThistleSolve()
        tryCube2 = ThistleSolve()
        tryCube3 = ThistleSolve()

        for node3 in self.tables[0]:
            transform3 = node3[0]
            for node2 in self.tables[0]:
                transform2 = node2[0]
                for node1 in self.tables[0]:
                    transform1 = node1[0]
                    solution = node3[1] + node2[1] + node1[1]
                    for i in range (1,13):

                        tryCube.cube[0][transform1.cube[0][i] & 0x0F]  = self.cube[0][i] ^ (transform1.cube[0][i] & 0xF0)
                        tryCube2.cube[0][transform2.cube[0][i] & 0x0F] = tryCube.cube[0][i] ^ (transform2.cube[0][i] & 0xF0)
                        tryCube3.cube[0][transform3.cube[0][i] & 0x0F] = tryCube2.cube[0][i] ^ (transform3.cube[0][i] & 0xF0)

                    solved = True

                    for j in range(1,13):

                        if tryCube3.cube[0][j] & 0xF0 != 0:
                            solved = False
                            break

                if solved == True: break

            if solved == True: break

        if solved == True:
            print("Solved: ", tryCube3.print_cube())

            self.twist(solution)

        else:
            group1_solution = "XXX"

        print(solution)

        return solution






# Make a copy of the corners positions, and solve for tetrad 1
        # corners = [i for i in self.cube[1]]
        #
        # for p in range(1,5):
        #     argmin = p + corners[p:5].index(min(corners[p:5]))
        #
        #     if p == 1 and argmin == 1: pass
        #     if p == 1 and argmin == 2: corners[1], corners[2], corners[5], corners[6] = corners[2], corners[1], corners[6], corners[5] #L2
        #     if p == 1 and argmin == 3: corners[1], corners[3], corners[6], corners[8] = corners[3], corners[1], corners[8], corners[6] #B2
        #     if p == 1 and argmin == 4: corners[1], corners[4], corners[5], corners[8] = corners[4], corners[1], corners[8], corners[5] #U2
        #
        #     if p == 2 and argmin == 2: pass
        #     if p == 2 and argmin == 3: corners[2], corners[3], corners[6], corners[7] = corners[3], corners[2], corners[7], corners[6] #D2
        #     if p == 2 and argmin == 4: corners[2], corners[4], corners[5], corners[7] = corners[4], corners[2], corners[7], corners[5] #F2
        #
        #     if p == 3 and argmin == 3: pass
        #     if p == 3 and argmin == 4: corners[3], corners[4], corners[7], corners[8] = corners[4], corners[3], corners[8], corners[7] #R2
        #
        # argmin, argmax = corners[5:9].index(min(corners[5:9])), corners[5:9].index(max(corners[5:9]))
        #
        # twist = argmax - argmin if argmax > argmin else 4 + argmax - argmin
        #
        # return twist, corners[5:9], corners[1:5]