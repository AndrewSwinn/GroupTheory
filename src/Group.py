from collections import deque
from itertools import permutations

import numpy as np


class Element:
    def __init__(self, name, number, permutation):
        self.name = name
        self.number = number
        self.permutation = permutation

    def __str__(self):

        return str(self.name)



class Group:
    def __init__(self, **kwargs):

        generators = kwargs.get('generators')
        factors    = kwargs.get('factors')

        if generators is not None:
            self.elements = self._generate_group(generators)

        elif factors is not None:
            self.elements = self._direct_product(factors)

    def _pretty_name(self, name):
        pretty_name = ''
        prior, count = '', 1
        for action in name:
            if action != prior:
                if count > 1: pretty_name += str(count)
                pretty_name += action
                prior, count = action, 1
            else:
                count = count + 1
        if count > 1:
            pretty_name += str(count)

        return pretty_name

    def _generate_group(self, generators):
        #create identity
        permute_length = 1
        for generator in generators.values():
            for cycle in generator:
                permute_length = max(permute_length, max(cycle))

        element_number = 1
        identity =  Element(name='e', number=element_number, permutation=tuple([i for i in range(1, permute_length + 1)]))
        element_number += 1

        group = [identity]
        new = True

        #keep applying generator until no new group members created:
        while new:
            new, new_members = False, []
            group_permutations = [element.permutation for element in group]
            for generator_name, permutations in generators.items():
                for member in group:
                    member_name, member_permutation = member.name, member.permutation
                    new_permutation = self._apply(permutations, member_permutation)
                    #Create new members as needed
                    if new_permutation not in group_permutations:
                        new = True
                        group_permutations.append(new_permutation)
                        new_name = (member_name + generator_name) .replace('e', '')
                        group.append(Element(name=new_name, number=element_number, permutation=new_permutation))
                        element_number += 1

        return group

    def _apply(self, permutations, member_permutation):
        working_permutation = list(member_permutation)
        new_permutation     = list(member_permutation)
        for permutation in permutations:
            #cycle has the elements of permutation cycled round once
            cycle = deque(permutation)
            cycle.rotate(1)
            for i, index in enumerate(permutation):
                new_permutation[cycle[i] - 1] = working_permutation[permutation[i] - 1]
        return tuple(new_permutation)



    # Takes 2 elements of the group, multiplies them together and returns the product
    def element_multiply(self, element1, element2):
        permutations1, permutations2 = element1.permutations, element2.permutations
        result = []
        for i, perm1 in enumerate(permutations1):
            perm2 = permutations2[i]
            result.append(tuple([perm1[i - 1] for i in perm2]))
        for element in self.elements:
            for i, permutation in enumerate(element.permutations):
                if permutation == result[i]:
                    return element

    def _direct_product(self, factors):

        for group in factors:
            pass

        for factor in factors[1:]:
            for factor_element in factor.elements:
                for element in base.elements:
                    pass




if __name__ == "__main__":

    C3 = Group(generators={'r': [(1,2,3)]})
    C4 = Group(generators={'r': [(1,2,3,4)]})

    #C3C4 = Group(factors=[C3, C4])
    #
    #
    #
    # def multiplication_table(group):
    #     order = len(group.elements)
    #     table = np.zeros(shape=(order, order))
    #
    #     for i in group.elements:
    #         for j in group.elements:
    #             product = group.element_multiply(i, j)
    #             table[i.number[0] - 1, j.number[0] - 1] = product.number[0]
    #     return table
    #
    #
    # mult = multiplication_table(C4)
    #
    #

    for i, element in enumerate(C4.elements):
        print(i, C4._pretty_name(element.name), element.number, element.permutation)
