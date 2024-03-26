from constraint import *

"""
Потребно е да се закаже состанок во петок за Марија, Петар и Симона. Симона како менаџер мора да присуствува на 
состанокот со најмалку уште една личност. Состанокот трае еден час, и може да се закаже во периодот од 12:00 до 20:00.
Почетокот на состанокот може да биде на секој час, односно состанокот може да почне во 12:00, но не во 12:05, 12:10 итн.
За секој од членовите дадени се времињата во кои се слободни:

Симона слободни термини: 13:00-15:00, 16:00-17:00, 19:00-20:00
Марија слободни термини: 14:00-16:00, 18:00-19:00
Петар слободни термини: 12:00-14:00, 16:00-20:00

Потребно е менаџерот Симона да ги добие сите можни почетни времиња за состанокот. Даден е почетен код со кој 
е креирана класа за претставување на проблемот, на кој се додадени променливите. Потоа се повикува наоѓање на решение
со BacktrackingSolver. Ваша задача е да ги додадете домените на променливите, како и да ги додадете ограничувањата
(условите) на проблемот.
"""


def at_least_one_equal(v1, v2, v3):  # custom constraint
    return (v1 == v2) or (v1 == v3)


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    simona = {13, 14, 16, 19}
    marija = {14, 15, 18}
    petar = {12, 13, 16, 17, 18, 19}

    problem.addVariable("Marija_prisustvo", list(marija))
    problem.addVariable("Simona_prisustvo", list(simona))
    problem.addVariable("Petar_prisustvo", list(petar))
    problem.addVariable("vreme_sostanok", range(12, 21))

    problem.addConstraint(AllEqualConstraint(), ["Simona_prisustvo", "vreme_sostanok"])
    problem.addConstraint(at_least_one_equal, ["Simona_prisustvo", "Marija_prisustvo", "Petar_prisustvo"])

    sol_set = set()  # used modify to fit only 1 and 0 for attendance

    for sol in problem.getSolutions():
        vals = list(sol.values())
        if vals[0] == vals[2]:
            vals[2] = 1
        else:
            vals[2] = 0
        if vals[0] == vals[3]:
            vals[3] = 1
        else:
            vals[3] = 0

        vals[0] = 1

        solution = dict()
        vals = tuple(vals)

        if vals not in sol_set:  # wtf ?
            sol_set.add(vals)
            solution["Simona_prisustvo"] = vals[0]
            solution["Marija_prisustvo"] = vals[2]
            solution["Petar_prisustvo"] = vals[3]
            solution["vreme_sostanok"] = vals[1]
            print(solution)
