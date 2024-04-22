import csv
from sklearn.naive_bayes import GaussianNB


def rff(path):
    with open(path) as file:
        return list(csv.reader(file))[1:]


if __name__ == '__main__':
    dataset = rff("./data/medical_data.csv")
    dataset = [list(map(int, patient)) for patient in dataset]

    convert = {
        0: "Non-Diabetic",
        1: "Diabetic"
    }

    slicing = int(0.7 * len(dataset))

    training_set = dataset[:slicing]
    testing_set = dataset[slicing:]

    features_train = [patient[:-1] for patient in training_set]
    classes_train = [convert[patient[-1]] for patient in training_set]

    features_test = [patient[:-1] for patient in testing_set]
    classes_test = [convert[patient[-1]] for patient in testing_set]

    classifier = GaussianNB()
    classifier.fit(X=features_train, y=classes_train)  # training the model

    comparison = [classifier.predict([data_point]) for data_point in features_test]

    correct = 0
    for x, y in zip(comparison, classes_test):
        if x == y:
            correct += 1

    print(f'Accuracy: {correct / len(features_test)}%')
