import seaborn as sn
import matplotlib.pyplot as plt
from sklearn import tree
import graphviz
import time
import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC


def get_confusion_matrix(Y, predictions, name):
    matrix = confusion_matrix(Y, predictions)
    # print(classification_report(Y, predictions))
    # print(matrix)
    df_cm = pd.DataFrame(matrix, range(2), range(2))
    sn.set(font_scale=1.4)
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, cmap='Blues', fmt='g')  # font size
    plt.title(str(name) + " feature selection")
    plt.show()


def show_graph(my_classifier, feautures_names, name):
    dot_data = tree.export_graphviz(my_classifier, out_file=None,
                                    feature_names=feautures_names,
                                    class_names=[str(0), str(1)],
                                    filled=True, rounded=True,
                                    special_characters=False)
    graph = graphviz.Source(dot_data)
    graph.render("decision_graph_" + str(name) + ".dot")




def train_decision_tree(X, Y, name):
    start_time = time.time()
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25)
    my_classifier = tree.DecisionTreeClassifier()
    my_classifier.fit(X_train, Y_train)
    score = my_classifier.score(X_test, Y_test)
    predictions = my_classifier.predict(X_test)
    print("")
    print(name + " feature selection")
    print(str(X.shape[1]) + " features")
    print("Accuracy ", score * 100)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("")
    get_confusion_matrix(Y_test, predictions, name)


if __name__ == "__main__":
    data = pd.read_csv("data.csv", sep='|')
    feautures_names = data.drop(['Name', 'md5', 'legitimate'], axis=1).columns
    X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values

    Y = data['legitimate'].values
    clf = ExtraTreesClassifier().fit(X, Y)
    feature_selection = SelectFromModel(clf, prefit=True)

    X_new_tree_based = feature_selection.transform(X)
    lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X, Y)
    model = SelectFromModel(lsvc, prefit=True)

    X_new_L1 = model.transform(X)

    train_decision_tree(X_new_L1, Y, "LinearSVC")

    train_decision_tree(X_new_tree_based, Y, "Tree selection")

    train_decision_tree(X, Y, "None")
