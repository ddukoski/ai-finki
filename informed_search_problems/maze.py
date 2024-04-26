import math

from searching_framework import Problem, astar_search


class Maze(Problem):

    def __init__(self, bound, illegal, initial, goal=None):
        super().__init__(initial, goal)
        self.direction = {
            "Gore": (0, 1),
            "Dolu": (0, -1),
            "Desno": (1, 0),
            "Levo": (-1, 0)
        }
        self.mv_times = {
            "": 1,
            " 2": 2,
            " 3": 3
        }
        self.illegal = illegal
        self.bound = bound

    def successor(self, state):
        s_states = dict()

        for direc in self.direction.keys():
            stop = False
            for times in self.mv_times.keys():
                if direc == "Desno":
                    if times == "":
                        continue
                    else:
                        if (state[0] + 1, state[1]) in self.illegal:
                            stop = True
                elif direc != "Desno" and times != "":
                    continue

                if not stop:
                    res = self.move(state, self.direction[direc], self.mv_times[times])
                    if res is not None:
                        s_states[direc + times] = res
                    else:
                        stop = True

        return s_states

    def move(self, state, where, t):
        n_state = list(state)

        n_state[0] += where[0] * t
        n_state[1] += where[1] * t

        n_state = tuple(n_state)

        return n_state if self.validate_state(n_state) else None

    def validate_state(self, state):
        if not (0 <= state[0] < self.bound) or not (0 <= state[1] < self.bound):
            return False

        if state in self.illegal:
            return False

        return True

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return super().goal_test(state)

    def h(self, node):
        s = node.state
        man_dist = abs(s[0] - self.goal[0]) + abs(s[1] - self.goal[1])
        return man_dist / 3


if __name__ == '__main__':
    map_size = int(input())
    n_walls = int(input())
    illegal_pos = list()
    for i in range(n_walls):
        pos = tuple(map(int, input().split(',')))
        illegal_pos.append(pos)

    illegal_pos = tuple(illegal_pos)
    human = tuple(map(int, input().split(',')))
    house = tuple(map(int, input().split(',')))

    maze = Maze(map_size, illegal_pos, human, house)
    solve_maze = astar_search(maze)
    if solve_maze is None:
        print("Nema reshenie!")
    else:
        print(solve_maze.solution())
