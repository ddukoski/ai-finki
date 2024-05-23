import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OrdinalEncoder


def rff(path):
    with open(path) as file:
        _read = list(csv.reader(file))
        return _read[0], _read[1:]


def numerize_levels(ds):
    encode = OrdinalEncoder()
    encode.fit([car_info[:-1] for car_info in ds])
    return encode


def print_accuracy_classifier(_classifier, features, classes, classifier_desc):
    test_n = len(features)
    predicted_classes = [_classifier.predict([features[i]])[0] for i in range(test_n)]

    predicted = 0
    for x, y in zip(predicted_classes, classes):
        if x == y:
            predicted += 1

    print(f'Accuracy of predictions ({classifier_desc}): {predicted / test_n * 100}%')


if __name__ == '__main__':
    feature_names, dataset = rff("data/car.csv")

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

    classifier = DecisionTreeClassifier(criterion='entropy', max_depth=10)
    classifier.fit(features_train, classes_train)

    importances = list(classifier.feature_importances_)

    for feature, imp in zip(feature_names, importances):
        print(f'{feature}: {imp}')

    best_feature = max(importances)
    rm_col = importances.index(best_feature)

    print(f'{feature_names[rm_col]} is the most important feature (according to the distribution), we are going to '
          f'remove it to see what happens to the predictions.')

    training_set_without_best = [car[:rm_col] + car[rm_col+1:] for car in training_set]
    testing_set_without_best = [car[:rm_col] + car[rm_col+1:] for car in training_set]

    dataset_morph = training_set_without_best + testing_set_without_best
    encoder_supress_best = numerize_levels(dataset_morph)

    features_wo_best_train = [car[:-1] for car in training_set_without_best]
    classes_wo_best_train = [car[-1] for car in training_set_without_best]
    features_wo_best_train = encoder_supress_best.transform(features_wo_best_train)

    features_wo_best_test = [car[:-1] for car in testing_set_without_best]
    classes_wo_best_test = [car[-1] for car in testing_set_without_best]
    features_wo_best_test = encoder_supress_best.transform(features_wo_best_test)

    classifier_without_best = DecisionTreeClassifier(criterion='entropy', max_depth=10)
    classifier_without_best.fit(X=features_wo_best_train, y=classes_wo_best_test)

    print_accuracy_classifier(classifier, features_test, classes_test, 'initial classifier')
    print_accuracy_classifier(classifier_without_best, features_wo_best_test, classes_wo_best_test, 'classifier '
                                                                                                    'without the best'
                                                                                                    ' feature of the '
                                                                                                    'criteria')
