from constraint import *

if __name__ == '__main__':
    problem = Problem(RecursiveBacktrackingSolver())

    # variables
    squares = list()

    for i in range(1, 9):
        for j in range(1, 9):
            squares.append((i, j))

    # domain
    domain = [0, 1]

    problem.addVariables(squares, domain)

    # solve
    for i in range(1, 9):
        problem.addConstraint(ExactSumConstraint(1), [(i, j) for j in range(1, 9)])
        problem.addConstraint(ExactSumConstraint(1), [(j, i) for j in range(1, 9)])

    solved = problem.getSolution()

    cb_files = {  # map the x coordinates into files (cols) from chess notation format
        1: 'a',
        2: 'b',
        3: 'c',
        4: 'd',
        5: 'e',
        6: 'f',
        7: 'g',
        8: 'h'
    }

    rook_descartes_coord = filter(lambda key: solved[key] == 1, solved.keys())
    rook_cb_coord = map(lambda tup: (cb_files[tup[0]], tup[1]), rook_descartes_coord)

    print(set(rook_cb_coord))
