from searching_framework.uninformed_search import *


class Molecules(Problem):
    def __init__(self, board, initial, goal=None):
        super().__init__(initial, goal)
        self.board = board
        self.limit_j = len(board[0]) - 1
        self.limit_i = len(board) - 1
        self.directions = {
            'right': (0, 1),
            'left': (0, -1),
            'up': (-1, 0),
            'down': (1, 0)
        }

    def successor(self, state):
        s_states = dict()

        for atom in range(3):
            for direction in self.directions:
                res = self.move(list(state[atom]), list(self.directions[direction]), depth=0)
                if res is None:
                    continue
                n_state = list(state)
                n_state[atom] = res
                n_state = tuple(n_state)
                if len(set(n_state)) != 3:  # careful! we are not checking whether we overlap
                    continue
                s_states[direction + ' ' + self.w_atom(atom)] = n_state

        return s_states

    def w_atom(self, num):
        if num == 0:
            return 'H1'
        if num == 1:
            return 'O'
        return 'H2'

    def move(self, atom, where, depth):
        if not self.validate_state(atom):
            if depth == 1:  # it's impossible to make a move
                return None
            return atom[0] - where[0], atom[1] - where[1]

        new_atom = [atom[0] + where[0], atom[1] + where[1]]

        return self.move(new_atom, where, depth + 1)

    def validate_state(self, atom):
        if atom[0] > self.limit_i \
                or atom[0] < 0 \
                or atom[1] > self.limit_j \
                or atom[1] < 0 \
                or self.board[atom[0]][atom[1]] == 1:
            return False

        return len(set())

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return (state[0][1] == state[1][1] - 1) \
            and (state[0][1] == state[2][1] - 2)


if __name__ == '__main__':
    '''
    in the board 1 is an obstacle, 0 is a free space
    
    state format: (posH1, posO, posH2)
    '''

    b = [  # concrete example
        [0, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0],
        [1, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    h1 = (0, 2)
    h2 = (5, 2)
    o = (4, 6)

    init_state = (h1, o, h2)
    print("start")
    problem = Molecules(b, init_state, ())
    solved = breadth_first_graph_search(problem)

    print(solved.path())
