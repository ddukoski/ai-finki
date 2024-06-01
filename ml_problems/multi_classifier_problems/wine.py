from data.wine_ds import dataset
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np

import warnings

if __name__ == '__main__':
    warnings.filterwarnings('ignore', category=ConvergenceWarning)

    dataset_bin = [wine[:-1] + [1] if wine[-1] >= 5 else wine[:-1] + [0] for wine in dataset]

    minmax = MinMaxScaler()
    std = StandardScaler()

    x = int((int(input()) / 100) * len(dataset_bin))

    training = dataset_bin[x:]
    testing = dataset_bin[:x]

    train_x = [wine[:-1] for wine in training]
    train_y = [wine[-1] for wine in training]

    test_x = [wine[:-1] for wine in testing]
    test_y = [wine[-1] for wine in testing]

    dtc = DecisionTreeClassifier(criterion='gini',
                                 random_state=0)

    dtc.fit(X=train_x, y=train_y)

    importances = list(dtc.feature_importances_)

    rm_col = np.argmin(importances)

    net = MLPClassifier(random_state=0,
                        activation='relu',
                        hidden_layer_sizes=15,
                        max_iter=200,
                        learning_rate_init=0.001)

    train_x = [wine[:rm_col] + wine[rm_col+1:] for wine in train_x]
    test_x = [wine[:rm_col] + wine[rm_col+1:] for wine in test_x]

    std.fit(train_x)
    minmax.fit(train_x)

    train_x_std = std.transform(train_x)
    test_x_std = std.transform(test_x)

    net.fit(X=train_x_std, y=train_y)

    pred_std = net.predict(test_x_std)

    train_x_min = minmax.transform(train_x)
    test_x_min = minmax.transform(test_x)

    net.fit(X=train_x_min, y=train_y)

    pred_minmax = net.predict(test_x_min)

    from sklearn.metrics import accuracy_score

    print(f'Tocnost so StandardScaler: {accuracy_score(y_true=test_y, y_pred=pred_std)}')
    print(f'Tocnost so MinMaxScaler: {accuracy_score(y_true=test_y, y_pred=pred_minmax)}')
