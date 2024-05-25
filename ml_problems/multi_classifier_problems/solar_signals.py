import numpy as np

from data.solar_signal_data import data
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB


if __name__ == '__main__':
    classifiers = [
        GaussianNB(),
        RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=0),
        MLPClassifier(hidden_layer_sizes=50, activation='relu', learning_rate_init=0.001, random_state=0)
    ]

    mode, split = input(), int(input()) / 100

    neg_classes = list()
    pos_classes = list()

    training = list()
    testing = list()

    if mode == 'balanced':
        neg_classes = [signal for signal in data if signal[-1] == 0]
        pos_classes = [signal for signal in data if signal[-1] == 1]

        spl_neg = int(split * len(neg_classes))
        spl_pos = int(split * len(pos_classes))

        training = neg_classes[:spl_neg] + pos_classes[:spl_pos]
        testing = neg_classes[spl_neg:] + pos_classes[spl_pos:]
    else:
        spl_ds = int(split * len(data))
        training = data[:spl_ds]
        testing = data[spl_ds:]

    train_x = [signal[:-1] for signal in training]
    train_y = [signal[-1] for signal in training]

    test_x = [signal[:-1] for signal in testing]
    test_y = [signal[-1] for signal in testing]

    for classifier in classifiers:
        classifier.fit(X=train_x, y=train_y)

    score_map = {
        0: 'prviot',
        1: 'vtoriot',
        2: 'tretiot'
    }

    scores = list()

    from sklearn.metrics import precision_score, accuracy_score

    for classifier in classifiers:
        predictions = classifier.predict(test_x)
        scores.append(precision_score(y_true=test_y, y_pred=predictions))

    most_precise_classifier = np.argmax(scores)

    print(f"Najvisoka preciznost ima {score_map[most_precise_classifier]} klasifikator")

    preds_most_precise_classifier = classifiers[most_precise_classifier].predict(test_x)
    print(f"Negovata tochnost e {accuracy_score(test_y, preds_most_precise_classifier)}")
