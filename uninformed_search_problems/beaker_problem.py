from searching_framework import breadth_first_graph_search, Problem

"""
Проблем:
    Дадени се два сада J0 и J1 со капацитети C0 и C1 литри,
    соодветно. Да се доведат до состојба во која J0 има G0 литри,
    а J1 има G1 литри.
"""

class Beakers(Problem):

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)

    def successor(self, state):
        """
        :param state: Tuple[Tuple[int], Tuple[int]]
        :return: Dictionary
        """
        successor_states = dict()

        po_l = self.pour_out(state, 0)
        if po_l is not None:
            successor_states["empty_left"] = po_l

        po_r = self.pour_out(state, 1)
        if po_r is not None:
            successor_states["empty_right"] = po_r

        pfi_l_r = self.pour_from_into(state, 0, 1)
        if pfi_l_r is not None:
            successor_states["pour_from_left_to_right"] = pfi_l_r

        pfi_r_l = self.pour_from_into(state, 1, 0)  # not the same as above
        if pfi_r_l is not None:
            successor_states["pour_from_left_to_right"] = pfi_r_l

        return successor_states

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return super().goal_test(state)

    def pour_from_into(self, state, _from, _into):
        if state[0][_from] == 0:
            return None
        if state[0][_into] == state[1][_into]:  # max capacity
            return None

        s_mutate = list(state[0])
        s_mutate[_from] -= 1
        s_mutate[_into] += 1

        s_mutate = tuple(s_mutate)

        return s_mutate, state[1]

    def pour_out(self, state, beak):
        """
        :param state: Tuple[int]
        :param beak: int (0 ^ 1)
        :return: Tuple[int] - modif. state
        """
        if state[0][beak] == 0:
            return None

        l_state = list(state[0])
        l_state[beak] -= 1
        l_state = tuple(l_state)

        return l_state, state[1]


if __name__ == "__main__":
    """
     state format: ((4, 6), (cap1, cap2)) where xi = 4 yi = 6,
     telling which beaker is what quantity full, and cap1 and cap2 are according capacities
    """

    goal_state = tuple(map(int, input().split()))
    in_values = tuple(map(int, input().split()))
    capacity = tuple(map(int, input().split()))

    in_state = (in_values, capacity)

    problem = Beakers(initial=in_state,
                      goal=(goal_state,
                            capacity))

    """
     very important not to tree search, since we know it's possible to get repeating sequences of
     actions and get stuck in a loopy path (unless avoided by tree search)
    """
    node_sol = breadth_first_graph_search(problem=problem)

    print("Solution: " + node_sol.solution().__str__())
    print("Solve: " + node_sol.solve().__str__())
