import csv
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OrdinalEncoder


def numerize_levels(ds):
    encode = OrdinalEncoder()
    encode.fit([car_info[:-1] for car_info in ds])
    return encode


def rff(path):
    with open(path) as file:
        return list(csv.reader(file))[1:]  # [1:] to avoid table descriptors


if __name__ == '__main__':
    dataset = rff("./data/car.csv")

    # train an encoder to interpret categorical (of ordinal type here) data as numerical
    encoder = numerize_levels(dataset)

    split_data = int(0.7 * len(dataset))

    training_set = dataset[:split_data]  # take 70% of the dataset for training of the model
    testing_set = dataset[split_data:]  # take other 30% for testing

    features_train = [car_info[:-1] for car_info in training_set]  # input vectors x
    classes_train = [y[-1] for y in training_set]  # output classes y
    features_train = encoder.transform(features_train)

    features_test = [car_info[:-1] for car_info in testing_set]
    classes_test = [y[-1] for y in testing_set]
    features_test = encoder.transform(features_test)

    classifier = CategoricalNB()
    classifier.fit(features_train, classes_train)

    test_n = len(features_test)
    predicted_classes = [classifier.predict([features_test[i]])[0] for i in range(test_n)]

    predicted = 0
    for x, y in zip(predicted_classes, classes_test):
        if x == y:
            predicted += 1

    print(f'Accuracy of predictions: {predicted / test_n * 100}%')
