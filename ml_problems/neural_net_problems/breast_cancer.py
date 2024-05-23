from data.nn_lab_dataset2 import data

from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPClassifier


def get_predictions_stats(classifier, test_x, test_y):
    predictions = classifier.predict(test_x)

    tp, fp, tn, fn = 0, 0, 0, 0

    for actual, predicted in zip(test_y, predictions):
        if actual == 'B':
            if predicted == actual:
                tn += 1
            else:
                fn += 1
        else:
            if predicted == actual:
                tp += 1
            else:
                fp += 1

    return tp, fp, tn, fn


def recall(classifier, test_x, test_y):
    tp, fp, tn, fn = get_predictions_stats(classifier, test_x, test_y)

    return tp / (tp + fn)


def precision(classifier, test_x, test_y):
    tp, fp, tn, fn = get_predictions_stats(classifier, test_x, test_y)

    return tp / (tp + fp)


if __name__ == '__main__':

    hidden_layer_neurons = int(input())

    benign = [scan for scan in data if scan[0] == 'B']
    malignant = [scan for scan in data if scan[0] == 'M']

    validation = malignant[int(0.7 * len(malignant)):] + benign[int(0.7 * len(benign)):]
    training = malignant[:int(0.7 * len(malignant))] + benign[:int(0.7 * len(benign))]

    min_max_scaler = MinMaxScaler(feature_range=(-1, 1))

    train_X = [scan[1:] for scan in training]
    train_Y = [scan[0] for scan in training]

    min_max_scaler.fit(train_X)
    train_X = min_max_scaler.transform(train_X)

    validate_X = [scan[1:] for scan in validation]
    validate_Y = [scan[0] for scan in validation]

    validate_X = min_max_scaler.transform(validate_X)

    net = MLPClassifier(activation='relu',
                        max_iter=20,
                        learning_rate_init=0.001,
                        hidden_layer_sizes=hidden_layer_neurons,
                        random_state=0)

    net.fit(X=train_X, y=train_Y)

    print(f'Preciznost so trenirachkoto mnozhestvo: {recall(net, train_X, train_Y)}')
    print(f'Odziv so trenirachkoto mnozhestvo: {precision(net, train_X, train_Y)}')
    print(f'Preciznost so testirachkoto mnozhestvo: {recall(net, validate_X, validate_Y)}')
    print(f'Odziv so testirachkoto mnozhestvo: {precision(net, validate_X, validate_Y)}')
