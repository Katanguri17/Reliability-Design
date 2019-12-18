import logs
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from sklearn import neighbors, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import confusion_matrix

"""K-nearest neighbours algorithm implementation
    @author Kamil Kaliś"""


@logs.log_exec_time
def malware_data_transform(optimize_data=None, csv_data='MalwareData.csv', csv_sep='|', enable_figures=False):
    log = logs.get_logger()
    log.info("-Reading csv file")
    full_data = pd.read_csv(csv_data, sep=csv_sep)

    pd.set_option("display.max_columns", None)

    labels = full_data['legitimate'].values
    full_data: pd.DataFrame = full_data.drop(['Name', 'md5', 'legitimate'], axis=1)

    if optimize_data == 'normalize':
        log.info("--Data normalization processing...")
        full_data = pd.DataFrame(preprocessing.MinMaxScaler().fit_transform(full_data))
    elif optimize_data == 'standardize':
        log.info("--Data standardization processing...")
        full_data = pd.DataFrame(preprocessing.StandardScaler().fit_transform(full_data))

    if enable_figures:
        log.info("--Figures enabled")
        plot_bar_figures(full_data, optimize_data)

    return full_data.values, labels


def plot_bar_figures(full_data, optimize_data):
    cols = full_data.keys()
    if optimize_data == 'normalize':
        full_data_normalized = pd.DataFrame(preprocessing.MinMaxScaler().fit_transform(full_data))
        trace_norm_mean: pd.DataFrame = full_data_normalized.mean()
        trace_norm_std: pd.DataFrame = full_data_normalized.std()

        # -------------------------------------------------
        layout = go.Layout(title='Normalized data mean')
        figure = go.Figure(go.Bar(y=trace_norm_mean,
                                  x=cols
                                  ), layout=layout)
        plot(figure, auto_open=True, filename='KNN_norm_mean.html')
        # -------------------------------------------------
        layout = go.Layout(title='Normalized data standard deviation')
        figure = go.Figure(go.Bar(y=trace_norm_std,
                                  x=cols
                                  ), layout=layout)
        plot(figure, auto_open=True, filename='KNN_norm_std.html')

    elif optimize_data == 'standardize':

        full_data_standardized = pd.DataFrame(preprocessing.StandardScaler().fit_transform(full_data))
        trace_stand_mean = full_data_standardized.mean()
        trace_stand_std = full_data_standardized.std()

        # -------------------------------------------------
        layout = go.Layout(title='Standardized data mean')
        figure = go.Figure(go.Bar(y=trace_stand_mean,
                                  x=cols
                                  ), layout=layout)
        plot(figure, auto_open=True, filename='KNN_stand_mean.html')
        # -------------------------------------------------
        layout = go.Layout(title='Standardized data standard deviation')
        figure = go.Figure(go.Bar(y=trace_stand_std,
                                  x=cols
                                  ), layout=layout)
        plot(figure, auto_open=True, filename='KNN_stand_std.html')
    else:
        trace_mean = full_data.mean()
        trace_std = full_data.std()

        # -------------------------------------------------
        layout = go.Layout(title='Data mean')
        figure = go.Figure(go.Bar(y=trace_mean,
                                  x=cols
                                  ), layout=layout)
        plot(figure, auto_open=True, filename='KNN_mean.html')
        # -------------------------------------------------
        layout = go.Layout(title='Data standard deviation')
        figure = go.Figure(go.Bar(y=trace_std,
                                  x=cols
                                  ), layout=layout)
        plot(figure, auto_open=True, filename='KNN_std.html')


@logs.log_exec_time
def knn_classifier(input_data, labels, n_neighbors=1, run_for_features=(3, 30, 20)):
    log = logs.get_logger()
    for n in range(1, n_neighbors + 1):
        log.info(f"-Running KNN algorithm with n_neighbors={n}")
        weight = 'distance'
        classifier = neighbors.KNeighborsClassifier(n, weights=weight, metric='euclidean')
        for k in range(*run_for_features):
            log.info(f"--Finding best {k} features")
            best_features_data = SelectKBest(f_classif, k=k).fit_transform(input_data, labels)
            X_train, X_test, Y_train, Y_test = train_test_split(best_features_data, labels, test_size=0.3)

            log.info(f"---Starting fitting for weight={weight}")
            classifier.fit(X_train, Y_train)

            score = classifier.score(X_test, Y_test)

            log.info(f"----KNN accuracy is: {score * 100}%")

            """ Confusion matrix """
            log.info("-----Measuring confusion matrix...")
            result = classifier.predict(X_test)
            conf_matrix = confusion_matrix(Y_test, result)

            false_positives = conf_matrix[0][1] / sum(conf_matrix[0]) * 100
            false_negatives = conf_matrix[1][0] / sum(conf_matrix[1]) * 100
            log.info(f"------False positives in percent: {false_positives}%")
            log.info(f"------False negatives in percent: {false_negatives}%")


# TODO: Accuracy, Precision, Recall
# TODO: plot with comparison
if __name__ == '__main__':
    logs.logger_setup()
    logs.get_logger().info("--------------------------------------")
    input_data, labels = malware_data_transform(enable_figures=True)
    knn_classifier(input_data, labels, 1, (3, 24, 20))
    logs.get_logger().info("--------------------------------------")
    input_data, labels = malware_data_transform(optimize_data='normalize', enable_figures=True)
    knn_classifier(input_data, labels, 1, (3, 24, 20))
    logs.get_logger().info("--------------------------------------")
    input_data, labels = malware_data_transform(optimize_data='standardize', enable_figures=True)
    knn_classifier(input_data, labels, 1, (3, 24, 20))
