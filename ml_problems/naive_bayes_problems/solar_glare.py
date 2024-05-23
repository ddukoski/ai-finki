from data.exer1_dataset import dataset
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import CategoricalNB

dataset_sample = [['C', 'S', 'O', '1', '2', '1', '1', '2', '1', '2', '0'],
                  ['D', 'S', 'O', '1', '3', '1', '1', '2', '1', '2', '0'],
                  ['C', 'S', 'O', '1', '3', '1', '1', '2', '1', '1', '0'],
                  ['D', 'S', 'O', '1', '3', '1', '1', '2', '1', '2', '0'],
                  ['D', 'A', 'O', '1', '3', '1', '1', '2', '1', '2', '0']]


def numerize_set(ds):
    """
    ds - a given dataset
    """
    coder = OrdinalEncoder()
    coder.fit([glare[:-1] for glare in ds])
    return coder


if __name__ == '__main__':

    encoder = numerize_set(dataset)

    feat = [glare[:-1] for glare in dataset]
    classes = [glare[-1] for glare in dataset]

    split_set = int(0.75 * len(feat))

    feat_train = feat[:split_set]
    class_train = classes[:split_set]
    feat_train = encoder.transform(feat_train)

    feat_test = feat[split_set:]
    class_test = classes[split_set:]
    feat_test = encoder.transform(feat_test)

    classifier = CategoricalNB()

    classifier.fit(X=feat_train, y=class_train)

    predicted = 0
    predictions = [classifier.predict([feat_test[i]])[0] for i in range(len(feat_test))]

    for actual, prediction in zip(class_test, predictions):
        if actual == prediction:
            predicted += 1

    print(f'Accuracy: {predicted / len(class_test)}')

    to_predict = encoder.transform([list
                                    (map
                                     (str, input().split())
                                     )])

    print(f'Prediction for input: {classifier.predict(to_predict)[0]}')

    print(f'Probability for each class: {classifier.predict_proba(to_predict)}')
