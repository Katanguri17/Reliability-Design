from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import pandas as pd
import time


# TODO: graficzne przedstawienie?

def training(x, y, model):
    start = time.time()

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.5, test_size=0.5, random_state=0)
    y_pred = model.fit(x_train, y_train).predict(x_test)
    print("\n" + "Number of mislabeled points out of a total %d points : %d" % (
    x_test.shape[0], (y_test != y_pred).sum()))

    score = model.score(x_test, y_test)
    print("Accuracy ", score * 100, "%")

    end = time.time()

    print("Start time is " + str(start) + " seconds")
    print("End time is " + str(end) + " seconds")
    print("Exec: " + str(end - start))

    return score


def kbest(x, y, model):
    start = time.time()

    sel_chi2 = SelectKBest(chi2, k=10)  # select k features
    x_chi2 = sel_chi2.fit_transform(X, y)

    x_train, x_test, y_train, y_test = train_test_split(x_chi2, y, train_size=0.4, test_size=0.1, random_state=0)

    y_pred = model.fit(x_train, y_train).predict(x_test)
    print("\n" + "Number of mislabeled points out of a total %d points : %d" % (
    x_test.shape[0], (y_test != y_pred).sum()))

    score = model.score(x_test, y_test)
    print("Accuracy ", score * 100, "%")

    end = time.time()

    print("Start time is " + str(start) + " seconds")
    print("End time is " + str(end) + " seconds")
    print("Exec: " + str(end - start))


def variance_tres(x, y, model):
    start = time.time()

    sel_variance_threshold = VarianceThreshold()
    X_remove_variance = sel_variance_threshold.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(X_remove_variance, y, train_size=0.5, test_size=0.4,
                                                        random_state=0)

    y_pred = model.fit(x_train, y_train).predict(x_test)
    print("\n" + "Number of mislabeled points out of a total %d points : %d" % (
    x_test.shape[0], (y_test != y_pred).sum()))

    score = model.score(x_test, y_test)
    print("Accuracy ", score * 100, "%")

    end = time.time()

    print("Start time is " + str(start) + " seconds")
    print("End time is " + str(end) + " seconds")
    print("Exec: " + str(end - start))

    if x_train.shape == x.shape: return print("Nothing has changed, method does not work")


if __name__ == "__main__":

    # generate dataset
    dataset = pd.read_csv("data.csv", sep='|')

    # print(dataset)

    X = dataset.drop(['Name', 'md5', 'legitimate'], axis=1).values
    y = dataset['legitimate'].values
    # define the model
    model = ComplementNB()
    model1 = MultinomialNB()
    model2 = GaussianNB()

    models = [model, model1, model2]
    model_names = ["ComplementNB", "MultinomialNB", "GaussianNB"]

    for i in range(3):
        # Default_training
        print("\n", str(model_names[i]), " default training method")
        training(X, y, models[i])
        print("\n" + "Now the most interesting, optimized part: ")
        # Optimized Training Methods
        print("\n", str(model_names[i]), " Variance Treshold method: ")
        variance_tres(X, y, models[i])
        print("\n", str(model_names[i]), " SelectKBest features method: ")
        kbest(X, y, models[i])
        print("-----------------------------------------------------------")
