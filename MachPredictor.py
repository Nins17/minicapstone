import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('data.csv')


X = data.drop(columns=['Desease'])
y = data['Desease']

model = DecisionTreeClassifier()

model.fit(X.values, y)

diagnosis = model.predict([[1,1,0,1,20,1,3,1]])

print(diagnosis)
