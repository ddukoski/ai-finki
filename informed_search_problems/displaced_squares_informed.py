from searching_framework import Problem, astar_search

"""
7-ма од колоквиумските задачи.
"""

class Squares(Problem):

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
        self.directions = {
            "gore": (0, 1),
            "dolu": (0, -1),
            "levo": (-1, 0),
            "desno": (1, 0)
        }

    def goal_test(self, state):
        return state == self.goal

    @staticmethod
    def check_valid(state):
        for x, y in state:
            if x < 0 or x > 4 or y < 0 or y > 4:
                return False
        return True

    def successor(self, state):
        s_states = dict()

        for sq in range(5):
            for direc in self.directions:
                res = self.displ(state, sq, self.directions[direc])

                if res is not None:
                    s_states[f'Pomesti kvadratche {sq + 1} {direc}'] = res

        return s_states

    def displ(self, state, sq, where):
        n_state = list(state)
        sq_moving = state[sq]
        n_state[sq] = (sq_moving[0] + where[0], sq_moving[1] + where[1])

        n_state = tuple(n_state)

        return n_state if Squares.check_valid(n_state) else None

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]


if __name__ == '__main__':
    # ((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5))

    initial_state = tuple()

    for _ in range(5):
        initial_state += (tuple(map(int, input().split(','))),)

    goal_state = ((0, 4), (1, 3), (2, 2), (3, 1), (4, 0))

    squares = Squares(initial_state, goal_state)
    solved = astar_search(squares)

    if solved is not None:
        print(solved.solution())
    else:
        print("No solution found.")