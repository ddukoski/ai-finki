from searching_framework import Problem, breadth_first_graph_search


"""
2-ра од колоквиумските задачи.
"""


class Hanoi(Problem):

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)

    def successor(self, state):
        s_states = dict()
        n = len(state)

        for i in range(n):
            for j in range(n):
                res = self.emplace(state, i, j)
                if res is not None:
                    s_states['MOVE TOP BLOCK FROM PILLAR ' + str(i+1) + ' TO PILLAR ' + str(j+1)] = res

        return s_states

    def emplace(self, state, i, j):
        if i == j:
            return None
        if len(state[i]) == 0:
            return None
        if len(state[j]) != 0 and state[i][-1] > state[j][-1]:
            return None

        # make state structure mutable
        pillars = list(state)
        pillars[i] = list(pillars[i])
        pillars[j] = list(pillars[j])

        # moving from pillar i to j
        pillars[j].append(pillars[i][-1])
        pillars[i].remove(pillars[i][-1])

        # internal lists back to tuples
        pillars[i] = tuple(pillars[i])
        pillars[j] = tuple(pillars[j])

        return tuple(pillars)

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return super().goal_test(state)


def create_pillars():
    pillars = input().split(";")

    idx = 0

    for i in range(len(pillars)):
        if len(pillars[i]) != 0:
            idx = i

    _initial = tuple(map(int, pillars[idx].split(',')))
    pillars = [tuple() for i in range(0, len(pillars))]
    pillars[idx] = _initial

    return tuple(pillars)


if __name__ == '__main__':

    _init = create_pillars()
    _goal = create_pillars()

    towers_hanoi = Hanoi(_init, _goal)
    solved = breadth_first_graph_search(towers_hanoi)
    if solved is not None:
        solution = solved.solution()
        print("Number of action " + str(len(solution)))
        print(solved.solution())
    else:
        print("No solution found.")
