from constraint import Problem, RecursiveBacktrackingSolver


def not_equal_colors(c1, c2):
    return c1 != c2


if __name__ == '__main__':
    problem = Problem(RecursiveBacktrackingSolver())
    # step 1 is to define the state, i.e., variables
    variables = ["WA", "NT", "T", "SA", "Q", "NSW", "V"]
    # step 2 is to define the domain, i.e., the values the variables can take on
    domain = ["red", "green", "blue"]

    problem.addVariables(variables, domain)

    australia_graph = {  # COMMUTATIVE graph representation of the bordering territories in Australia
        "WA": ["NT", "SA"],
        "NT": ["Q", "SA"],
        "Q": ["NSW"],
        "NSW": ["V"],
        "SA": ["Q", "NSW", "V"],
        "T": []
    }

    for key in australia_graph.keys():
        for bordering in australia_graph[key]:
            # constrain each arc in the graph
            problem.addConstraint(lambda a, b: a != b, (key, bordering))

    solved = problem.getSolution()
    print(solved)
