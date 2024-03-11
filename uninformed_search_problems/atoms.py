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
        for direction in self.directions:
            for atom in range(3):
                transitioned = self.move(idx=atom, where=list(self.directions[direction]), depth=0, state=state)
                if transitioned is None:
                    continue
                print(str(atom) + ' ' + direction + " | before: " + str(state))
                s_states[direction] = transitioned

        return s_states

    def move(self, idx, where, depth, state):

        if not self.validate_state(state):
            if depth == 1:  # it's impossible to make a move
                return None
            else:
                new_state = list(state)
                new_state[idx] = (new_state[idx][0] - where[0], new_state[idx][1] - where[1])
                return tuple(new_state)

        new_atom = [state[idx][0] + where[0], state[idx][1] + where[1]]
        new_atom = tuple(new_atom)
        new_state = list(state)
        new_state[idx] = new_atom
        new_state = tuple(new_state)

        return self.move(idx, where, depth + 1, new_state)

    def validate_state(self, state):
        for atom in state:
            if atom[0] > self.limit_i \
                    or atom[0] < 0 \
                    or atom[1] > self.limit_j \
                    or atom[1] < 0 \
                    or self.board[atom[0]][atom[1]] == 1:
                return False

        if len(set(state)) != 3:
            return False

        return True

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        print(state)
        return state[0][1] == state[1][1] - 1 \
            and state[1][1] == state[2][1] - 1 \
            and state[0][0] == state[1][0] and state[1][0] == state[2][0]


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
    o = (4, 7)

    init_state = (h1, o, h2)
    print("start")
    problem = Molecules(b, init_state, ())
    solved = breadth_first_graph_search(problem)

    print(solved.path())
