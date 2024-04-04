from flask import Flask, render_template,redirect,url_for, request
import pandas as pd
from flask import *
from sklearn.tree import DecisionTreeClassifier
from flaskext.mysql import MySQL
import pyttsx3
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
        accounts = cursor.fetchall()  # Instead of fetching one, fetch everything.
        all_emails = []  # Create an empty list to add all the emails.
        for i in accounts:
            all_emails.append(i[8])  # i with the index of 8 is the column of email.
        print(all_emails)
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
             
            if emailsignup in all_emails:
                flash('Email already exist, Sign up again.', 'error')

            else:
                if(len(password) >= 8 and password == confirm_password):
                    query = "INSERT INTO profileinfo (id, prof_pic, full_name, age, address, gender, birthday, contact, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (0, prof_pic, fullname, age, address, gender, birthday, contact, emailsignup, password)
                    cursor.execute(query, values)
                    conn.commit()
                    flash('Account created Successfully!!', 'success')
                else:
                    flash('Password does not match or shorter ', 'error')

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
        engine = pyttsx3.init()

    # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech

    # Convert diagnosis to speech
        diagnosis_text = "Welcom to Predicty Care! Where we care with Predictive Precision."
        engine.say(diagnosis_text)

        engine.runAndWait()
        return render_template("home.html",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email)
        
        
    else:
        flash('no matching credentials', 'error')
        return redirect('/')  
            
    
@app.route("/home",methods=["POST", "GET"])
def home():
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

@app.route("/diagnose", methods=["POST", "GET"])
def diagnose():
    if request.method == "POST":
        ages = int(request.form["age"])
        fever = int(request.form["fever"])
        cough = int(request.form["cough"])
        fatigue = int(request.form["fatigue"])
        difBr = int(request.form["difbr"])
        gender = int(request.form["gender"])
        bp = int(request.form["bp"])
        chol = int(request.form["chols"])
         
        # Checking conditions for variables
        if fever == 0 or cough == 0 or fatigue == 0 or difBr == 0:
            varfever = "NO"
            varcough = "NO"
            varfatigue = "NO"
            vardifBr = "NO"
        if fever == 1 or cough == 1 or fatigue == 1 or difBr == 1 or bp == 1 or chol == 1:
            varfever = "YES"
            varcough = "YES"
            varfatigue = "YES"
            vardifBr = "YES"
            varbp = "LOW"
            varchol = "LOW"
        if  gender==1:
            vargender="FEMALE"
        if  gender==0:
            vargender="MALE"
        if bp == 2 or chol == 2:
            varbp = "NORMAL"
            varchol = "NORMAL"
        elif bp == 3 or chol == 3:
            varbp = "HIGH"
            varchol = "HIGH"
        data = pd.read_csv("data.csv")

        X = data.drop(columns=["Desease"])
        y = data["Desease"]

        model = DecisionTreeClassifier()

        model.fit(X.values, y)

        diagnosis = model.predict([[ fever,cough,fatigue,difBr, ages, gender,bp,chol]])
        session['diagnosis_res']=str(diagnosis[0])
        
        
        cursor.execute('SELECT id FROM profileinfo WHERE email = %s and password = %s',( session['email'],session['password']))  
        ref_id = cursor.fetchone()
        # Inserting data into the records table
        query = "INSERT INTO records (Id, Reference_num, Fever, Cough, Fatigue, difficulty_breathing, Age, Gender, Blood_pressure, Cholesterol, Result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (0, ref_id, varfever, varcough, varfatigue, vardifBr, ages,vargender, varbp, varchol, diagnosis[0])
        cursor.execute(query, values)
        conn.commit()
        
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
        
        cursor.execute('SELECT * FROM records WHERE Reference_num=%s',(ref_id)) 
        records = list(cursor.fetchall())
        
    
       
        cursor.execute('SELECT * FROM records WHERE Reference_num=%s',(ref_id)) 
        records = list(cursor.fetchall())
        diagnosis_res=str(diagnosis[0])
        # Initialize the TTS engine
        engine = pyttsx3.init()

    # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech

    # Convert diagnosis to speech
        diagnosis_text = "The prediction says you have: " +diagnosis_res+"...We recommend yo to visit your doctor"
        engine.say(diagnosis_text)

    # Wait for the speech to finish
        engine.runAndWait()
        return render_template("records.html",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email,records=records)


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
    
    cursor.execute('SELECT id FROM profileinfo WHERE email = %s and password = %s',( session['email'],session['password']))  
    ref_id = cursor.fetchone()
    cursor.execute('SELECT * FROM records WHERE Reference_num=%s',(ref_id)) 
    records = list(cursor.fetchall())
    
    return render_template("records.html",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email,records=records)


@app.route('/update')
def update():
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
    return render_template("updateProfile.html",ref_id=id,pic=prof_pic,name=fullname,age=age,address=address,gender=gender,bday=birthday,number=contact,email=email)
    
@app.route('/updateinfo',methods=["POST", "GET"])
def updateinfo():
    if request.method == "POST":
        cursor.execute('SELECT * FROM profileinfo')
        accounts = cursor.fetchall()
        all_emails = [i[8] for i in accounts]  # List comprehension to extract emails
        print(all_emails)
        
        cursor.execute('SELECT * FROM profileinfo WHERE email = %s and password = %s',
                       (session['email'], session['password']))
        info = list(cursor.fetchone())
        id = info[0]
        profpic = info[1]
        
        file = request.files.get('pic')  # Use get() to avoid KeyError if 'pic' is not in request.files
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(filename)
            newprof_pic = "img/Cover/" + file.filename 
        else:
            newprof_pic = profpic
        
        # Extract form data
        newfullname = request.form["fullname"]
        newage = int(request.form["age"])
        newaddress = request.form["address"]
        newgender = request.form["gender"]
        newbirthday = request.form["birthday"]
        newcontact = int(request.form["contact"])
        newemail = request.form["email"]
        new_password = request.form["password"]
        old_password = request.form["old_password"]
        confirm_password = request.form["confirm_password"]
        
        # Validate and update password
        if len(new_password) >= 8 and new_password == confirm_password:
            pass  # Password meets criteria
        elif len(new_password) == 0:
            new_password = session['password']
        else:
            flash('Password does not match or shorter', 'error')
            return redirect(url_for('updateinfo'))  # Redirect to updateinfo page on password error
        
        # Validate and update email
        if newemail in all_emails:
            newemail = session['email']
        else:
            pass  # Email is unique
        
        # Check old password before updating profile
        if old_password == session['password']:
            query = "UPDATE profileinfo SET prof_pic=%s, full_name=%s, age=%s, address=%s, gender=%s, " \
                    "birthday=%s, contact=%s, email=%s, password=%s WHERE id=%s"
            values = (newprof_pic, newfullname, newage, newaddress, newgender, newbirthday, newcontact,
                      newemail, new_password, id)
            cursor.execute(query, values)
            conn.commit()
            flash('Account updated Successfully!!', 'success')
        else:
            flash('Old password does not match current password', 'error')
            return redirect(url_for('updateinfo'))  # Redirect to updateinfo page on password error
    
    # Fetch user info and render updateProfile.html
    cursor.execute('SELECT * FROM profileinfo WHERE email = %s and password = %s',
                   (session['email'], session['password']))
    info = list(cursor.fetchone())
    id, prof_pic, fullname, age, address, gender, birthday, contact, email = info[:9]
    
    return render_template("updateProfile.html", ref_id=id, pic=prof_pic, name=fullname, age=age, address=address,
                           gender=gender, bday=birthday, number=contact, email=email)

        
        
@app.route('/deleteacc')
def deleteacc():
    cursor.execute('DELETE FROM profileinfo WHERE email = %s and password = %s',
                   (session['email'], session['password']))
    conn.commit()
    session.pop('email')
    flash('Account has been deleted!!', 'success')
    return redirect(url_for('land'))


@app.route('/deleterec',methods=["POST", "GET"])
def deleterec():
    row_number = int(request.form['row_number'])
    cursor.execute('DELETE FROM records WHERE id=%s',(row_number))
    conn.commit()
    return redirect(url_for('records'))

    
    
@app.route('/sign_out')
def sign_out():
    session.pop('email')
    return redirect(url_for('land'))

    



if __name__ == "__main__":
    app.run(debug=True, port=5001)