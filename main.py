from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    data = pd.read_csv('data.csv')

    X = data.drop(columns=['Desease'])
    y = data['Desease']

    model = DecisionTreeClassifier()

    model.fit(X.values, y)
    
    # fever = request.form["fever"]
    # cough = request.form["cough"]
    # fatigue = request.form["fatigue"]
    # difBr = request.form["difBr"]
    # age = request.form["age"]
    # gender = request.form["gender"]
    # bp = request.form["bp"]
    # chol = request.form["chol"]
    
   
    
    varfever = 1
    varcough = 1
    varfatigue = 0
    vardifBr = 1
    varage = 20
    vargender = 1
    varbp = 3
    varchol = 1
    

    diagnosis = model.predict([[ varfever,varcough, varfatigue, vardifBr, varage, vargender, varbp, varchol]])

    return render_template("home.html", diagnosis=diagnosis)

@app.route("/records")
def records():
    return render_template("records.html")

if __name__ == "__main__":
    app.run(debug=True)