from searching_framework import astar_search, Problem
import math


class Football(Problem):
    def __init__(self, forbid_ball, opponents, x_b, y_b, initial, goal=None):
        super().__init__(initial, goal)
        self.BOUND_Y = y_b
        self.BOUND_X = x_b
        self.directs = {
            'Pomesti coveche dolu': (0, -1),
            'Pomesti coveche desno': (1, 0),
            'Pomesti coveche dolu-desno': (1, -1),
            'Pomesti coveche gore-desno': (1, 1),
            'Pomesti coveche gore': (0, 1)
        }
        self.shooting = {
            'Turni topka gore': (0, 1),
            'Turni topka dolu': (0, -1),
            'Turni topka desno': (1, 0),
            'Turni topka gore-desno': (1, 1),
            'Turni topka dolu-desno': (1, -1)
        }
        self.opponents = opponents
        self.forbid_ball = forbid_ball

    def successor(self, state):
        s_states = dict()

        # initial=(human, ball)

        for direction in self.directs.keys():
            res = self.move(state, self.directs[direction])
            if res is not None:
                s_states[direction] = res

        for shoot in self.shooting.keys():
            h = list(state[0])
            b = list(state[1])

            h[0] += self.shooting[shoot][0]
            h[1] += self.shooting[shoot][1]
            if h == b:
                res = self.shoot(state, self.shooting[shoot])
                if res is not None:
                    s_states[shoot] = res
                    break

        return s_states

    def move(self, state, where):
        n_state = list(state)

        n_human = list(n_state[0])
        n_human[0] += where[0]
        n_human[1] += where[1]

        n_state[0] = tuple(n_human)
        n_state = tuple(n_state)

        return n_state if self.validate_state(n_state, 'human') else None

    def shoot(self, state, where):
        n_state = list(state)

        n_human = list(n_state[0])
        n_ball = list(n_state[1])

        if abs(n_human[0] - n_ball[0]) > 1 or abs(n_human[1] - n_ball[1]) > 1:
            return None

        n_human[0] += where[0]
        n_human[1] += where[1]

        n_ball[0] += where[0]
        n_ball[1] += where[1]

        n_state[0] = tuple(n_human)
        n_state[1] = tuple(n_ball)
        n_state = tuple(n_state)

        return n_state if self.validate_state(n_state, 'ball') else None

    def validate_state(self, state, validation_type):
        b = state[1]
        h = state[0]

        if validation_type == 'human':
            if b == h:
                return False

        if b in self.forbid_ball or \
                b in _opponents or \
                h in _opponents:
            return False

        if not (0 <= b[1] < self.BOUND_Y and 0 <= b[0] < self.BOUND_X) or \
                not (0 <= h[1] < self.BOUND_Y and 0 <= h[0] < self.BOUND_X):
            return False

        return True

    def h(self, node):
        _ball = node.state[1]

        first_goal = self.goal[0]
        second_goal = self.goal[1]

        # man_first = abs(_ball[0] - first_goal[0]) + abs(_ball[1] - first_goal[1])
        # man_second = abs(_ball[0] - second_goal[0]) + abs(_ball[1] - second_goal[1])

        euc1 = math.sqrt(math.pow((first_goal[0] - _ball[0]), 2) + math.pow((first_goal[1] - _ball[1]), 2))
        euc2 = math.sqrt(math.pow((second_goal[0] - _ball[0]), 2) + math.pow((second_goal[1] - _ball[1]), 2))

        return min(math.floor(euc1), math.floor(euc2))

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state[1] in self.goal


if __name__ == '__main__':
    x_bound = 8
    y_bound = 6

    human = tuple(map(int, input().split(',')))
    ball = tuple(map(int, input().split(',')))
    _goal = ((7, 2), (7, 3))
    _opponents = ((3, 3), (5, 4))
    _forbid_ball = (
        (2, 2), (2, 3), (2, 4), (3, 2), (4, 2), (3, 4), (4, 4), (4, 3), (4, 5), (5, 5), (6, 5), (6, 4), (6, 3), (5, 3)
    )
    problem = Football(forbid_ball=_forbid_ball,
                       opponents=_opponents,
                       x_b=x_bound, y_b=y_bound,
                       initial=(human, ball),
                       goal=_goal)

    solve = astar_search(problem)
    if solve is not None:
        print(solve.solution())
    else:
        "No solution found"
