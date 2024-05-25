import numpy as np

from data.example_comparison_2_ds import dataset

from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def recall_custom_model(_classifiers, test_x, test_y, w):
    predictions_from_all = [_classifiers[0].predict(test_x),
                            _classifiers[1].predict(test_x),
                            _classifiers[2].predict(test_x),
                            _classifiers[3].predict(test_x)]

    final_pred = []

    for i in range(len(test_y)):
        zero = 0
        one = 0
        for j in range(4):
            if predictions_from_all[j][i] == 0:
                zero += w[j]
            else:
                one += w[j]

        final_pred.append(np.argmax([zero, one]))

    from sklearn.metrics import recall_score
    return recall_score(test_y, final_pred)


if __name__ == '__main__':
    x = int(input()) / 100

    neg_class = [data for data in dataset if data[-1] == 0]
    pos_class = [data for data in dataset if data[-1] == 1]

    coef_neg = int(len(neg_class) * x)
    coef_pos = int(len(pos_class) * x)

    training = neg_class[:coef_neg] + pos_class[:coef_pos]
    testing = neg_class[coef_neg:] + pos_class[coef_pos:]

    train_X = [data[:-1] for data in training]
    train_Y = [data[-1] for data in training]

    test_X = [data[:-1] for data in testing]
    test_Y = [data[-1] for data in testing]

    # 0 - nb, 1 - tree, 2 - forest, 3 - neural net
    index_mappings = {
        0: "Naive Bayes",
        1: "Decision Tree",
        2: "Random Forest",
        3: "MLP"
    }

    classifiers = [
        GaussianNB(),
        DecisionTreeClassifier(criterion='entropy', random_state=0),
        RandomForestClassifier(n_estimators=4, criterion='entropy', random_state=0),
        MLPClassifier(hidden_layer_sizes=10, activation='relu', learning_rate_init=0.001, random_state=0)
    ]

    classifier_scores = []

    for classifier in classifiers:
        classifier.fit(X=train_X, y=train_Y)
        pred = classifier.predict(test_X)

        classifier_scores.append(accuracy_score(test_Y, pred))

    weights = [1, 1, 1, 1]
    weights[np.argmax(classifier_scores)] += 1

    print(f"Najgolema tocnost ima klasifikatorot {index_mappings[np.argmax(classifier_scores)]}")

    print(f"Odzivot na kolekcijata so klasifikatori e {recall_custom_model(classifiers, test_X, test_Y, weights)}")
