from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
import time

def plot_conf_matrix(y_real, y_pred, name, name2):
    cm = confusion_matrix(y_real, y_pred)
    df = pd.DataFrame(cm, range(2), range(2))
    sn.set(font_scale=1.4)
    sn.heatmap(df, annot=True, annot_kws={"size": 16}, cmap='Blues', fmt='g')
    plt.title(str(name) + " model selection, " + name2 + " feature selection")
    plt.show()

def default_training(x, y, model):
    start = time.time()


    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.5, test_size=0.5, random_state=0)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("\n" + "Number of mislabeled points out of a total %d points : %d" % (x_test.shape[0], (y_test != y_pred).sum()))
    score = model.score(x_test, y_test)
    print("Accuracy ", score * 100, "%")
    print("Inne Accuracy: ", accuracy_score(y_pred, y_test) * 100, "%")

    end = time.time()

    print("Start time is " + str(start) + " seconds")
    print("End time is " + str(end) + " seconds")
    print("Exec: " + str(end - start))
    print("Matrix size: ", x.shape)
    model_name = ""
    for x in range(len(str(model))):
        if str(model)[x] == 'N':
            break
        model_name = model_name + str(model)[x]

    plot_conf_matrix(y_test, y_pred, model_name, "default")


def kbest(x, y, model):
    start = time.time()

    sel_chi2 = SelectKBest(chi2, k=8)  # select k features
    x_chi2 = sel_chi2.fit_transform(X, y)

    x_train, x_test, y_train, y_test = train_test_split(x_chi2, y, train_size=0.4, test_size=0.1, random_state=0)

    y_pred = model.fit(x_train, y_train).predict(x_test)
    print("\n"+"Number of mislabeled points out of a total %d points : %d" % (x_test.shape[0], (y_test != y_pred).sum()))

    score = model.score(x_test, y_test)
    print("Accuracy ", score * 100, "%")

    end = time.time()

    print("Start time is " + str(start) + " seconds")
    print("End time is " + str(end) + " seconds")
    print("Exec: " + str(end - start))
    print("Matrix size: ", x_chi2.shape)
    model_name = ""
    for x in range(len(str(model))):
        if str(model)[x] == 'N':
            break
        model_name = model_name + str(model)[x]

    plot_conf_matrix(y_test, y_pred, model_name, "SelectKBest")

def variance_tres(x,y,model):
    start = time.time()

    sel_variance_threshold = VarianceThreshold()
    X_remove_variance = sel_variance_threshold.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(X_remove_variance, y, train_size=0.5, test_size=0.4, random_state=0)

    y_pred = model.fit(x_train, y_train).predict(x_test)
    print("\n" + "Number of mislabeled points out of a total %d points : %d" % (x_test.shape[0], (y_test != y_pred).sum()))

    score = model.score(x_test, y_test)
    print("Accuracy ", score * 100, "%")

    end = time.time()

    print("Start time is " + str(start) + " seconds")
    print("End time is " + str(end) + " seconds")
    print("Exec: " + str(end - start))
    print("Matrix size: ", X_remove_variance.shape)
    model_name = ""
    for i in range(len(str(model))):
        if str(model)[i] == 'N':
            break
        model_name = model_name + str(model)[i]

    plot_conf_matrix(y_test, y_pred, model_name, "Variance Threshold")

    if x_train.shape[0] == x.shape[0]: print("Nothing has changed, method does not optimize in this case")

if __name__ == "__main__":

    # generate dataset
    dataset = pd.read_csv("data.csv", sep='|')

    # print(dataset)

    X = dataset.drop(['Name', 'md5', 'legitimate'], axis=1).values
    y = dataset['legitimate'].values

    # define the model
    model = ComplementNB()          # slightly better than MNB, supposed to be more accurate
    model1 = MultinomialNB()
    model2 = GaussianNB()
    model3 = CategoricalNB()

    models = [model, model1, model2]
    model_names = ["ComplementNB", "MultinomialNB", "GaussianNB"]

    for i in range(3):
        # Default_training
        print("\n", str(model_names[i]), " default training method")
        default_training(X, y, models[i])

        # Optimized Training Methods

        print("\n" + "Now the most interesting, optimized part: ")
        print("\n", str(model_names[i]),  " Variance Threshold method: ")
        variance_tres(X, y, models[i])

        print("\n", str(model_names[0]), " SelectKBest features method: ")
        kbest(X, y, models[0])
        print("-----------------------------------------------------------")

