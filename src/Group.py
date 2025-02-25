
import copy
import itertools
from collections import deque
from itertools import permutations
import numpy as np


class Element:
    def __init__(self, name, permutation):
        self.name = name
        self.pretty_name = self._pretty_name(name)
        self.permutation = permutation

    def __str__(self):
        return str(self.name) + " " + str(self.permutation)

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

    def generate(self, generator_name, permute_cycles):
        working_permutation = list(self.permutation)
        new_permutation     = list(self.permutation)
        for permutation in permute_cycles:
            # print(permutation)
            # cycle has the elements of permutation cycled round once
            cycle = deque(permutation)
            cycle.rotate(1)
            for i, index in enumerate(permutation):
                new_permutation[cycle[i] - 1] = working_permutation[permutation[i] - 1]
        new_name = (self.name + generator_name).replace('e','')
        return Element(new_name, tuple(new_permutation))



class ElementSet:
    def __init__(self, elements=[]):
        self.elements = elements

    def __str__(self):
        return str([element.name for element in self.elements])

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __eq__(self, other):
        equal = True

        for element in self.elements:
            if element not in other.elements:
                equal = False
                break
        if equal:
            for element in other.elements:
                if element not in self.elements:
                    equal = False
                    break
        return equal

    def add(self, element):
        added = False
        if element not in self.elements:
            self.elements.append(element)
            added = True
        return added

    def multiply(self, element1, element2):

        new_permutation = tuple([element1.permutation[index-1] for index in element2.permutation])
        product_list = [element for element in self.elements if element.permutation == new_permutation]
        if len(product_list) == 1:
            return product_list[0]
        else:
            return None

    def set_multiply(self, element, elementset):
        prodset = ElementSet(elements=[])
        for element2 in elementset:
            product = self.multiply(element, element2)
            prodset.add(product)
        return prodset


    def get_identity(self):
        for element1 in self:
            identity = True
            for element2 in self:
                element3 = self.multiply(element1, element2)
                if element3 != element2:
                    identity is False
                    break
            if identity:
                return element1
        return None

    def is_closed(self):
        for element1 in self:
            for element2 in self:
                element3 = self.multiply(element1, element2)
                if element3 is None:
                    return False
        return True



class Group:
    def __init__(self, **kwargs):

        generators = kwargs.get('generators')
        factors    = kwargs.get('factors')
        elementset = kwargs.get('elementset')


        # Create elements (members) of the group
        if generators is not None:
            self.elementset = self._generate_group(generators)
        elif factors is not None:
            self.elementset = self._direct_product(factors)
        elif elementset is not None:
            self.elementset=  elementset
        else:
            print('Cannot create an empty group')

    def __len__(self):
        return len(self.elementset.elements)

    def __eq__(self, group):

        return self.elementset == group.elementset


    def _generate_group(self, generators):
        #create identity
        permute_length = 1
        for generator in generators.values():
            for cycle in generator:
                permute_length = max(permute_length, max(cycle))

        identity =  Element(name='e', permutation=tuple([i for i in range(1, permute_length + 1)]))

        elementset = ElementSet([identity])

        new_count = 1
        while new_count != 0:
            new_count = 0
            for generator_name, permute_cycles in generators.items():
                for element in elementset:
                    new_element = element.generate(generator_name, permute_cycles)
                    new_count += elementset.add(new_element)

        return elementset

    def _direct_product(self, factors):

        #take a copy of each of the factors and renumber the permutation elements so they don't overlap
        factors = [copy.deepcopy(factor) for factor in factors]
        permute_offset = 0
        for factor in factors:
            for element in factor.elementset:
                element.re_number(permute_offset)
            permute_offset += len(factor.elementset.elements[0].permutation)

        base_elementset = factors[0].elementset
        for factor in factors[1:]:
            elementset = ElementSet(elements=[])
            for factor_element in factor.elementset:
                for element in base_elementset:
                    new_name = element.name.replace('(', '')
                    new_name = new_name.replace(')', '')
                    new_name = '(' +  new_name + ',' +  factor_element.name + ')'
                    new_element = Element(new_name, element.permutation + factor_element.permutation)
            base_elementset = copy.deepcopy(elementset)

        return elementset

    def get_identity(self):
        return self.elementset.get_identity()

    def _subgroup(self, elements):
        subset = ElementSet(elements=[])
        identity =  self.get_identity()
        subset.add(identity)

        new_count = 1
        while new_count != 0:
            new_count  = 0
            for element1 in subset:
                for element2 in elements:
                    new_element = self.element_multiply(element1, element2)
                    new_count += subset.add(new_element)
        return subset

    def subgroups(self):
        subgroups = []
        for length in range(1, len(self) + 1):
            for elements in itertools.combinations(self.elementset, length):
                subgroup = self._subgroup(elements)
                if subgroup not in subgroups:
                   subgroups.append(subgroup)
        return subgroups


    #TODO ALMOST !!!
    def quotient(self, subgroup):
        quotient, cosets = ElementSet(elements=[]), []
        for element in self.elementset:
            coset = self.elementset.set_multiply(element, subgroup.elementset)

            if coset not in cosets:
                cosets.append(coset)
                quotient.add(element)

        return quotient






    # Takes 2 elements of the group, multiplies them together and returns the product
    def element_multiply(self, element1, element2):

        return self.elementset.multiply(element1, element2)



if __name__ == "__main__":

    A4 = Group(generators={'a': [(2,3,4)], 'b':[(1,2), (3,4)]})

    C3 = Group(generators={'r': [(1,2,3)]})
    C4 = Group(generators={'r': [(1,2,3,4)]})
    C5 = Group(generators={'r': [(1, 2, 3, 4, 5)]})
    C6 = Group(generators={'r': [(1, 2, 3, 4, 5, 6)]})
        #
    C3C4 = Group(factors=[C3, C4, C3, C5])
    #
    S3 = Group(generators={'a': [(1, 2, 3)], 'b': [(1, 2)]})

    group = A4
    for elementset in group.subgroups():
        subgroup = Group(elementset=elementset)
        quotient = group.quotient(subgroup)
        quot_identity = quotient.get_identity()
        print(subgroup.elementset, quotient, quot_identity.name, quotient.is_closed())



    print(len(C3C4.elementset))
    print(C3C4.get_identity())


