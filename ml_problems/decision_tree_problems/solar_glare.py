from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OrdinalEncoder
from data.zad1_dataset import dataset


def codec(_set):
    """
    Performs ordinal encoding on an arbitrary set using sklearn.preprocessing.OrdinalEncoder
    """
    encoder = OrdinalEncoder()
    encoder.fit([feat[:-1] for feat in _set])
    return encoder


def accuracy(_classifier, test_x, test_y):
    predictions = [_classifier.predict([test])[0] for test in test_x]

    correct = 0

    for predicted, actual in zip(predictions, test_y):
        if actual == predicted:
            correct += 1

    return correct/len(test_y)


if __name__ == '__main__':
    coder = codec(dataset)

    split_percent = 1 - (int(input()) / 100)
    split_set = int(split_percent * len(dataset))

    training = dataset[split_set:]
    testing = dataset[:split_set]

    train_X = [glare[:-1] for glare in training]
    train_Y = [glare[-1] for glare in training]
    train_X = coder.transform(train_X)

    test_X = [glare[:-1] for glare in testing]
    test_Y = [glare[-1] for glare in testing]
    test_X = coder.transform(test_X)

    criterion_classify = input()

    dtc = DecisionTreeClassifier(random_state=0, criterion=criterion_classify)
    dtc.fit(X=train_X, y=train_Y)

    importances = list(dtc.feature_importances_)

    print(f'Depth: {dtc.get_depth()}')
    print(f'Number of leaves: {dtc.get_n_leaves()}')
    print(f"Accuracy: {accuracy(dtc, test_X, test_Y)}")
    print(f'Most important feature: {importances.index(max(importances))}')
    print(f'Least important feature: {importances.index(min(importances))}')



