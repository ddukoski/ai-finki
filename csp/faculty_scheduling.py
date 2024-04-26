from constraint import *


def space_two_hours(schedule1, schedule2):

    if schedule1[0:4] == schedule2[0:4]:
        time1 = int(schedule1[4:])
        time2 = int(schedule2[4:])

        return abs(time1 - time2) >= 2

    else:
        return True


def ml_time_disallow(schedule1, schedule2):

    time1 = int(schedule1[4:])
    time2 = int(schedule2[4:])

    return time1 != time2


def count_lectures(n, prob, subject, domain):

    l_ret = list()

    for keep in range(n):
        l_ret.append(f'{subject}_cas_{keep + 1}')
        prob.addVariable(f'{subject}_cas_{keep + 1}', domain)

    return l_ret


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    casovi_AI = int(input())
    casovi_ML = int(input())
    casovi_R = int(input())
    casovi_BI = int(input())

    AI_predavanja_domain = ["Mon_11", "Mon_12", "Wed_11", "Wed_12", "Fri_11", "Fri_12"]
    ML_predavanja_domain = ["Mon_12", "Mon_13", "Mon_15", "Wed_12", "Wed_13", "Wed_15", "Fri_11", "Fri_12", "Fri_15"]
    R_predavanja_domain = ["Mon_10", "Mon_11", "Mon_12", "Mon_13", "Mon_14", "Mon_15", "Wed_10", "Wed_11", "Wed_12",
                           "Wed_13", "Wed_14", "Wed_15", "Fri_10", "Fri_11", "Fri_12", "Fri_13", "Fri_14", "Fri_15"]
    BI_predavanja_domain = ["Mon_10", "Mon_11", "Wed_10", "Wed_11", "Fri_10", "Fri_11"]

    AI_vezbi_domain = ["Tue_10", "Tue_11", "Tue_12", "Tue_13", "Thu_10", "Thu_11", "Thu_12", "Thu_13"]
    ML_vezbi_domain = ["Tue_11", "Tue_13", "Tue_14", "Thu_11", "Thu_13", "Thu_14"]
    BI_vezbi_domain = ["Tue_10", "Tue_11", "Thu_10", "Thu_11"]

    # ---Tuka dodadete gi promenlivite--------------------

    variables = ["AI_vezbi", "ML_vezbi", "BI_vezbi"]

    variables += count_lectures(casovi_AI, problem, "AI", AI_predavanja_domain)
    variables += count_lectures(casovi_ML, problem, "ML", ML_predavanja_domain)
    variables += count_lectures(casovi_R, problem, "R", R_predavanja_domain)
    variables += count_lectures(casovi_BI, problem, "BI", BI_predavanja_domain)

    all_ml = list(
                filter(lambda x: x is not None, [sub if sub.__contains__("ML") else None for sub in variables])
                )

    problem.addVariable("AI_vezbi", AI_vezbi_domain)

    problem.addVariable("ML_vezbi", ML_vezbi_domain)

    problem.addVariable("BI_vezbi", BI_predavanja_domain)

    # ---Tuka dodadete gi ogranichuvanjata----------------

    for i in range(len(variables)):
        for j in range(i, len(variables)):
            if variables[i] != variables[j]:
                problem.addConstraint(space_two_hours, (variables[i], variables[j]))

    for i in range(len(all_ml)):
        for j in range(i, len(all_ml)):
            if all_ml[i] != all_ml[j]:
                problem.addConstraint(ml_time_disallow, (all_ml[i], all_ml[j]))

    # ----------------------------------------------------

    solution = problem.getSolution()

    print(solution)
