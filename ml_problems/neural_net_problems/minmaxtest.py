from data.kol_12_ds import dataset
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.exceptions import ConvergenceWarning
import warnings

def accuracy_score(y_true, y_pred):
    tp = 0

    for actual, pred in zip(y_true, y_pred):
        if actual == pred:
            tp += 1

    return tp / len(y_true)


if __name__ == '__main__':
    minmax = MinMaxScaler(feature_range=(-1, 1))
    warnings.filterwarnings(action='ignore', category=ConvergenceWarning)

    hidden_layer_neurons = int(input())
    learning_rate_init = float(input())
    rmcol = int(input())

    net = MLPClassifier(max_iter=200,
                        activation='relu',
                        random_state=0,
                        learning_rate_init=learning_rate_init,
                        hidden_layer_sizes=hidden_layer_neurons)

    splitter = int(0.8 * len(dataset))

    training = dataset[:splitter]
    testing = dataset[splitter:]

    train_x = [data[:-1] for data in training]
    train_y = [data[-1] for data in training]

    minmax.fit(train_x)

    train_x = minmax.transform(train_x)

    test_x = [data[:-1] for data in testing]
    test_y = [data[-1] for data in testing]
    test_x = minmax.transform(test_x)

    net.fit(X=train_x, y=train_y)

    pred_test = net.predict(test_x)
    pred_train = net.predict(train_x)

    train_acc = accuracy_score(train_y, pred_train)
    test_acc = accuracy_score(test_y, pred_test)

    train_x_remcol = []
    test_x_remcol = []

    if train_acc - test_acc > 0.15:
        print("Se sluchuva overfitting")

        for i in range(len(train_x)):
            train_x_remcol.append(list())
            for j in range(len(train_x[i])):
                if j != rmcol:
                    train_x_remcol[i].append(train_x[i][j])

        for i in range(len(test_x)):
            test_x_remcol.append(list())
            for j in range(len(test_x[i])):
                if j != rmcol:
                    test_x_remcol[i].append(test_x[i][j])

        net.fit(X=train_x_remcol, y=train_y)
    else:
        print("Ne se sluchuva overfitting")

    general = list(map(float, input().split()))
    general = general[:rmcol] + general[rmcol + 1:] if len(train_x_remcol) != 0 else general
    print(net.predict([general])[0])
