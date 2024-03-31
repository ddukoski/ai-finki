from constraint import *


class MaxAssignmentConstraint:
    def __init__(self, val):
        self.val = val

    def __call__(self, *vals):
        """
        @param *vals: the assigment to the variables so far
        @return: bool, representing the constraint satisfaction elaborated below

        This method will impose a constraint that checks if less than 4
        appointments at the same time are concurrently assigned
        (ex. if T1 appears at most 4 times it would be okay, otherwise not)
        """
        frequency = 0

        for val in vals:
            if val == self.val:
                frequency += 1

        return frequency <= 4


if __name__ == '__main__':
    num = int(input())

    papers = dict()

    paper_info = input()
    while paper_info != 'end':
        title, topic = paper_info.split(' ')
        papers[title] = topic
        paper_info = input()

    # Tuka definirajte gi promenlivite

    domain = [f'T{i + 1}' for i in range(num)]

    variables = []

    for paper in papers.keys():
        variables.append(f'{paper} ({papers[paper]})')

    problem = Problem(BacktrackingSolver())

    # Dokolku vi e potrebno moze da go promenite delot za dodavanje na promenlivite
    problem.addVariables(variables, domain)

    # Tuka dodadete gi ogranichuvanjata

    [problem.addConstraint(MaxAssignmentConstraint(_val), variables) for _val in domain]

    for subject in papers.values():
        same = []
        for combo in variables:
            if subject in combo:
                same.append(combo)

        if len(same) <= 4:
            problem.addConstraint(AllEqualConstraint(), same)

    # Tuka dodadete go kodot za pechatenje
    solved = problem.getSolution()

    keys_iterate = ["Paper" + str(i) for i in range(1, 11)]
    skip = True
    for k in keys_iterate:
        for key_actl in solved.keys():
            if key_actl.startswith(k+" "):
                print(f'{key_actl}: {solved[key_actl]}')
