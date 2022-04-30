import os, datetime
from flask import *
from flask_session import Session
import requests

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from firebase_admin import exceptions


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = r's\xb6%\x99\x8d2\n\x84=Y5H\x0c\'^\xfb>\x86\xa4\xbe"\n\xf9r'

cred_obj = credentials.Certificate("firebase_cred.json")
fire = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': "https://ace-39874-default-rtdb.firebaseio.com"
	})

def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
        params={
            "key": os.environ['FIREBASE_API_KEY']
        },
        data=payload
        )

    return r.json()

@app.route("/")
def index():
    if not "user" in session.keys():
        return redirect("/signup")

    ref = db.reference(session['user'])
    tasks = ref.get()

    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    if not "user" in session.keys():
        return redirect("/signup")

    ref = db.reference(session['user'])
    tasks = ref.get()
    
    title = request.form.get("title")
    sports = ['badminton', 'basketball', 'cricket', 'football', 'rugby', 'tennis', 'volleyball', 'bowling', 'baseball', 'golf', 'hockey', 'soccer', 'swimming', 'table tennis', 'weightlifting', 'boxing', 'gymnastics', 'karate', 'martial arts', 'taekwondo', 'wrestling', 'yoga', 'sport']
    instruments = ['piano', 'saxophone', 'clarinet', 'violin', 'flute', 'trumpet', 'baritone', 'french horn', 'trombone', 'drum', 'mallet', 'xylophone', 'viola', 'cello', 'orchestra', 'band', 'chorus', 'music']
    education = ['test', 'quiz', 'hw', 'homework', 'assignment', 'class']

    sets = [sports, instruments, education]

    titleWords = title.split(" ")
    customText = ""
    itemType = ""

    while 1:
        for item in sets:
            matches = list(set(item).intersection(titleWords)) 
            if matches:
                if item == sports:
                    itemType = "sports"
                    if matches[0] != "sport":
                        customText = f"Remember to practice {matches[0]}!"
                if item == instruments:
                    itemType = "instruments" 
                    if matches[0] != "music" and matches[0] != "orchestra" and matches[0] != "band" and matches[0] != "chorus":
                        customText = f"Remember play your {matches[0]}!"
                if item == education:
                    itemType = "education"
                    customText = f"Remember to study for your {matches[0]}!"
                break
    
    task = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "createdAt": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "type": itemType,
        "reminders": [
        ]
    }

    for k, v in request.form.items():
        if k != "title" and k != "description":
            task["reminders"].append({
                "time": v,
                "customText": customText
            })

    tasks.append(task)
    ref.set(tasks)

    return redirect('/')

@app.route("/edit/<id>", methods=["POST"])
def edit(id):
    if not "user" in session.keys():
        return redirect("/signup")

    ref = db.reference(session['user'])
    tasks = ref.get()
    
    title = request.form.get("title")
    sports = ['badminton', 'basketball', 'cricket', 'football', 'rugby', 'tennis', 'volleyball', 'bowling', 'baseball', 'golf', 'hockey', 'soccer', 'swimming', 'table tennis', 'weightlifting', 'boxing', 'gymnastics', 'karate', 'martial arts', 'taekwondo', 'wrestling', 'yoga', 'sport']
    instruments = ['piano', 'saxophone', 'clarinet', 'violin', 'flute', 'trumpet', 'baritone', 'french horn', 'trombone', 'drum', 'mallet', 'xylophone', 'viola', 'cello', 'orchestra', 'band', 'chorus', 'music']
    education = ['test', 'quiz', 'hw', 'homework', 'assignment', 'class']

    sets = [sports, instruments, education]

    titleWords = title.split(" ")
    customText = ""
    itemType = ""

    while 1:
        for item in sets:
            matches = list(set(item).intersection(titleWords)) 
            if matches:
                if item == sports:
                    itemType = "sports"
                    if matches[0] != "sport":
                        customText = f"Remember to practice {matches[0]}!"
                if item == instruments:
                    itemType = "instruments" 
                    if matches[0] != "music" and matches[0] != "orchestra" and matches[0] != "band" and matches[0] != "chorus":
                        customText = f"Remember play your {matches[0]}!"
                if item == education:
                    itemType = "education"
                    customText = f"Remember to study for your {matches[0]}!"
                break
    
    task = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "createdAt": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "type": itemType,
        "reminders": [
        ]
    }

    for k, v in request.form.items():
        if k != "title" and k != "description":
            task["reminders"].append({
                "time": v,
                "customText": customText
            })

    tasks[id] = task
    ref.set(tasks)

    return redirect('/')

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    if not "user" in session.keys():
        return redirect("/signup")

    ref = db.reference(session['user'])
    tasks = ref.get()
    del tasks[id]
    ref.set(tasks)

    return redirect('/')

@app.route("/signup")
def signup():
    if request.method == "GET":
        error = request.args.get("error")
        return render_template("signup.html", error=error)
    else:
        try:
            form = request.form
            email = form["email"]
            username = form["username"]
            password = form["password"]

            user = auth.create_user(email=email, password=password, display_name=username)
            userId = user.uid
            
            session['user'] = userId
            return redirect("/")

        except exceptions.FirebaseError as e:
            return redirect(f"https://hours.mathlings.org/signup?error={e}")
        
@app.route("/login")
def login():
    if request.method == "GET":
        error = request.args.get("error")
        return render_template("login.html", error=error)
    else:
        form = request.form
        email = form["email"]
        password = form["password"]

        resp = sign_in_with_email_and_password(email, password)
        if "error" not in resp:
            user = auth.get_user_by_email(email)
            userId = user.uid
            
            session['user'] = userId
            return redirect("/")

        else:
            e = resp["error"]['message']
            return redirect(f"https://hours.mathlings.org/signup?error={e}")
            
        

app.run(host='0.0.0.0', port=8080)