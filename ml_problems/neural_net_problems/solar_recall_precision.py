from data.solar_signal_data_2 import dataset
from sklearn.neural_network import MLPClassifier

import warnings
warnings.filterwarnings("ignore")


if __name__ == '__main__':
    x = int(input())
    classifier = MLPClassifier(3,
                               activation='relu',
                               learning_rate_init=0.003,
                               max_iter=200,
                               random_state=0)

    training = dataset[:len(dataset)-x]
    testing = dataset[len(dataset)-x:]

    train_x = [glare[:-1] for glare in training]
    train_y = [glare[-1] for glare in training]

    test_x = [glare[:-1] for glare in testing]
    test_y = [glare[-1] for glare in testing]

    classifier.fit(X=train_x, y=train_y)

    preds = classifier.predict(test_x)

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for pred, actual in zip(preds, test_y):
        if actual == 1:
            if pred == actual:
                tp += 1
            else:
                fn += 1
        else:
            if pred == actual:
                tn += 1
            else:
                fp += 1

    print(f'Precision: {(tp / (tp + fp))}')
    print(f'Recall: {(tp / (tp + fn))}')
