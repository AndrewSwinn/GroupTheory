
import copy
import itertools
from collections import deque
from itertools import permutations
import numpy as np


class Element:
    def __init__(self, name, number, permutation):
        self.name = name
        self.pretty_name = self._pretty_name(name)
        self.number = number
        self.permutation = permutation

    def __str__(self):
        return str(self.number) + " " + str(self.name) + " " + str(self.permutation)

    def __eq__(self, other):
        return self.permutation == other.permutation


    def re_number(self, offset):
        self.permutation = tuple([i + offset for i in self.permutation])

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

class ElementSet:
    def __init__(self, elements=[]):
        self.elements = elements

    def __str__(self):
        return [element.name for element in self.elements]

    def __iter__(self):
        return iter(self.elements)

    def __eq__(self, other):
        equal = True

        for element in self.elements:
            if element not in group.elements:
                equal = False
                break
        if equal:
            for element in group.elements:
                if element not in self.elements:
                    equal = False
                    break
        return equal

    def add(self, element):
        exists = True
        if element not in self.elements:
            self.elements.append(element)
            exists = False
        return exists




class Group:
    def __init__(self, **kwargs):

        generators = kwargs.get('generators')
        factors    = kwargs.get('factors')
        elements   = kwargs.get('elements')

        # Create elements (members) of the group
        if generators is not None:
            self.elements = self._generate_group(generators)
        elif factors is not None:
            self.elements = self._direct_product(factors)
        else: self.elements = elements



    def __eq__(self, group):

        #check that every element in 'self' maps to group, and vice versa
        self_permutations  = [element.permutation for element in self.elements]
        group_permutations = [element.permutation for element in group.elements]

        return self._bijection(self_permutations, group_permutations)


    def _bijection(self, permutations_1, permutations_2):
        equal = True
        for permutation in permutations_1:
            if permutation not in permutations_2:
                equal = False
                break
        if equal:
            for permutation in permutations_2:
                if permutation not in permutations_1:
                    equal = False
                    break
        return equal

    def _generate_group(self, generators):
        #create identity
        permute_length = 1
        for generator in generators.values():
            for cycle in generator:
                permute_length = max(permute_length, max(cycle))

        element_number = 1
        identity =  Element(name='e', number=element_number, permutation=tuple([i for i in range(1, permute_length + 1)]))

        self.elementset = ElementSet([identity])
        for generator_name, permute_cycles in generators.items():
            for element in self.elementset:
                pass


        group = [identity]
        new = True
        #keep applying generator until no new group members created:
        while new:
            new, new_members = False, []
            group_permutations = [element.permutation for element in group]
            for generator_name, permute_cycles in generators.items():
                for member in group:
                    member_name, member_permutation = member.name, member.permutation
                    new_permutation = self._apply(permute_cycles, member_permutation)
                    #Create new members as needed
                    if new_permutation not in group_permutations:
                        new = True
                        group_permutations.append(new_permutation)
                        new_name = (member_name + generator_name) .replace('e', '')
                        group.append(Element(name=new_name, number=element_number, permutation=new_permutation))
                        element_number += 1

        return group



    def _subgroup(self, elements):
        identity =  self.get_identity()
        subgroup = [identity]
        for start in subgroup:
            for element in elements:
                new_element = self.element_multiply(start, element)
                if new_element.number not in [element.number for element in subgroup]:
                    subgroup.append(new_element)
        return Group(elements = subgroup)

    def subgroups(self):
        self.subgroups = []
        for length in range(1, len(self.elements) + 1):
            for elements in itertools.combinations(self.elements, length):
                subgroup = self._subgroup(elements)
                if subgroup not in self.subgroups:
                    self.subgroups.append(subgroup)

    def _coset(self, multiplier, subgroup):
        coset = []
        for element in subgroup.elements:
            product = self.element_multiply(multiplier, element)
            coset.append(product)
        return coset

    def _cosets(self, subgroup):
        quotant, cosets = [], []
        for element in self.elements:
            coset = self._coset(element, subgroup)
            coset_permutations = [element.permutation for element in coset]
            new = True
            for existing in cosets:
                existing_permutation = [element.permutation for element in existing]
                new = True if new and self._bijection(coset_permutations, existing_permutation) is False else False
            if new:
                quotant.append(element)
                cosets.append(coset)

        return quotant, cosets

    def cosets(self, subgroup):
        return self._cosets(subgroup)[1]

    def quotant(self, subgroup):
        return self._cosets(subgroup)[0]


    def _apply(self, permute_cycles, member_permutation):
        working_permutation = list(member_permutation)
        new_permutation     = list(member_permutation)
        for permutation in permute_cycles:
            #print(permutation)
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

        for factor in factors[1:]:
            elements = []
            element_number = 1
            for factor_element in factor.elements:
                for element in base_elements:
                    new_name = element.name.replace('(', '')
                    new_name = new_name.replace(')', '')
                    new_name = '(' +  new_name + ',' +  factor_element.name + ')'
                    elements.append(Element(name         = new_name,
                                            number       = element_number,
                                            permutation  = element.permutation + factor_element.permutation))
                    element_number += 1
            base_elements = elements

        return elements

    def get_element(self, pretty_name):

        return [element for element in self.elements if element.pretty_name == pretty_name][0]

    def get_identity(self):
        return [element for element in self.elements if element.number == 1][0]






if __name__ == "__main__":

    A4 = Group(generators={'a': [(2,3,4)], 'b':[(1,2), (3,4)]})

    C3 = Group(generators={'r': [(1,2,3)]})
    C4 = Group(generators={'r': [(1,2,3,4)]})
    C5 = Group(generators={'r': [(1, 2, 3, 4, 5)]})
    C6 = Group(generators={'r': [(1, 2, 3, 4, 5, 6)]})
    C6.subgroups()

    C3C4 = Group(factors=[C3, C4, C5, C3])

    S3 = Group(generators={'a': [(1, 2, 3)], 'b': [(1, 2)]})

    A4.subgroups()
    print(len(A4.elements))
    for subgroup in A4.subgroups:
        quotant = A4.quotant(subgroup)
        print([element.name for element in subgroup.elements], [element.name for element in quotant] )









