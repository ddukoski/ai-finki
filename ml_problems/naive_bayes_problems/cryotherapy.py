from data.exer2_dataset import dataset
from sklearn.naive_bayes import GaussianNB

# Ova e primerok od podatochnoto mnozestvo, za treniranje/evaluacija koristete ja
# importiranata promenliva dataset

dataset_sample = [['1', '35', '12', '5', '1', '100', '0'],
                  ['1', '29', '7', '5', '1', '96', '1'],
                  ['1', '50', '8', '1', '3', '132', '0'],
                  ['1', '32', '11.75', '7', '3', '750', '0'],
                  ['1', '67', '9.25', '1', '1', '42', '0']]


if __name__ == '__main__':

    dataset = [list(map(float, therapy)) for therapy in dataset]

    X = [therapy[:-1] for therapy in dataset]
    Y = [therapy[-1] for therapy in dataset]

    split_point = int(0.85 * len(X))

    train_X = X[:split_point]
    train_Y = Y[:split_point]

    test_X = X[split_point:]
    test_Y = Y[split_point:]

    classifier = GaussianNB()
    classifier.fit(X=train_X, y=train_Y)

    predictions = [classifier.predict([test_X[i]])[0] for i in range(len(test_Y))]

    predicted = 0

    for actual, prediction in zip(test_Y, predictions):
        if actual == prediction:
            predicted += 1

    print(predicted / len(test_Y))

    to_predict = list(map(float, input().split()))

    print( int(classifier.predict([to_predict])[0]) )

    print(classifier.predict_proba([to_predict]))


