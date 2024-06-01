from data.solar_signals_data import dataset
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

if __name__ == '__main__':
    x = int(input())
    make_classifier = input()
    rmcol = int(input())

    testing = dataset[:x]
    training = dataset[x:]

    map_classifiers = {
        'NB': GaussianNB(),
        'DT': DecisionTreeClassifier(random_state=0),
        'NN': MLPClassifier(random_state=0,
                            hidden_layer_sizes=3,
                            max_iter=200,
                            learning_rate_init=0.003,
                            activation='relu')
    }

    classifier = map_classifiers[make_classifier]

    train_x = [sig[:-1] for sig in training]
    train_y = [sig[-1] for sig in training]

    test_x = [sig[:-1] for sig in testing]
    test_y = [sig[-1] for sig in testing]

    classifier.fit(X=train_x, y=train_y)

    pred = classifier.predict(test_x)

    from sklearn.metrics import precision_score, accuracy_score

    acc_full_col = accuracy_score(y_true=test_y, y_pred=pred)
    prec_full_col = precision_score(y_true=test_y, y_pred=pred)

    train_x_prune = [sig[:rmcol] + sig[rmcol + 1:] for sig in train_x]
    test_x_prune = [sig[:rmcol] + sig[rmcol + 1:] for sig in test_x]

    classifier.fit(X=train_x_prune, y=train_y)

    pred_prune = classifier.predict(test_x_prune)

    acc_prune_col = accuracy_score(y_true=test_y, y_pred=pred_prune)
    prec_prune_col = precision_score(y_true=test_y, y_pred=pred_prune)

    if acc_prune_col < acc_full_col:
        print(f'Klasifikatorot so site koloni ima pogolema tochnost\n{prec_full_col}')
    elif acc_prune_col > acc_full_col:
        print(f'Klasifikatorot so edna kolona pomalku ima pogolema tochnost\n{prec_prune_col}')
    else:
        print(f"Klasifikatorite imaat ista tochnost\n{prec_prune_col}")
