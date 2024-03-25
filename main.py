from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home(): 
    varfever = 1
    varcough = 1
    
    vardifBr = 1
    vargender = 1
    varbp = 3
    varchol = 1
    if request.method == "POST":
        
        fever = request.form["fever"]
        cough = request.form["cough"]
        fatigue = request.form["fatigue"]
        difBr = request.form["difBr"]
        age = request.form["age"]
        gender = request.form["gender"]
        bp = request.form["bp"]
        chol = request.form["chol"]
   
    if(fever=="Yes"):
         varfever = 1
    elif(cough=="Yes"):
        varcough = 1
    elif(fatigue=="Yes"):
        varfatigue = 1  
    elif(difBr=="Yes"):
        vardifBr =1 
    elif(gender=="Female" or gender=="female"):  
        vargender = 1
    elif(gender=="Male" or gender=="male"): 
        vargender = 0
    data = pd.read_csv('data.csv')

    X = data.drop(columns=['Desease'])
    y = data['Desease']

    model = DecisionTreeClassifier()

    model.fit(X.values, y)

    diagnosis = model.predict([[ varfever,varcough, varfatigue, vardifBr, age, vargender, varbp, varchol]])

    return render_template("home.html", diagnosis=diagnosis)

@app.route("/records")
def records():
    return render_template("records.html")

if __name__ == "__main__":
    app.run(debug=True)