import logs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn import neighbors, preprocessing
from sklearn.model_selection import train_test_split
from plotly.offline import plot

"""K-nearest neighbours algorithm implementation
    @author Kamil Kaliś"""


@logs.log_exec_time
def malware_data_transform(csv_data='MalwareData.csv', csv_sep='|', optimize_data=True):
    log = logs.get_logger()
    log.info("---Reading csv file")
    full_data = pd.read_csv(csv_data, sep=csv_sep)

    full_data = full_data.drop(['Name', 'md5'], axis=1)

    if optimize_data:
        trace = full_data['SizeOfCode'][:10]

        layout = go.Layout(title='Not normalized data')
        figure = go.Figure(go.Bar(y=trace), layout=layout)
        plot(figure, auto_open=True, filename='KNN.html')

        full_data_normalized = normalize_data(full_data)

        trace_norm = full_data_normalized['SizeOfCode'][:10]

        layout = go.Layout(title='Normalized data')
        figure = go.Figure(go.Bar(y=trace_norm), layout=layout)
        plot(figure, auto_open=True, filename='KNN_norm.html')
        # TODO: Find most significant features
        # TODO: check data normalization corectness

    transformed_data = full_data_normalized.drop(['legitimate'], axis=1).values if optimize_data \
        else full_data.drop(['legitimate'], axis=1).values

    labels = full_data['legitimate'].values

    return transformed_data, labels


def normalize_data(data: pd.DataFrame, max_range=1):
    return (data - data.min()) / (data.max() - data.min()) * max_range


@logs.log_exec_time
def knn_classifier(input_data, labels, n_neighbors=5):
    log = logs.get_logger()
    log.info(f"---Running KNN algorithm with n_neighbors={n_neighbors}")
    for weight in ['uniform', 'distance']:
        classifier = neighbors.KNeighborsClassifier(n_neighbors, weights=weight, metric='euclidean')
        X_train, X_test, Y_train, Y_test = train_test_split(input_data, labels, test_size=0.3)

        log.info(f"---Starting fitting for weight={weight}")
        classifier.fit(X_train, Y_train)

        score = classifier.score(X_test, Y_test)

        log.info(f"KNN accuracy is: {score * 100}%")


if __name__ == '__main__':
    logs.logger_setup()
    input_data, labels = malware_data_transform(optimize_data=True)
    knn_classifier(input_data, labels, 1)
