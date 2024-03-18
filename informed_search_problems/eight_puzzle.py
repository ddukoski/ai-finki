from searching_framework import Problem, astar_search

"""
Примерен проблем од 4та ауд. вежба (прв проблем)
"""


class EightPuzzle(Problem):
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
        self.dirs = \
            {
                'left': -1,
                'right': 1,
                'up': -3,
                'down': +3
            }

    def successor(self, state):
        s_states = dict()
        for direct in self.dirs.keys():  # first try moving each plate
            for plate in state:
                res = self.move(state, plate, direct)
                if res is not None:
                    s_states[plate + ' ' + direct] = res

        return s_states

    def move(self, state, plate, direct):
        n_state = list(state)
        pos = state.index(plate)
        switch_w = pos + self.dirs[direct]

        if self.in_bounds(switch_w):
            n_state[pos], n_state[switch_w] = n_state[switch_w], n_state[pos]
        else:
            return None

        return "".join(n_state)

    def in_bounds(self, switch_idx):
        return not (switch_idx < 0 or switch_idx > 8)

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return super().goal_test(state)

    def h(self, node):
        """
        another less intuitive solution (but 3x faster) is using
        Manhattan  distance for each plate to its position
        """
        cmp = node.state
        out_of_place = 0
        for pair in zip(cmp, self.goal):
            if pair[0] != pair[1]:
                out_of_place += 1

        return out_of_place


if __name__ == '__main__':
    """
    state format: str, i.e., "*12345678" is our goal state, an ordered string
    and we will check how many numbers are out of place in our state,
    for example "*32415678" by comparing each letter 1 by one in the 
    heuristic function (h).
    """

    init_state = '*32485671'  # concrete example
    goal = '*12345678'

    problem = EightPuzzle(init_state, goal)
    solve = astar_search(problem)

    if solve is not None:
        print(solve.solution())
    else:
        print("No solution found")
