from data.solar_signal_data import data

from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

if __name__ == '__main__':
    model, col_rem = input(), int(input())

    classifier = None
    if model == 'NB':
        classifier = GaussianNB()
    else:
        classifier = MLPClassifier(hidden_layer_sizes=50 ,activation='relu', learning_rate_init=0.001, random_state=0)

    neg_data = [signal for signal in data if signal[-1] == 0]
    pos_data = [signal for signal in data if signal[-1] == 1]

    p1 = neg_data[:int(0.25 * len(neg_data))] + pos_data[:int(0.25 * len(pos_data))]
    p2 = neg_data[int(0.25 * len(neg_data)):int(0.5 * len(neg_data))] + pos_data[int(0.25 * len(pos_data)):int(
        0.5 * len(pos_data))]
    p3 = neg_data[int(0.5 * len(neg_data)):int(0.75 * len(neg_data))] + pos_data[int(0.5 * len(pos_data)):int(0.75 * len(pos_data))]
    p4 = neg_data[int(0.75 * len(neg_data)):] + pos_data[int(0.75 * len(pos_data)):]

    subsets = [p1, p2, p3, p4]

    test = 0
    max_acc = 0
    sum_acc = 0

    train_best = []
    test_best = []
    test_y_best = []
    train_y_best = []

    from sklearn.metrics import accuracy_score, precision_score

    for i in range(0, 4):
        training = list()
        testing = list()
        for j in range(4):
            if j == test:
                testing += subsets[j]
            else:
                training += subsets[j]

        test += 1

        train_x = [signal[:-1] for signal in training]
        train_y = [signal[-1] for signal in training]

        test_x = [signal[:-1] for signal in testing]
        test_y = [signal[-1] for signal in testing]

        classifier.fit(X=train_x, y=train_y)
        predictions = classifier.predict(test_x)

        acc = accuracy_score(y_true=test_y, y_pred=predictions)
        sum_acc += acc

        if max_acc < acc:
            max_acc = acc
            train_best = list(training)
            test_best = list(testing)
            test_y_best = list(test_y)
            train_y_best = list(train_y)

    print(f'Prosechna tochnost: {sum_acc / 4}')

    train_best = [signal[:col_rem] + signal[col_rem + 1:] for signal in train_best]
    test_best = [signal[:col_rem] + signal[col_rem + 1:] for signal in test_best]

    train_x = [signal[:-1] for signal in train_best]
    test_x = [signal[:-1] for signal in test_best]

    classifier.fit(X=train_x, y=train_y_best)
    predictions = classifier.predict(test_x)

    print(f"Tochnost so otstraneta kolona: {accuracy_score(y_true=test_y_best, y_pred=predictions)}")
