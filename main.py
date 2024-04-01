from flask import Flask, render_template,redirect,url_for, request,jsonify
import pandas as pd
from flask import *
from sklearn.tree import DecisionTreeClassifier
from flaskext.mysql import MySQL

import os

app = Flask(__name__)
app.secret_key = "Mekusmekus"
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'  # Database user
app.config['MYSQL_DATABASE_PASSWORD'] = ''  # Database password
app.config['MYSQL_DATABASE_DB'] = 'predicticare'  # Name of database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Hosting site
app.config['UPLOAD_FOLDER'] = 'static/img/cover'

mysql.init_app(app)  
conn = mysql.connect()  
cursor = conn.cursor()





@app.route("/",methods=["POST", "GET"])
def land():
    return render_template("landing.html", show ="true")

@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == "POST":
        cursor.execute('SELECT * FROM profileinfo') 
        accounts = cursor.fetchone() 
        file = request.files['pic'] 
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            prof_pic = "img/Cover/" + file.filename
            fullname = request.form["fullname"]
            age = int(request.form["age"])
            address = request.form["address"]
            gender = request.form["gender"]
            birthday = request.form["birthday"]
            address = request.form["address"]
            contact = int(request.form["contact"])
            emailsignup = request.form["email"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]    
             
    if accounts[8] == emailsignup:
        if(len(password) >= 8 and password == confirm_password):
            query = "INSERT INTO profileinfo (id, prof_pic, full_name, age, address, gender, birthday, contact, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (0, prof_pic, fullname, age, address, gender, birthday, contact, emailsignup, password)
            cursor.execute(query,values)
            conn.commit()
            flash('Account created Successfully!!', 'success')
        else:
            flash('Password does not match or shorter ', 'error')

    else:
        flash('Email already exist, Sign up again.', 'error')             
    return redirect(url_for('land'))
            
            
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST": 
        cursor.execute('SELECT email FROM profileinfo')  
        emaildb = cursor.fetchall()
        emails_list = [email[0] for email in emaildb]
        
        cursor.execute('SELECT password FROM profileinfo')  
        passwrds = cursor.fetchall()
        psswrd_list = [passwrd[0] for passwrd in passwrds]
        
        session['email'] = request.form["loginemail"]
        session['password'] = request.form["loginpassword"]
       
        if  session['email'] in emails_list and session['password'] in psswrd_list:
            session["logged"] = True  
        else:
            session["logged"] = False
            
    if session["logged"] == True: 
        cursor.execute('SELECT * FROM profileinfo WHERE email = %s and password = %s',( session['email'],session['password']))  
        info = list(cursor.fetchone())
        id = info[0]
        prof_pic = info[1]
        fullname = info[2]
        age = info[3]
        address = info[4]
        gender = info[5]
        birthday = info[6]
        contact = info[7]
        email = info[8]
        
        return render_template("home.html",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email)
    elif session["logged"]:
        cursor.execute('SELECT * FROM profileinfo WHERE email = %s and password = %s',( session['email'],session['password']))  
        info = list(cursor.fetchone())
        id = info[0]
        prof_pic = info[1]
        fullname = info[2]
        age = info[3]
        address = info[4]
        gender = info[5]
        birthday = info[6]
        contact = info[7]
        email = info[8]
        return redirect("/records",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email)
        
    else:
        flash('no matching credentials', 'error')
        return redirect('/')  
            
    
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
            return render_template("records.html",prediction=diagnosis[0])

@app.route("/records")
def records():
    cursor.execute('SELECT * FROM profileinfo WHERE email = %s and password = %s',( session['email'],session['password']))  
    info = list(cursor.fetchone())
    id = info[0]
    prof_pic = info[1]
    fullname = info[2]
    age = info[3]
    address = info[4]
    gender = info[5]
    birthday = info[6]
    contact = info[7]
    email = info[8]
    return render_template("records.html",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email)

@app.route('/sign_out')
def sign_out():
    session.pop('email')
    return redirect(url_for('land'))

    



if __name__ == "__main__":
    app.run(debug=True)