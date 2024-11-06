import os
import pickle
import queue
import random

from requests.packages import target


class ThistleCube:

    edges         = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]
    corners       = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
    parity        = [0x00]
    identity_cube = bytes(edges + corners + parity)

    thistlewaite_tables = 'thistle.pickle'

    def generate_new(members, generators, subgroup_mask):

        members_list = set(
            [bytes([membercube[i] & subgroup_mask[i] for i in range(0, 21)]) for membercube in members.values()])

        candidates, new_members = dict(), dict()

        for name, membercube in members.items():
            for n, generator in generators.items():
                new_name = name + n
                new_twist_array = ([membercube[0x0F & generator[i]] ^ (generator[i] & 0xF0) for i in range(0, 12)] +
                                   [(membercube[12 + (0x0F & generator[j])] & 0x0F) + (((membercube[12 + (
                                               0x0F & generator[j])] & 0xF0) + (generator[j] & 0xF0)) % 0xC0) for j in
                                    range(12, 20)] +
                                   [membercube[20] ^ generator[20]])
                new_twist = bytes(new_twist_array)

                twist_masked = bytes([new_twist[i] & subgroup_mask[i] for i in range(0, 21)])

                if twist_masked not in members_list:
                    new_members[new_name] = new_twist
                    members_list.add(twist_masked)

        return new_members

    moves_dict = {
        'R': bytes(b'\x00\x01\x07\x06\x04\x05\x02\x03\x08\t\n\x0b\x00\x01\x07\x06\x04\x05\x02\x03\x80'),
        'L': bytes(b'\x04\x05\x02\x03\x01\x00\x06\x07\x08\t\n\x0b\x05\x04\x02\x03\x00\x01\x06\x07\x80'),
        'F': bytes(b'\x00\x01\x02\x03\x04\t\x08\x07\x05\x06\n\x0b\x00\x86\x02\x84A\x05C\x07\x80'),
        'B': bytes(b'\x00\x01\x02\x03\x0b\x05\x06\n\x08\t\x04\x07\x87\x01\x85\x03\x04@\x06B\x80'),
        'U': bytes(b'\x88\x01\x02\x8b\x04\x05\x06\x07\x83\t\n\x80D\x01\x02G\x83\x05\x06\x80\x80'),
        'D': bytes(b'\x00\x8a\x89\x03\x04\x05\x06\x07\x08\x81\x82\x0b\x00EF\x03\x04\x82\x81\x07\x80'),
        'S': bytes(b'\x00\x01\x03\x02\x04\x05\x07\x06\x08\t\n\x0b\x00\x01\x03\x02\x04\x05\x07\x06\x00'),
        'M': bytes(b'\x01\x00\x02\x03\x05\x04\x06\x07\x08\t\n\x0b\x01\x00\x02\x03\x05\x04\x06\x07\x00'),
        'G': bytes(b'\x00\x01\x02\x03\x04\x06\x05\x07\t\x08\n\x0b\x00\x03\x02\x01\x06\x05\x04\x07\x00'),
        'C': bytes(b'\x00\x01\x02\x03\x07\x05\x06\x04\x08\t\x0b\n\x02\x01\x00\x03\x04\x07\x06\x05\x00'),
        'V': bytes(b'\x03\x01\x02\x00\x04\x05\x06\x07\x0b\t\n\x08\x03\x01\x02\x00\x07\x05\x06\x04\x00'),
        'E': bytes(b'\x00\x02\x01\x03\x04\x05\x06\x07\x08\n\t\x0b\x00\x02\x01\x03\x04\x06\x05\x07\x00'),
        'r': bytes(b'\x00\x01\x06\x07\x04\x05\x03\x02\x08\t\n\x0b\x00\x01\x06\x07\x04\x05\x03\x02\x80'),
        'l': bytes(b'\x05\x04\x02\x03\x00\x01\x06\x07\x08\t\n\x0b\x04\x05\x02\x03\x01\x00\x06\x07\x80'),
        'f': bytes(b'\x00\x01\x02\x03\x04\x08\t\x07\x06\x05\n\x0b\x00\x84\x02\x86C\x05A\x07\x80'),
        'b': bytes(b'\x00\x01\x02\x03\n\x05\x06\x0b\x08\t\x07\x04\x85\x01\x87\x03\x04B\x06@\x80'),
        'u': bytes(b'\x8b\x01\x02\x88\x04\x05\x06\x07\x80\t\n\x83G\x01\x02D\x80\x05\x06\x83\x80'),
        'd': bytes(b'\x00\x89\x8a\x03\x04\x05\x06\x07\x08\x82\x81\x0b\x00FE\x03\x04\x81\x82\x07\x80')
    }

    edge_dict = {0:'WR', 1:'YR', 2:'OY', 3:'WO', 4:'RG', 5:'RB', 6:'OB', 7:'OG', 8:'WB', 9:'YB', 10:'YG', 11:'WG'}

    group_moves = ['RLFBUDrlfbudSMGCVE', 'RLFBrlfbSMGCVE', 'RLrlSMGCVE', 'SMGCVE']
    group_masks = [[[0x80], [0x00], [0x00]],
                   [[0x08], [0xC0], [0x00]],
                   [[0x0C], [0x06], [0xFF]],
                   [[0xFF], [0xFF], [0xF0]]]
    bit_masks = [bytes(group_mask[0] * 12 + group_mask[1] * 8 + group_mask[2]) for group_mask in group_masks]

    try:

        with open(os.path.join(os.getcwd(), 'rsc', thistlewaite_tables), 'rb') as f:
            thistle_tables = pickle.load(f)

    except FileNotFoundError:
        print('Generating Tables')
        thistle_tables = []
        for group in range(0, 4):
            move_dict = dict()
            for move_key in group_moves[group]:
                move_dict[move_key] = moves_dict[move_key]
            #move_dict = {move_key: moves_dict[move_key] for move_key in group_moves[group]}

            #move_dict = moves_dict
            bit_mask = bytes(group_masks[group][0] * 12 + group_masks[group][1] * 8 + group_masks[group][2])
            new, members = 1, {'': identity_cube}
            while new > 0:
                new_members = generate_new(members, move_dict, bit_mask)
                new = len(new_members)
                members.update(new_members)
            print(group, len(members))
            thistle_tables.append(members)
        with open(os.path.join(os.getcwd(), 'rsc', thistlewaite_tables), 'wb') as file:
            pickle.dump(thistle_tables, file)




    def __init__(self, cube=None):

        edges = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]
        corners = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        parity = [0x00]

        self.cube = bytes(edges + corners + parity) if cube==None else cube.cube

    def move_cube(self, moves):

        for m in moves:

            if m in self.moves_dict.keys():

                move = self.moves_dict[m]

                new_cube_array  = ([self.cube[0x0F & move[i]] ^ (move[i] & 0xF0) for i in range(0, 12)] +
                                   [(self.cube[12 + (0x0F & move[j])] & 0x0F) + (
                                               ((self.cube[12 + (0x0F & move[j])] & 0xF0) + (move[j] & 0xF0)) % 0xC0)
                                    for j in range(12, 20)] +
                                   [self.cube[20] ^ move[20]])

                self.cube = bytes(new_cube_array)

    def reverse(self, moves):

        reverse = ''
        for move in moves[::-1]:
            if   move in 'SMGCVE': reverse += move
            elif move in 'RLFBUD': reverse += move.lower()
            else: reverse += move.upper()

        return reverse

    def solve(self, group=4):

        solution = ''
        temp_cube = ThistleCube(cube=self)

        for group in range(0, group):
            if group > 0: solution = solution + '-'

            masked_cube = bytes([temp_cube.cube[i] & self.bit_masks[group][i] for i in range(0,21)])

            for moves, group_cube in self.thistle_tables[group].items():
                group_cube = bytes([group_cube[i] & self.bit_masks[group][i] for i in range(0,21)])
                if group_cube == masked_cube:
                    solution = solution +  self.reverse(moves)
                    temp_cube.move_cube(self.reverse(moves))
                    print('Group:', group, 'solution', self.reverse(moves), temp_cube.cube)
               #             break
        return solution

    def __str__(self):

        numbers = ''
        colours = ''

        for edge in self.cube[:12]:
            number  = edge & 0x0F
            flipped = edge & 0x80
            edgestr = '*' + str(number) if flipped==0x80 else ' ' + str(number)
            colstr  = self.edge_dict[number]
            numbers += edgestr + ' '
            colours += colstr + ' '

        for corner in self.cube[12:20]:
            number = corner & 0x0F
            orient = corner & 0xC0
            if   orient == 0x00: prefix = ' '
            elif orient == 0x40: prefix = 'A'
            elif orient == 0x80: prefix = 'C'
            cornerstr = prefix + str(number)

            numbers += cornerstr + ' '

        numbers = numbers + ' ' + str(self.cube[20])

        return numbers + '  ' + colours

    def optimal(self):

        def distance(cube):
            dist = 0
            for target, edge in enumerate(cube.cube[0:12]):
               dist += (edge != target)
            return dist

        searchtree = queue.PriorityQueue()
        searchtree.put((distance(self), ['',  ThistleCube(cube=self)]))

        while not searchtree.empty():
            [queue_move, queue_cube] = searchtree.get()

            print(queue_move, distance(queue_cube))

            if distance(queue_cube) > 0:
                for move in self.moves_dict.keys():
                    test_cube = ThistleCube(cube=queue_cube)
                    test_cube.move_cube(move)
                    print(queue_move + move, distance(test_cube))
                    searchtree.put((distance(test_cube), [queue_move + move, test_cube]) )
            else:
                break









        return ''






