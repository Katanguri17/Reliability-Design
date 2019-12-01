from sklearn import tree
import graphviz
import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv("data.csv", sep='|')

clean_files = data[0:41323].drop(['legitimate'], axis=1)
infected_files = data[41323::].drop(['legitimate'], axis=1)

feautures_names = data.drop(['Name', 'md5', 'legitimate'], axis=1).columns

X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values
Y = data['legitimate'].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.35)


my_classifier = tree.DecisionTreeClassifier()
my_classifier.fit(X_train, Y_train)
score = my_classifier.score(X_test, Y_test)
print("Accuracy ", score * 100)

dot_data = tree.export_graphviz(my_classifier, out_file=None,
                                feature_names=feautures_names,
                                class_names=[str(0), str(1)],
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("decision_graph")
