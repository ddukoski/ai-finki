from searching_framework import Problem, breadth_first_graph_search


class Snake(Problem):

    def __init__(self, r_apples, initial, goal=None):
        super().__init__(initial, goal)
        self.r_apples = r_apples
        self.BOUND = 10
        self.directs = ('SvrtiLevo', 'ProdolzhiPravo', 'SvrtiDesno')

    def successor(self, state):
        '''
        We can go either left, forward or right, i.e., maximum 3 new states on the fringe

        We need node that the turning of the snake is done from its persective, instead of
        from the user looking at the matrix of squares
        '''

        s_states = dict()

        for direc in self.directs:
            res = self.move(state, direc)
            if res is not None:
                s_states[direc] = res

        return s_states

    def move(self, state, direction):
        n_state = list(state)
        return self.move_dir(n_state, direction)

    def move_dir(self, l_state, direction):
        snake_body = list(l_state[0])
        head_move = list(snake_body[-1])
        new_direction = l_state[-1]
        if l_state[-1] == 's':
            if direction == 'ProdolzhiPravo':
                head_move[1] -= 1
            if direction == 'SvrtiLevo':
                head_move[0] += 1
                new_direction = 'e'
            if direction == 'SvrtiDesno':
                head_move[0] -= 1
                new_direction = 'w'
        elif l_state[-1] == 'n':
            if direction == 'ProdolzhiPravo':
                head_move[1] += 1
            if direction == 'SvrtiLevo':
                head_move[0] -= 1
                new_direction = 'w'
            if direction == 'SvrtiDesno':
                head_move[0] += 1
                new_direction = 'e'
        elif l_state[-1] == 'e':
            if direction == 'ProdolzhiPravo':
                head_move[0] += 1
            if direction == 'SvrtiLevo':
                head_move[1] += 1
                new_direction = 'n'
            if direction == 'SvrtiDesno':
                head_move[1] -= 1
                new_direction = 's'
        elif l_state[-1] == 'w':
            if direction == 'ProdolzhiPravo':
                head_move[0] -= 1
            if direction == 'SvrtiLevo':
                head_move[1] -= 1
                new_direction = 's'
            if direction == 'SvrtiDesno':
                head_move[1] += 1
                new_direction = 'n'

        head_move = tuple(head_move)

        snake_body.append(head_move)

        if head_move not in l_state[1]:
            snake_body.pop(0)
        else:
            g_apples_rem = list(l_state[1])
            g_apples_rem.remove(head_move)
            l_state[1] = tuple(g_apples_rem)

        snake_body = tuple(snake_body)
        l_state[0] = snake_body
        l_state[2] = new_direction

        return tuple(l_state) if self.validate_move(head_move, snake_body[:-1]) else None

    def validate_move(self, moving, body_bef):
        body_bef = tuple(body_bef)
        if moving[0] == self.BOUND or moving[1] == self.BOUND \
                or moving[0] < 0 or moving[1] < 0 \
                or moving in self.r_apples \
                or moving in body_bef:
            return False

        return True

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return len(state[1]) == 0  # the goal is an empty tuple (see main)


if __name__ == '__main__':

    def read_apples():

        n = int(input())

        apples = list()

        while n != 0:
            pos = tuple(map(int, input().split(',')))
            apples.append(pos)
            n -= 1

        return apples


    """
    state format: 
    ((snake part 1, snake part 2, ..., snake part n+3), g_apples, green apples ,facing), where n is the num. of apples, and snake parts are tuples
    and facing is a string indicating where the snake is facing
    
    Crucial: green apples MUST BE IN STATE BECAUSE THEY CHANGE!
    """

    trail_init = ((0, 9), (0, 8), (0, 7))

    green_apples = tuple(read_apples())
    red_apples = tuple(read_apples())

    face = 's'

    init_state = (trail_init, green_apples, face)

    problem = Snake(red_apples, init_state, ())
    problem_solved = breadth_first_graph_search(problem)
    print(problem_solved.solution())
