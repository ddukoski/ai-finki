from constraint import *

def sol(board, problem):
    if not problem.getSolutions():
        return None

    for solution in problem.getSolutions():
        for (row, col), value in solution.items():
            board[row][col] = value

    return board

def solve_sudoku(board):
    problem = Problem(RecursiveBacktrackingSolver())

    cells = [(row, col) for row in range(9) for col in range(9)]
    problem.addVariables(cells, range(1, 10))

    for i in range(9):
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for j in range(9)])
        problem.addConstraint(AllDifferentConstraint(), [(j, i) for j in range(9)])

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            problem.addConstraint(AllDifferentConstraint(), [(row + i, col + j) for i in range(3) for j in range(3)])

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                problem.addConstraint(lambda cell, value=board[row][col]: cell == value, [(row, col)])

    return sol(board, problem)


if __name__ == '__main__':
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    solved_board = solve_sudoku(board)
    for row in solved_board:
        for cell in row:
            print(f'{cell}  ', end="")

        print()
