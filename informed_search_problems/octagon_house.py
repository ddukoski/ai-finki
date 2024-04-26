from searching_framework import Problem, astar_search


class OctagonPath(Problem):

    def __init__(self, octagons, initial, goal=None):
        super().__init__(initial, goal)
        self.octagons = octagons
        self.bound_x = 5
        self.bound_y = 9
        self.human_dirs = {
            "Gore": (0, 1),
            "Gore-desno": (1, 1),
            "Gore-levo": (-1, 1),
            "Stoj": (0, 0)
        }
        self.times = {
            " 2": 2,
            " 1": 1
        }

    def successor(self, state):
        s_states = dict()

        for direc in self.human_dirs.keys():
            for t in self.times.keys():
                res = self.move_human(state, self.human_dirs[direc], self.times[t])
                if res is not None:
                    if direc == "Stoj":
                        s_states[direc] = res
                        break
                    s_states[direc + t] = res

        return s_states

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def validate_human_pos(self, moved_human, house):

        return moved_human == house[0] or (
                (0 <= moved_human[0] < self.bound_x and 0 <= moved_human[1] < self.bound_y)
                and moved_human in self.octagons)

    def move_human(self, state, where, t):
        n_state = list(state[0])

        n_state[0] += where[0] * t
        n_state[1] += where[1] * t

        n_house = self.move_house(state)

        n_state = (tuple(n_state), n_house)
        if self.validate_human_pos(n_state[0], n_house):
            return n_state

        return None

    def move_house(self, state):
        house = list(state[1])

        moved_tup = list(house[0])

        if not (0 <= moved_tup[0] + house[1] < self.bound_x):
            house[1] *= -1
            moved_tup[0] += 1 * house[1]
        else:
            moved_tup[0] += house[1]

        moved_tup = tuple(moved_tup)

        house = (moved_tup, house[1])

        return house

    def goal_test(self, state):
        return state[0] == state[1][0]

    def h(self, node):
        """
            we are using distance to the top and dividing by 2 since it is the most optimal way in which the
            person can get to the house (it is above him in the best case scenario)

            we can also make a heuristic on how much we would have to wait if we reached the top, but it's
            more complex and this is enough
        """
        s = node.state
        human = s[0]
        return (8 - human[1]) // 2


if __name__ == '__main__':
    """
        state format: (human, house) - both are tuples, and only dynamic elements in the problem
                house = ((x, y), dir_x)
                human = (x, y)
    """

    allowed = ((1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (0, 2), (2, 2), (4, 2), (1, 3), (3, 3), (4, 3), (0, 4), (2, 4),
               (2, 5), (3, 5), (0, 6), (2, 6), (1, 7), (3, 7))

    human_start = tuple(map(int, input().split(',')))
    house_init = tuple(map(int, input().split(',')))

    house_start = list()
    house_start.append(house_init)
    house_start.append(-1)

    if input() == "desno":
        house_start[1] = 1

    house_start = tuple(house_start)

    octagon_path = OctagonPath(allowed, (human_start, house_start), ())
    path_solved = astar_search(octagon_path)

    if path_solved is not None:
        print(path_solved.solution())
    else:
        print("No solution")
