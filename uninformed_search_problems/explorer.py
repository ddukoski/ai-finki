from searching_framework.uninformed_search import *


"""
Проблем 1 од трета аудиториска аудиториска ( потребна е и слика, и мака ми е ! :-) )
"""


class Explorer(Problem):

    def __init__(self, boundary_x, boundary_y, initial, goal=None):
        super().__init__(initial, goal)
        self.boundary_x = boundary_x - 1
        self.boundary_y = boundary_y - 1
        self.b1_dir = 1  # going down
        self.b2_dir = -1  # going up

    def successor(self, state):
        suc_states = dict()

        """
        naming meaning: displ - displacement; l - left; r - right ...
        """

        l_displ = self.move((0, -1), state)
        if l_displ is not None:
            suc_states["left"] = l_displ
        r_displ = self.move((0, 1), state)
        if r_displ is not None:
            suc_states['right'] = r_displ
        d_displ = self.move((1, 0), state)
        if d_displ is not None:
            suc_states['down'] = d_displ
        u_displ = self.move((-1, 0), state)
        if u_displ is not None:
            suc_states['up'] = u_displ

        print(suc_states)

        return suc_states

    def goal_test(self, state):
        return state[0] == self.goal

    def actions(self, state):
        return self.successor(state)

    def result(self, state, action):
        return self.successor(state)[action]

    def move(self, where, state):
        moved_exp = list(state[0])
        moved_exp[0] += where[0]
        moved_exp[1] += where[1]

        block1_move = list(state[1])
        block2_move = list(state[2])

        if moved_exp[0] > self.boundary_y or moved_exp[0] < 0 or \
                moved_exp[1] > self.boundary_x or moved_exp[1] < 0:
            return None

        if moved_exp == block1_move or moved_exp == block2_move:
            return None

        moved_blocks_pos = self.move_blocks(block1_move, block2_move)

        return tuple(moved_exp), moved_blocks_pos[0], moved_blocks_pos[1]

    def move_blocks(self, b1, b2):

        # if one block reaches a boundary, then the other one surely has too

        if (b1[0] == self.boundary_y and self.b1_dir == 1) \
                or (b1[0] == 0 and self.b1_dir == -1):
            self.b1_dir *= -1
            self.b2_dir *= -1
            return (b1[0] + (2 * self.b1_dir), b1[1]), (b2[0] + (2 * self.b2_dir), b2[1])

        return (b1[0] + self.b1_dir, b1[1]), (b2[0] + self.b2_dir, b2[1])


if __name__ == '__main__':
    """
    state format: (explorer position, block1 position, block2 position)
    all positions will be ordered pairs of x,y coordinates in a matrix
    """
    limit_i = int(input())
    limit_j = int(input())
    house_coord = tuple(map(int, input().split()))  # goal state of explorer
    exp_start = tuple(map(int, input().split()))
    block1, block2 = (0, 2), (limit_i - 1, 4)  # constants are used in favor of brevity

    init_state = (exp_start, block1, block2)

    to_solve = Explorer(boundary_x=limit_j, boundary_y=limit_i, initial=init_state, goal=house_coord)

    solved_node = breadth_first_graph_search(to_solve)

    print(solved_node.solution())
