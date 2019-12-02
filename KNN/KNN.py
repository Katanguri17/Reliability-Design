import logs
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2

"""K-nearest neighbours algorithm implementation
    @author Kamil Kaliś"""


@logs.log_exec_time
def malware_data_transform(csv_data='MalwareData.csv', csv_sep='|', optimize_data=True, enable_figures=False):
    log = logs.get_logger()
    log.info("---Reading csv file")
    full_data = pd.read_csv(csv_data, sep=csv_sep)

    pd.set_option("display.max_columns", None)

    full_data = full_data.drop(['Name', 'md5'], axis=1)
    labels = full_data['legitimate'].values
    # data_to_norm = full_data.drop(['legitimate'], axis=1)

    if optimize_data:
        full_data_normalized = normalize_data(full_data)

        if enable_figures:
            trace = full_data['SizeOfCode'][:10]
            trace_norm = full_data_normalized['SizeOfCode'][:10]
            trace_all_norm = full_data_normalized.take([1]).max()

            # -------------------------------------------------
            layout = go.Layout(title='Not normalized data')
            figure = go.Figure(go.Bar(y=trace), layout=layout)
            plot(figure, auto_open=True, filename='KNN.html')
            # -------------------------------------------------
            layout = go.Layout(title='Normalized data')
            figure = go.Figure(go.Bar(y=trace_norm), layout=layout)
            plot(figure, auto_open=True, filename='KNN_norm.html')
            # -------------------------------------------------
            layout = go.Layout(title='Full normalized data')
            figure = go.Figure(go.Bar(y=trace_all_norm), layout=layout)
            plot(figure, auto_open=True, filename='KNN_all_norm.html')

    transformed_data = full_data_normalized.drop(['legitimate'], axis=1).values if optimize_data \
        else full_data.drop(['legitimate'], axis=1).values

    return transformed_data, labels


def normalize_data(data: pd.DataFrame, max_range=1):
    return (data - data.min()) / (data.max() - data.min()) * max_range


@logs.log_exec_time
def knn_classifier(input_data, labels, n_neighbors=5):
    log = logs.get_logger()
    for n in range(1, n_neighbors+1):
        log.info(f"---Running KNN algorithm with n_neighbors={n}")
        weight = 'distance'
        classifier = neighbors.KNeighborsClassifier(n, weights=weight, metric='euclidean')
        X_train, X_test, Y_train, Y_test = train_test_split(input_data, labels, test_size=0.3)

        """ Seems like number of features does not affect KNN algorithm"""
        # for k in range(3, 54, 25):
        # k = 20
        # log.info(f"---Finding best {k} features")
        # best_features_data = SelectKBest(chi2, k=k).fit_transform(input_data, labels)

        log.info(f"---Starting fitting for weight={weight}")
        classifier.fit(X_train, Y_train)

        score = classifier.score(X_test, Y_test)

        log.info(f"KNN accuracy is: {score * 100}%")


if __name__ == '__main__':
    logs.logger_setup()
    logs.get_logger().info("--------------------------------------")
    input_data, labels = malware_data_transform(optimize_data=True, enable_figures=False)
    knn_classifier(input_data, labels, 5)
    logs.get_logger().info("--------------------------------------")
