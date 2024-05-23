from data.kol_13_ds import dataset

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def accuracy(classifier1, classifier2, classifier3, test_x, test_y):
    c1_pred = classifier1.predict(test_x)
    c2_pred = classifier2.predict(test_x)
    c3_pred = classifier3.predict(test_x)

    correct_outer = 0

    for i in range(len(test_y)):
        correct_inner = 0

        if c1_pred[i] == test_y[i]:
            correct_inner += 1

        if c2_pred[i] == test_y[i]:
            correct_inner += 1

        if c3_pred[i] == test_y[i]:
            correct_inner += 1

        if correct_inner > 1:
            correct_outer += 1

    return correct_outer / len(test_y)


if __name__ == '__main__':
    x1, x2 = float(input()), float(input())

    datasets_idx_by_class = list()
    classes = set()

    for wine in dataset:
        classes.add(wine[-1])

    for _ in range(len(classes)):
        datasets_idx_by_class.append(list())

    for wine in dataset:
        datasets_idx_by_class[wine[-1]].append(wine)

    nb_train = []
    tree_train = []
    forest_train = []

    for class_set in datasets_idx_by_class:
        nb_train += class_set[:int(len(class_set) * x1)]

    for class_set in datasets_idx_by_class:
        tree_train += class_set[int(len(class_set) * x1): int(len(class_set) * x2)]

    for class_set in datasets_idx_by_class:
        forest_train += class_set[:int(len(class_set) * x2)]

    nb_train_X = [wine[:-1] for wine in nb_train]
    nb_train_Y = [wine[-1] for wine in nb_train]

    tree_train_X = [wine[:-1] for wine in tree_train]
    tree_train_Y = [wine[-1] for wine in tree_train]

    forest_train_X = [wine[:-1] for wine in forest_train]
    forest_train_Y = [wine[-1] for wine in forest_train]

    nbc = GaussianNB()
    dtc = DecisionTreeClassifier()
    rfc = RandomForestClassifier(n_estimators=3, random_state=0)

    nbc.fit(X=nb_train_X, y=nb_train_Y)
    dtc.fit(X=tree_train_X, y=tree_train_Y)
    rfc.fit(X=forest_train_X, y=forest_train_Y)

    test_set = list()

    for class_set in datasets_idx_by_class:
        test_set += class_set[int(len(class_set) * x2):]

    test_X = [wine[:-1] for wine in test_set]
    test_Y = [wine[-1] for wine in test_set]

    print(f'Tochnost: {accuracy(nbc, dtc, rfc, test_X, test_Y)}')
