import seaborn as sn
import matplotlib.pyplot as plt
from sklearn import tree
import graphviz
import numpy as np
import time
import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC
import warnings

warnings.filterwarnings("ignore")

svc_list = []
svc_features = []

tree_selection_list = []
tree_selection_features = []

none_feature_list = []


def get_average_confusion_matrix(list, name):
    a = list[0][0]
    b = list[0][1]

    for single_matrix in list:
        a = np.vstack((a, single_matrix[0]))
        b = np.vstack((b, single_matrix[1]))

    a = np.delete(a, (0), axis=0)
    b = np.delete(b, (0), axis=0)

    a_average = np.mean(a, axis=0)
    b_average = np.mean(b, axis=0)

    average_matrix = list[0][0]
    average_matrix = np.vstack((average_matrix, a_average))
    average_matrix = np.vstack((average_matrix, b_average))
    average_matrix = np.delete(average_matrix, 0, axis=0)

    df_cm = pd.DataFrame(average_matrix, range(2), range(2))
    sn.set(font_scale=1.4)
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, cmap='Blues', fmt='g')  # font size
    plt.title(str(name) + " feature selection")
    plt.show()

    print("average matrix : " + str(average_matrix))


def get_confusion_matrix(Y, predictions, name):
    matrix = confusion_matrix(Y, predictions)
    # print(classification_report(Y, predictions))
    if name == "LinearSVC":
        svc_list.append(matrix)
    if name == "Tree selection":
        tree_selection_list.append(matrix)
    if name == "None":
        none_feature_list.append(matrix)


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
    if name == "LinearSVC":
        svc_features.append(X.shape[1])
    if name == "Tree selection":
        tree_selection_features.append(X.shape[1])
    print("Accuracy ", score * 100)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("")
    get_confusion_matrix(Y_test, predictions, name)


def test_SVC_loop(X, Y, loop_range):
    for i in range(loop_range):
        print(i)
        lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X, Y)
        model = SelectFromModel(lsvc, prefit=True)
        X_new_L1 = model.transform(X)
        train_decision_tree(X_new_L1, Y, "LinearSVC")


def test_extra_tree_loop(X, Y, loop_range):
    for i in range(loop_range):
        print(i)
        clf = ExtraTreesClassifier().fit(X, Y)
        feature_selection = SelectFromModel(clf, prefit=True)
        X_new_tree_based = feature_selection.transform(X)
        train_decision_tree(X_new_tree_based, Y, "Tree selection")


def test_no_features_selection_loop(X, Y, loop_range):
    for i in range(loop_range):
        print(i)
        train_decision_tree(X, Y, "None")

if __name__ == "__main__":
    print("--- main starts ---")
    start_time = time.time()
    data = pd.read_csv("data.csv", sep='|')
    feautures_names = data.drop(['Name', 'md5', 'legitimate'], axis=1).columns
    X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values

    Y = data['legitimate'].values

    test_SVC_loop(X, Y, 5)
    test_extra_tree_loop(X, Y, 5)
    test_no_features_selection_loop(X, Y, 5)

    print("SVC average confusion matrix : ")
    get_average_confusion_matrix(svc_list , "LinerSVC")

    print("Tree Selection average matrix : ")
    get_average_confusion_matrix(tree_selection_list, "ExtraTree")

    print("No feature selection average confusion matrix : ")
    get_average_confusion_matrix(none_feature_list, "None")

    svc_average_features_amount = sum(svc_features) / len(svc_features)
    print("Average amount of features in SVC feature selection: " + str(svc_average_features_amount))

    tree_features_average_amount = sum(tree_selection_features) / len(tree_selection_features)
    print("Average amount of features in Tree Selection:  " + str(tree_features_average_amount))

    print("--- %s seconds ---" % (time.time() - start_time))
