from collections import deque
import copy

from itertools import permutations

import numpy as np


class Element:
    def __init__(self, name, number, permutation):
        self.name = name
        self.number = number
        self.permutation = permutation

    def __str__(self):
        return str(self.name) + str(self.permutation)

    def re_number(self, offset):
        self.permutation = tuple([i + offset for i in self.permutation])



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

        new_permutation = tuple([element1.permutation[index-1] for index in element2.permutation])

        return [element for element in self.elements if element.permutation == new_permutation][0]



    def _direct_product(self, factors):

        #take a copy of each of the factors and renumber the permutation elements so they don't overlap
        factors = [copy.deepcopy(factor) for factor in factors]
        permute_offset = 0
        for factor in factors:
            for element in factor.elements:
                element.re_number(permute_offset)

            permute_offset += len(factor.elements[0].permutation)

        base_elements = factors[0].elements

        element_number = 1
        for factor in factors[1:]:
            elements = []
            for factor_element in factor.elements:
                for element in base_elements:
                    elements.append(Element(name         = element.name + ':' +  factor_element.name   ,
                                            number       = element_number,
                                            permutation  = element.permutation + factor_element.permutation))
                    element_number += 1
            base_elements = elements

        return elements

    def get_element(self, pretty_name):

        return [element for element in self.elements if self._pretty_name(element.name) == pretty_name][0]




if __name__ == "__main__":

    C3 = Group(generators={'r': [(1,2,3)]})
    C4 = Group(generators={'r': [(1,2,3,4)]})
    C5 = Group(generators={'r': [(1, 2, 3, 4, 5)]})

    C3C4 = Group(factors=[C3, C4, C5, C3])
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

    for i, element in enumerate(C3C4.elements):
        print(i, C3C4._pretty_name(element.name), element.number, element.permutation)

    e1 = C3C4.get_element(pretty_name='r2:r3:r4:r2' )
    e2 = C3C4.get_element(pretty_name='r2:e:e:e' )

    prod = C3C4.element_multiply(e1, e2)

    print(prod)
