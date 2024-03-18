from searching_framework import Problem, astar_search

"""
Проблем 3 од 4та ауд.
"""


class Farmer(Problem):
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
        self.entities = \
            {
                "farmer": 0,
                "jare": 1,
                "volk": 2,
                "zelka": 3
            }

    def successor(self, state):
        s_states = dict()

        for entity in self.entities.keys():
            res = self.transfer(state, self.entities[entity])
            if res is not None:
                s_states["Farmer_nosi_" + entity] = res

        print(s_states)
        return s_states

    def transfer(self, state, entity):
        n_state = list(state)
        if n_state[0] == n_state[entity]:
            if n_state[0] == 'w':
                n_state[0] = 'e'
                n_state[entity] = 'e'
            else:
                n_state[0] = 'w'
                n_state[entity] = 'w'

        n_state = tuple(n_state)

        return n_state if self.validate_state(n_state) else None

    def validate_state(self, state):
        if state[0] != state[1] and \
                (state[1] == state[3] or state[1] == state[2]):
            return False
        return True

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return super().goal_test(state)

    def h(self, node):
        hamming_dist = 0
        for pair in zip(node.state, self.goal):
            if pair[0] != pair[1]:
                hamming_dist += 1

        return hamming_dist


if __name__ == '__main__':
    """
    state format: ('w', 'w', 'e', 'w'), where w/e are west and east
    the goal is to get all to ('e', 'e', 'e', 'e')
    Let state[0] = farmer
    Let state[1] = goat
    Let state[2] = wolf
    let state[3] = cabbage
    """
    goal = ('e', 'e', 'e', 'e')
    init_state = ('w', 'w', 'w', 'w')

    problem = Farmer(init_state, goal)
    solve = astar_search(problem)

    if solve is not None:
        print(solve.solution())
    else:
        print("No solution found")
