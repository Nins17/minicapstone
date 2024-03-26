from flask import Flask, render_template,redirect,url_for, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from flaskext.mysql import MySQL

app = Flask(__name__)

@app.route("/",methods=["POST", "GET"])
def home():
    return render_template("home.html")
def diagnose():
     if request.method == "POST": 
        e = request.form["age"]
        age =e
        if request.form["fever"] == "Yes":
            varfever = 1
        elif request.form["fever"] == "No":
            varfever = 0
        if request.form["cough"] == "Yes":
            varcough = 1
        elif request.form["cough"] == "No":
            varcough = 0
        if request.form["fatigue"] == "Yes":
            varfatigue = 1
        elif request.form["fatigue"] == "No":
            varfatigue = 0
        if request.form["difbr"] == "Yes":
            vardifBr = 1
        elif request.form["difbr"] == "No":
            vardifBr = 0
        if request.form["gender"] == "Female" :
            vargender = 1
        elif request.form["gender"] == "Male":
            vargender = 0
        if request.form["bp"] == "low" :
            varbp = 1
        elif request.form["bp"] == "Normal":
            varbp = 2
        elif request.form["bp"] == "High":
            varbp = 3
        if request.form["chol"] == "low" :
            varchol = 1
        elif request.form["chol"] == "Normal":
            varchol= 2
        elif request.form["chol"] == "High":
            varchol = 3

        data = pd.read_csv("data.csv")

        X = data.drop(columns=["Desease"])
        y = data["Desease"]

        model = DecisionTreeClassifier()

        model.fit(X.values, y)

        diagnosis = model.predict([[ varfever,varcough, varfatigue, vardifBr, age, vargender, varbp, varchol]]) 
        return render_template("home.html",prediction=diagnosis[0])

@app.route("/records")
def records():
    
    return render_template("records.html")

if __name__ == "__main__":
    app.run(debug=True)