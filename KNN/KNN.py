import logs
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from sklearn import neighbors, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import confusion_matrix

"""K-nearest neighbours algorithm implementation
    @author Kamil Kaliś"""


@logs.log_exec_time
def malware_data_transform(optimize_data, csv_data='MalwareData.csv', csv_sep='|', enable_figures=False):
    log = logs.get_logger()
    log.info("---Reading csv file")
    full_data = pd.read_csv(csv_data, sep=csv_sep)

    pd.set_option("display.max_columns", None)

    labels = full_data['legitimate'].values
    full_data: pd.DataFrame = full_data.drop(['Name', 'md5', 'legitimate'], axis=1)

    if optimize_data == 'normalize':
        log.info("---Data normalization processing...")
        """ Not really improving stats... """
        # to_remove = []
        # for i, item in enumerate(full_data.std()):
        #     if item > 10 ** 3:
        #         to_remove.append(full_data.columns[i])
        #
        # full_data = full_data.drop(to_remove, axis=1)

        full_data_normalized = normalize_data(full_data)
    elif optimize_data == 'standardize':
        log.info("---Data standardization processing...")
        full_data = preprocessing.StandardScaler().fit_transform(full_data)

    if enable_figures:
        log.info("---Figures enabled")
        plot_bar_figures(full_data, optimize_data)

    transformed_data = full_data_normalized.values if optimize_data else full_data.values

    return transformed_data, labels


def normalize_data(data: pd.DataFrame, max_range=1):
    return (data - data.min()) / (data.max() - data.min()) * max_range


# TODO:
def standarize_data(data: pd.DataFrame):
    pass


def plot_bar_figures(full_data, optimize_data):
    if optimize_data == 'normalize':
        full_data_normalized = normalize_data(full_data)
    elif optimize_data == 'standardize':
        full_data = preprocessing.StandardScaler().fit_transform(full_data)

    trace_mean = full_data.mean()
    trace_norm_mean: pd.DataFrame = full_data_normalized.mean()

    trace_std = full_data.std()
    trace_norm_std: pd.DataFrame = full_data_normalized.std()

    # -------------------------------------------------
    layout = go.Layout(title='Not normalized data mean')
    figure = go.Figure(go.Bar(y=trace_mean,
                              x=trace_mean.keys()
                              ), layout=layout)
    plot(figure, auto_open=True, filename='KNN_mean.html')
    # -------------------------------------------------
    layout = go.Layout(title='Normalized data mean')
    figure = go.Figure(go.Bar(y=trace_norm_mean,
                              x=trace_norm_mean.keys()
                              ), layout=layout)
    plot(figure, auto_open=True, filename='KNN_norm_mean.html')
    # -------------------------------------------------
    layout = go.Layout(title='Not normalized data standard deviation')
    figure = go.Figure(go.Bar(y=trace_std,
                              x=trace_std.keys()
                              ), layout=layout)
    plot(figure, auto_open=True, filename='KNN_std.html')
    # -------------------------------------------------
    layout = go.Layout(title='Normalized data standard deviation')
    figure = go.Figure(go.Bar(y=trace_norm_std,
                              x=trace_norm_std.keys()
                              ), layout=layout)
    plot(figure, auto_open=True, filename='KNN_norm_std.html')


@logs.log_exec_time
def knn_classifier(input_data, labels, n_neighbors=5):
    log = logs.get_logger()
    for n in range(1, n_neighbors + 1):
        log.info(f"---Running KNN algorithm with n_neighbors={n}")
        weight = 'distance'
        classifier = neighbors.KNeighborsClassifier(n, weights=weight, metric='euclidean')
        X_train, X_test, Y_train, Y_test = train_test_split(input_data, labels, test_size=0.3)

        """ Seems like number of features does not affect KNN algorithm"""
        for k in range(3, 54, 25):
            k = 20
        log.info(f"---Finding best {k} features")
        best_features_data = SelectKBest(chi2, k=k).fit_transform(input_data, labels)

        log.info(f"---Starting fitting for weight={weight}")
        classifier.fit(X_train, Y_train)

        score = classifier.score(X_test, Y_test)

        log.info(f"KNN accuracy is: {score * 100}%")

        """ Confusion matrix """
        log.info("---Measuring confusion matrix...")
        result = classifier.predict(X_test)
        conf_matrix = confusion_matrix(Y_test, result)

        false_positives = conf_matrix[0][1] / sum(conf_matrix[0]) * 100
        false_negatives = conf_matrix[1][0] / sum(conf_matrix[1]) * 100
        log.info(f"False positives in percent: {false_positives}%")
        log.info(f"False negatives in percent: {false_negatives}%")


if __name__ == '__main__':
    logs.logger_setup()
    logs.get_logger().info("--------------------------------------")
    input_data, labels = malware_data_transform(optimize_data='Normalize', enable_figures=False)
    knn_classifier(input_data, labels, 3)
    logs.get_logger().info("--------------------------------------")
    input_data, labels = malware_data_transform(optimize_data='Standardize', enable_figures=False)
    knn_classifier(input_data, labels, 3)
