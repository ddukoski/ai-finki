from data.zad2_dataset import dataset
from sklearn.ensemble import RandomForestClassifier

def accuracy(_classifier, test_x, test_y):
    predictions = [_classifier.predict([test])[0] for test in test_x]
    correct = 0

    for actual, predicted in zip(test_y, predictions):
        if actual == predicted:
            correct += 1

    return correct/len(test_y)


if __name__ == '__main__':

    split_set = int(0.85 * len(dataset))

    rm_col = int(input())
    n_trees = int(input())
    criterion_classify = input()
    new_data_point = list(map(float, input().split()))

    dataset_rem_col = [fish[:rm_col] + fish[rm_col+1:] for fish in dataset]

    training_rem_col = dataset_rem_col[:split_set]
    testing_rem_col = dataset_rem_col[split_set:]

    train_X = [fish[:-1] for fish in training_rem_col]
    train_Y = [fish[-1] for fish in training_rem_col]

    test_X = [fish[:-1] for fish in testing_rem_col]
    test_Y = [fish[-1] for fish in testing_rem_col]

    rfc = RandomForestClassifier(n_estimators=n_trees, random_state=0, criterion=criterion_classify)
    rfc.fit(X=train_X, y=train_Y)

    removed_col_ndp = new_data_point[:rm_col] + new_data_point[rm_col + 1:]

    print(f'Accuracy: {accuracy(rfc, test_X, test_Y)}')
    print(rfc.predict([removed_col_ndp])[0])
    print(rfc.predict_proba([removed_col_ndp])[0])