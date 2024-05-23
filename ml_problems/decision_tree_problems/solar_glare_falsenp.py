from data.kol_6_ds import dataset
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OrdinalEncoder


def codec(ds):
    _encoder = OrdinalEncoder()
    _encoder.fit([feats[:-1] for feats in ds])

    return _encoder

def accuracy(_classifier, test_x, test_y):
    predictions = _classifier.predict(test_x)

    correct = 0

    for actual, predicted in zip(test_y, predictions):
        if actual == predicted:
            correct += 1

    return correct / len(test_y)


def precision(_classifier, test_x, test_y):
    predictions = _classifier.predict(test_x)

    tp = 0
    fp = 0

    for actual, predicted in zip(test_y, predictions):
        if actual == '1':
            if predicted == actual:
                tp += 1
        else:
            if predicted == '1':
                fp += 1

    if tp == 0:
        return 0.0

    return tp / (tp + fp)


if __name__ == '__main__':

    encoder = codec(dataset)

    samples_take = int(input())
    split_set = len(dataset) - samples_take

    train_set = dataset[:split_set]
    test_set = dataset[split_set:]

    train_X = [glare[:-1] for glare in train_set]
    train_Y = [glare[-1] for glare in train_set]
    train_X = encoder.transform(train_X)

    test_X = [glare[:-1] for glare in test_set]
    test_Y = [glare[-1] for glare in test_set]
    test_X = encoder.transform(test_X)

    dtc = DecisionTreeClassifier(criterion='gini', random_state=0)

    dtc.fit(X=train_X, y=train_Y)

    print(f'Accuracy: {accuracy(dtc, test_X, test_Y)}')
    print(f'Precision: {precision(dtc, test_X, test_Y)}')
