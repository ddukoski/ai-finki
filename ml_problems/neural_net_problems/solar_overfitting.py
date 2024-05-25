from data.nn_lab_dataset1 import data as data
from sklearn.neural_network import MLPClassifier

def accuracy(classifier, test_x, test_y):
    predictions = classifier.predict(test_x)

    correct = 0

    for actual, pred in zip(test_y, predictions):
        if actual == pred:
            correct += 1

    return correct / len(test_y)


if __name__ == '__main__':

    hidden_layer_neurons = 6

    learning_rate = float(input())
    epochs = int(input())

    classes_ds = [glare[-1] for glare in data]
    classes = set(classes_ds)

    split_by_class = list()

    for i in range(len(classes)):
        split_by_class.append(list())

    for data_point in data:
        split_by_class[data_point[-1]].append(data_point)

    training_set = []
    validation_set = []

    for by_class in split_by_class:
        coef = int(len(by_class) * 0.8)
        training_set += by_class[:coef]
        validation_set += by_class[coef:]

    net = MLPClassifier(hidden_layer_sizes=hidden_layer_neurons,
                        learning_rate_init=learning_rate,
                        max_iter=epochs,
                        activation='tanh',
                        random_state=0)

    train_X = [glare[:-1] for glare in training_set]
    train_Y = [glare[-1] for glare in training_set]

    validate_X = [glare[:-1] for glare in validation_set]
    validate_Y = [glare[-1] for glare in validation_set]

    net.fit(X=train_X, y=train_Y)

    acc_upon_training = accuracy(net, train_X, train_Y)
    acc_upon_validation = accuracy(net, validate_X, validate_Y)

    conclusion = 'Se sluchuva overfitting' if (acc_upon_training - acc_upon_validation) >= 0.1 else 'Ne se sluchuva overfitting'

    print(conclusion)
    print(f'Tochnost so trenirachko mnozhestvo {acc_upon_training}')
    print(f'Tochnost so validacisko mnozhestvo {acc_upon_validation}')
