from flask import Flask, render_template,redirect,url_for, request,jsonify
import pandas as pd
from flask import *
from sklearn.tree import DecisionTreeClassifier
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = "Mekusmekus"
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'  # Database user
app.config['MYSQL_DATABASE_PASSWORD'] = ''  # Database password
app.config['MYSQL_DATABASE_DB'] = 'predicticare'  # Name of database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Hosting site

mysql.init_app(app)  
conn = mysql.connect()  
cursor = conn.cursor()



@app.route("/",methods=["POST", "GET"])
def land():
    return render_template("index.html")

@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == "POST": 
        cursor.execute('SELECT * FROM profileinfo') 
        check_num = cursor.fetchone()
           
        fullname = request.form["fullname"]
        age = int(request.form["age"])
        address = request.form["address"]
        gender = request.form["gender"]
        birthday = request.form["birthday"]
        address = request.form["address"]
        contact = int(request.form["contact"])
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]     
           
            
        if check_num[8] != email:
            flash('Account created Successfully', 'error')
            
        else:
             flash('Email already exist', 'error')             
        return redirect(url_for('land'))
            
    
       
            
    
@app.route("/home",methods=["POST", "GET"])
def home():
    return render_template("home.html")
def diagnose():
     if request.method == "POST": 
         if request.form['diagnosis_input']:
            age = int(request.form["age"])
            varfever=int(request.form["fever"])
            varcough = int(request.form["cough"])
            varfatigue = int(request.form["fatigue"]) 
            vardifBr = int(request.form["difbr"])
            vargender = int(request.form["gender"])
            varbp = int(request.form["bp"])
            varchol = int(request.form["chol"])
          
      
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