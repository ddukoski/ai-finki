from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # variables
    variables = list()

    for i in range(1, 5):
        for j in range(1, 5):
            variables.append((i, j))

    # domain
    domain = range(1, 17)
    problem.addVariables(variables, domain)

    problem.addConstraint(AllDifferentConstraint(), variables)

    # solve
    for i in range(1, 5):
        problem.addConstraint(AllDifferentConstraint(), [(j, i) for j in range(1, 5)])
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for j in range(1, 5)])
        problem.addConstraint(ExactSumConstraint(34), [(i, j) for j in range(1, 5)])
        problem.addConstraint(ExactSumConstraint(34), [(j, i) for j in range(1, 5)])

    solved = problem.getSolution()
    count = 0

    sorted_keys = sorted(solved.keys())

    for variable in sorted_keys:
        print(f"{variable.__str__():5} : " + f"{str(solved[variable]):5}", end=" ")
        count += 1
        if count == 4:
            count = 0
            print()
