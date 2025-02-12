from collections import deque
import numpy as np


class Element:
    def __init__(self, name, number, permutations):
        self.name = name
        self.number = number
        self.permutations = permutations

    def __str__(self):

        return str(self.name) + "\t" +  str(self.number) + "\t" + str(self.permutations)



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

    def _direct_product(self,factors):

        base_elements = factors[0].elements

        for factor in factors[1:]:
            elements = []
            for factor_element in factor.elements:
                for element in base_elements:
                    elements.append(Element(name         = factor_element.name         + element.name,
                                            number       = factor_element.number       + element.number,
                                            permutations = factor_element.permutations + element.permutations))
            base_elements = elements

        return elements




    def _generate_group(self, generators):
        #create identity
        permute_length = 1
        for generator in generators.values():
            for cycle in generator:
                permute_length = max(permute_length, max(cycle))

        identity = Element(name=['e'], number=[1], permutations=[tuple([i for i in range(1, permute_length + 1)])])


        #create group (unsorted and unnumbered)
        group = [identity]
        new = True
        while new:
            new, new_members = False, []
            for member in group:
                member_name, member_permutation = member.name[0], member.permutations[0]
                for name, cycles in generators.items():
                    orig_permutation = list(member_permutation)
                    work_permutation = list(member_permutation)
                    new_name = (name + member_name).replace('e', '')
                    for cycle in cycles:
                        sublist = deque(cycle)
                        sublist.rotate(1)
                        for i, element in enumerate(sublist):
                            work_permutation[cycle[i] - 1] = orig_permutation[sublist[i] - 1]

                    if (tuple(work_permutation) not in [element.permutations[0] for element in group]) and (
                            tuple(work_permutation) not in [element.permutations for element in new_members]):
                        new_members.append(Element([new_name], [0],  [tuple(work_permutation)]))

            if len(new_members) > 0:
                new = True
                group = group + new_members

        #sort and number the elements (identity e is always 1).
        next = 2
        group.sort(key=lambda x: x.name)
        for element in group:
            if element.number != [1]:
                element.number = [next]
                next += 1
        group.sort(key=lambda x: x.number)

        return group

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





if __name__ == "__main__":

    C3 = Group(generators={'r': [(1,2,3)]})
    C4 = Group(generators={'r': [(1,2,3,4)]})
    C5 = Group(generators={'r': [(1,2,3,4,5)]})

    C3C4 = Group(factors=[C3, C4])
    C3C4C5 = Group(factors=[C3, C4, C5])

    print(len(C3C4.elements))
    
    for element in C3C4.elements:

        print(element)




    def multiplication_table(group):
        order = len(group.elements)
        table = np.zeros(shape=(order, order))

        for i in group.elements:
            for j in group.elements:
                product = group.element_multiply(i, j)
                print(i, j, product)
                table[i.number[0] - 1, j.number[0] - 1] = product.number[0]
        return table

    mult = multiplication_table(C3C4)




    print(mult)
