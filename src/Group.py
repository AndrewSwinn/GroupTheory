from collections import deque


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

        if generators is not None:
            self.elements = self._generate_group(generators)

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

        identity = Element(name=['e'], number=1, permutation=[tuple([i for i in range(1, permute_length + 1)])])


        #create group (unsorted and unnumbered)
        group = [identity]
        new = True
        while new:
            new, new_members = False, []
            for member in group:
                member_name, member_permutation = member.name[0], member.permutation[0]
                for name, cycles in generators.items():
                    orig_permutation = list(member_permutation)
                    work_permutation = list(member_permutation)
                    new_name = (name + member_name).replace('e', '')
                    for cycle in cycles:
                        sublist = deque(cycle)
                        sublist.rotate(1)
                        for i, element in enumerate(sublist):
                            work_permutation[cycle[i] - 1] = orig_permutation[sublist[i] - 1]

                    if (tuple(work_permutation) not in [element.permutation[0] for element in group]) and (
                            tuple(work_permutation) not in [element.permutation for element in new_members]):
                        new_members.append(Element([new_name], 0,  [tuple(work_permutation)]))

            if len(new_members) > 0:
                new = True
                group = group + new_members

        #sort and number the elements (identity e is always 1).
        next = 2
        group.sort(key=lambda x: x.name)
        for element in group:
            if element.number != 1:
                element.number = next
                next += 1
        group.sort(key=lambda x: x.number)

        return group

    # Takes 2 elements of the group, multiplies them together and returns the product
    def element_multiply(self, element1, element2):
        perm1, perm2 = list(element1.permutation), list(element2.permutation)
        result = tuple([perm1[i - 1] for i in perm2])
        for element in self.elements:
            if element.permutation == result:
                return element





if __name__ == "__main__":

    g = Group(generators={'r': [(1,2,3,4,5,6)], 'f':[(2,6),(3,5)]})

    for e in g.elements:
        print(e, e.number, e.permutation)



    #print(g.element_multiply('f', 'f'))
