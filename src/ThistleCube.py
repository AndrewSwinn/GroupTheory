import os
import pickle

class ThistleCube:

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
                                   [cube[20] ^ generator[20]])
                new_twist = bytes(new_twist_array)

                twist_masked = bytes([new_twist[i] & subgroup_mask[i] for i in range(0, 21)])

                if twist_masked not in members_list:
                    new_members[new_name] = new_twist
                    members_list.add(twist_masked)

        return new_members

    thistle_tables = []

    moves_dict = {
        'R': bytes(b'\x00\x01\x06\x07\x04\x05\x03\x02\x08\t\n\x0b\x00\x01\x07\x06\x04\x05\x02\x03\x80'),
        'L': bytes(b'\x04\x05\x02\x03\x01\x00\x06\x07\x08\t\n\x0b\x05\x04\x02\x03\x00\x01\x06\x07\x80'),
        'F': bytes(b'\x00\x01\x02\x03\x04\t\x08\x07\x05\x06\n\x0b\x00\x86\x02\x84A\x05C\x07\x80'),
        'B': bytes(b'\x00\x01\x02\x03\x0b\x05\x06\n\x08\t\x04\x07\x87\x01\x85\x03\x04@\x06B\x80'),
        'U': bytes(b'\x88\x01\x8b\x03\x04\x05\x06\x07\x82\t\n\x80D\x01\x02G\x83\x05\x06\x80\x80'),
        'D': bytes(b'\x00\x8a\x02\x89\x04\x05\x06\x07\x08\x81\x83\x0b\x00EF\x03\x04\x82\x81\x07\x80'),
        'S': bytes(b'\x00\x01\x03\x02\x04\x05\x07\x06\x08\t\n\x0b\x00\x01\x03\x02\x04\x05\x07\x06\x00'),
        'M': bytes(b'\x01\x00\x02\x03\x05\x04\x06\x07\x08\t\n\x0b\x01\x00\x02\x03\x05\x04\x06\x07\x00'),
        'G': bytes(b'\x00\x01\x02\x03\x04\x06\x05\x07\t\x08\n\x0b\x00\x03\x02\x01\x06\x05\x04\x07\x00'),
        'C': bytes(b'\x00\x01\x02\x03\x07\x05\x06\x04\x08\t\x0b\n\x02\x01\x00\x03\x04\x07\x06\x05\x00'),
        'V': bytes(b'\x02\x01\x00\x03\x04\x05\x06\x07\x0b\t\n\x08\x03\x01\x02\x00\x07\x05\x06\x04\x00'),
        'E': bytes(b'\x00\x03\x02\x01\x04\x05\x06\x07\x08\n\t\x0b\x00\x02\x01\x03\x04\x06\x05\x07\x00'),
        'r': bytes(b'\x00\x01\x07\x06\x04\x05\x02\x03\x08\t\n\x0b\x00\x01\x06\x07\x04\x05\x03\x02\x80'),
        'l': bytes(b'\x05\x04\x02\x03\x00\x01\x06\x07\x08\t\n\x0b\x04\x05\x02\x03\x01\x00\x06\x07\x80'),
        'f': bytes(b'\x00\x01\x02\x03\x04\x08\t\x07\x06\x05\n\x0b\x00\x84\x02\x86C\x05A\x07\x80'),
        'b': bytes(b'\x00\x01\x02\x03\n\x05\x06\x0b\x08\t\x07\x04\x85\x01\x87\x03\x04B\x06@\x80'),
        'u': bytes(b'\x8b\x01\x88\x03\x04\x05\x06\x07\x80\t\n\x82G\x01\x02D\x80\x05\x06\x83\x80'),
        'd': bytes(b'\x00\x89\x02\x8a\x04\x05\x06\x07\x08\x83\x81\x0b\x00FE\x03\x04\x81\x82\x07\x80')
    }

    group_moves = ['RLFBUDrlfbudSMGCVE', 'RLFBrlfbSMGCVE', 'RLrlSMGCVE', 'SMGCVE']
    group_masks = [[[0x80], [0x00], [0x00]],
                   [[0x10], [0xC0], [0x00]],
                   [[0x0C], [0x06], [0x8F]],
                   [[0x0FF], [0xFF], [0x00]]]
    bit_masks = [bytes(group_mask[0] * 12 + group_mask[1] * 8 + group_mask[2]) for group_mask in group_masks]

    with open(os.path.join(os.getcwd(), 'rsc', 'thistle_tables.dat'), 'rb') as f:
        thistle_tables = pickle.load(f)

    def __init__(self, cube=None):

        edges = [0x10, 0x11, 0x12, 0x13, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]
        corners = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        parity = [0x00]
        if cube is None:
            self.cube = bytes(edges + corners + parity)
        else:
            self.cube = cube.cube

    def move_cube(self, moves):

        for m in moves:

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

    def solve(self):

        solution = ''
        temp_cube = ThistleCube(self)

        for group in range(0,4):

            if group > 0: solution = solution + '-'

            masked_cube = bytes([temp_cube.cube[i] & self.bit_masks[group][i] for i in range(0,21)])

            for moves, group_cube in self.thistle_tables[group].items():
                group_cube = bytes([group_cube[i] & self.bit_masks[group][i] for i in range(0,21)])
                if group_cube == masked_cube:
              #      print(moves)
                    solution = solution +  self.reverse(moves)
                    temp_cube.move_cube(temp_cube.reverse(moves))
              #      print('Group:', group, 'solution', self.reverse(moves), temp_cube.cube)

                    break






        return solution





