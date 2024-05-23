from data.example_glass_1 import dataset

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def accuracy(classifier, test_x, test_y):
    predictions = classifier.predict(test_x)

    correct = 0

    for actual, pred in zip(test_y, predictions):
        if actual == pred:
            correct += 1

    return correct / len(test_y)


if __name__ == '__main__':
    n = int(input())
    max_leaves = int(input())  # for decision tree
    max_trees = int(input())  # for random forest

    training = dataset[n:]
    testing = dataset[:n]

    train_X = [compo[:-1] for compo in training]
    train_Y = [compo[-1] for compo in training]

    test_X = [compo[:-1] for compo in testing]
    test_Y = [compo[-1] for compo in testing]

    rfc_org = RandomForestClassifier(criterion='gini', n_estimators=max_trees, random_state=0)
    rfc_org.fit(X=train_X, y=train_Y)

    dtc = DecisionTreeClassifier(criterion='gini', max_leaf_nodes=max_leaves, random_state=0)
    dtc.fit(X=train_X, y=train_Y)

    importances = list(dtc.feature_importances_)
    best_attr = importances.index(max(importances))  # argmax

    dataset_dropped_col = [compo[:best_attr] + compo[best_attr + 1:] for compo in dataset]

    training = dataset_dropped_col[n:]
    testing = dataset_dropped_col[:n]

    train_X_rfc = [compo[:-1] for compo in training]
    train_Y_rfc = [compo[-1] for compo in training]

    test_X_rfc = [compo[:-1] for compo in testing]
    test_Y_rfc = [compo[-1] for compo in testing]

    scaler = StandardScaler()
    scaler.fit(train_X_rfc)

    train_X_rfc = scaler.transform(train_X_rfc)
    test_X_rfc = scaler.transform(test_X_rfc)

    rfc = RandomForestClassifier(criterion='gini', n_estimators=max_trees, random_state=0)
    rfc.fit(X=train_X_rfc, y=train_Y)

    from sklearn.metrics import accuracy_score

    old = accuracy_score(test_Y, rfc_org.predict(test_X))
    new = accuracy_score(test_Y, rfc.predict(test_X_rfc))

    print(f"Tochnost so originalnoto podatochno mnozhestvo: {old}")
    print(f"Tochnost so skalirani atributi: {new}")

    if new > old:
        print("Skaliranjeto na atributi ja podobruva tochnosta")
    if new < old:
        print("Skaliranjeto na atributi ne ja podobruva tochnosta")
    else:
        print("Skaliranjeto na atributi nema vlijanie")
