from searching_framework import Problem, astar_search

"""
Задача 1 од колоквиумските.
"""


class Ghost(Problem):

    def __init__(self, bound, walls, initial, goal=None):
        super().__init__(initial, goal)
        self.bound = bound
        self.walls = walls
        self.directions = {
            "Gore ": (0, 1),
            "Desno ": (1, 0)
        }
        self.times = {
            "1": 1,
            "2": 2,
            "3": 3
        }

    def successor(self, state):
        s_states = dict()

        for direct in self.directions:
            for t in self.times:
                res = self.move(state, self.directions[direct], self.times[t])
                if res is not None:
                    s_states[direct + t] = res

        return s_states

    def move(self, state, where, t):
        n_state = list(state)
        n_state = (n_state[0] + where[0] * t, n_state[1] + where[1] * t)

        return n_state if self.validate_state(n_state) else None

    def validate_state(self, state):
        return state not in self.walls and (0 <= state[0] < self.bound) and (0 <= state[1] < self.bound)

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return super().goal_test(state)

    def h(self, node):
        s = node.state
        man_dist = abs(s[0] - self.goal[0]) + abs(s[1] - self.goal[1])
        return man_dist / 3


if __name__ == '__main__':
    maze_n = int(input())
    walls_n = int(input())
    walls_avoid = list()
    for i in range(walls_n):
        walls_avoid.append(tuple
                           (map(int, input().split(',')))
                           )

    walls_avoid = tuple(walls_avoid)

    ghost_problem = Ghost(maze_n, walls_avoid, (0, 0), (maze_n - 1, maze_n - 1))
    solved = astar_search(ghost_problem)

    if solved is not None:
        print(solved.solution())
    else:
        print("No solution")
