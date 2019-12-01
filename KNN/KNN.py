import pandas as pd
import logs
from sklearn import neighbors, preprocessing
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
from plotly.offline import plot

"""K-nearest neighbours algorithm implementation
    @author Kamil Kaliś"""


@logs.log_exec_time
def malware_data_transform(csv_data='MalwareData.csv', csv_sep='|', optimize_data=False):
    log = logs.get_logger()
    log.info("---Reading csv file")
    full_data = pd.read_csv(csv_data, sep=csv_sep)

    if optimize_data:
        df = pd.DataFrame(full_data)
        trace = df['SizeOfInitializedData'][:10]
        print(trace)
        layout = go.Layout(title='KNN Plot')
        figure = go.Figure(go.Bar(y=trace), layout=layout)
        plot(figure, auto_open=True, filename='KNN.html')
        # TODO: Find most significant features
        # TODO: Normalize data
        pass

    transformed_data = full_data.drop(['Name', 'md5', 'legitimate'], axis=1).values
    labels = full_data['legitimate'].values

    return transformed_data, labels


@logs.log_exec_time
def classifier_knn(input_data, labels):
    log = logs.get_logger()
    n_neighbors = 10
    log.info(f"---Running KNN algorithm with n_neighbors={n_neighbors}")
    for weight in ['uniform', 'distance']:
        classifier = neighbors.KNeighborsClassifier(n_neighbors, weights=weight, metric='euclidean')
        X_train, X_test, Y_train, Y_test = train_test_split(input_data, labels, test_size=0.3)

        log.info(f"---Starting fitting for weight={weight}")
        classifier.fit(X_train, Y_train)

        score = classifier.score(X_test, Y_test)

        log.info(f"---KNN accuracy is: {score * 100}%")


if __name__ == '__main__':
    # logs.logger_setup()
    input_data, labels = malware_data_transform(optimize_data=True)
    # classifier_knn(input_data, labels)
