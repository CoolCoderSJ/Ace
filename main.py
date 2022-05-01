import os, datetime, json
from flask import *
from flask_session import Session
import requests

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import auth
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

    htmlTasks = []

    i = 0

    if tasks:
        for task in tasks:
            if task['type'] == "2" or task['type'] == "3" or task['type'] == "7":
                keywordbased = True
            else:
                keywordbased = False
        
            if keywordbased:
                message = f"Ace detected specific keywords that made it believe a {len(task['reminders'])} day reminder period would be best. You will be reminded each day for {len(task['reminders'])} days before the day of the task, as well as the day of the task."
            else: 
                message = f"Ace did not detect any specific keywords to determine a proper reminder time period. You will be reminded each day for 2 days before the day of the task, as well as the day of the task."
                
            htmlTasks.append({
                "id": i,
                "title": task['title'],
                "description": task['description'],
                "time": task['timedue'],
                "message": task['message'],
            })
            i += 1

    
    return render_template("index.html", tasks=htmlTasks)

@app.route("/complete/<id>", methods=['POST'])
def complete(id):
    ref = db.reference(session['user'])
    tasks = ref.get()

    for task in tasks:
        if task['id'] == id:
            ref.child(task['id']).update({
                "completed": True
            })

    return redirect("/")

@app.route("/uncomplete/<id>", methods=['POST'])
def uncomplete(id):
    ref = db.reference(session['user'])
    tasks = ref.get()

    for task in tasks:
        if task['id'] == id:
            ref.child(task['id']).update({
                "completed": False
            })

    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add():
    if not "user" in session.keys():
        return redirect("/signup")

    if request.method == "GET":
        return render_template("add.html")
        
    else:
        ref = db.reference(session['user'])
        tasks = ref.get()

        
        title = request.form.get("title")
        reminders = []

        days_7 = ['test', 'quiz', 'concert', 'project']
        days_3 = ['match', 'game', 'competition', 'contest', 'tournament', 'event']
        days_2 = ['piano', 'saxophone', 'clarinet', 'violin', 'flute', 'trumpet', 'baritone', 'french horn', 'trombone', 'drum', 'mallet', 'xylophone', 'viola', 'cello', 'orchestra', 'band', 'chorus', 'badminton', 'basketball', 'cricket', 'football', 'rugby', 'tennis', 'volleyball', 'bowling', 'baseball', 'golf', 'hockey', 'soccer', 'swimming', 'table tennis', 'weightlifting', 'boxing', 'gymnastics', 'karate', 'martial arts', 'taekwondo', 'wrestling', 'yoga']


        titleWords = title.split(" ")
        itemType = ""

        matchfor7 = list(set(days_7).intersection(titleWords)) 
        if matchfor7:
            itemType = "7"
            if matchfor7[0] == "test" or matchfor7[0] == "quiz":
                reminders.append({
                    "time": "-07:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-06:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-05:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-04:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-03:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-02:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-01:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-00:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })
            elif matchfor7[0] == "concert":
                reminders.append({
                    "time": "-07:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-06:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-05:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-04:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-03:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-02:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-01:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-00:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })
            else:
                reminders.append({
                    "time": "-07:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-06:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-05:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-04:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-03:00:00:00",
                    "customText": f"Are you sure your {matchfor7[0]} is ready?"
                })
                reminders.append({
                    "time": "-02:00:00:00",
                    "customText": f"Are you sure your {matchfor7[0]} is ready?"
                })
                reminders.append({
                    "time": "-01:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]} submission!"
                })
                reminders.append({
                    "time": "-00:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })

        matchfor3 = list(set(days_3).intersection(titleWords)) 
        if matchfor3:
            itemType = "3"
            reminders.append({
                "time": "-03:00:00:00",
                "customText": f"You have a {matchfor3[0]} coming up, make sure to prepare!"
            })
            reminders.append({
                "time": "-02:00:00:00",
                "customText": f"You have a {matchfor3[0]} coming up, make sure to prepare!"
            })
            reminders.append({
                "time": "-01:00:00:00",
                "customText": f"Good luck with your {matchfor3[0]}!"
            })
            reminders.append({
                "time": "-00:00:00:00",
                "customText": f"Good luck with your {matchfor3[0]}!"
            })

        matchfor2 = list(set(days_2).intersection(titleWords)) 
        if matchfor2:
            itemType = "2"
            reminders.append({
                "time": "-02:00:00:00",
                "customText": f"Make sure to practice your {matchfor2[0]}!"
            })
            reminders.append({
                "time": "-01:00:00:00",
                "customText": f"Make sure to practice your {matchfor2[0]}!"
            })
            reminders.append({
                "time": "-00:00:00:00",
                "customText": f"Make sure to practice your {matchfor2[0]}!"
            })
        
        if reminders == []:
            itemType = ""
            reminders.append({
                "time": "-02:00:00:00",
                "customText": ""
            })
            reminders.append({
                "time": "-01:00:00:00",
                "customText": ""
            })
            reminders.append({
                "time": "-00:00:00:00",
                "customText": ""
            })
            
        
        task = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "completed": False,
            "timedue": request.form.get("timedue"),
            "type": itemType,
            "reminders": reminders,
        }

        if not tasks:
            ref = db.reference("/")
            existing = ref.get()
            if not existing:
                existing = {}
            existing[session['user']] = [task]
            ref.set(existing)
        
        else:
            tasks.append(task)
            ref.set(tasks)

        return redirect('/')

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    id = int(id)

    if not "user" in session.keys():
        return redirect("/signup")

    if request.method == "GET":
        ref = db.reference(session['user'])
        tasks = ref.get()
        task = tasks[id]

        htmlTask = {
            "title": task["title"],
            "description": task["description"],
            "timedue": task["timedue"],
            "id": id
        }
        return render_template("edit.html", task=htmlTask)

    else:
        ref = db.reference(session['user'])
        tasks = ref.get()
        
        title = request.form.get("title")
        reminders = []

        days_7 = ['test', 'quiz', 'concert', 'project']
        days_3 = ['match', 'game', 'competition', 'contest', 'tournament', 'event']
        days_2 = ['piano', 'saxophone', 'clarinet', 'violin', 'flute', 'trumpet', 'baritone', 'french horn', 'trombone', 'drum', 'mallet', 'xylophone', 'viola', 'cello', 'orchestra', 'band', 'chorus', 'badminton', 'basketball', 'cricket', 'football', 'rugby', 'tennis', 'volleyball', 'bowling', 'baseball', 'golf', 'hockey', 'soccer', 'swimming', 'table tennis', 'weightlifting', 'boxing', 'gymnastics', 'karate', 'martial arts', 'taekwondo', 'wrestling', 'yoga']


        titleWords = title.split(" ")
        itemType = ""

        matchfor7 = list(set(days_7).intersection(titleWords)) 
        if matchfor7:
            itemType = "7"
            if matchfor7[0] == "test" or matchfor7[0] == "quiz":
                reminders.append({
                    "time": "-07:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-06:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-05:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-04:00:00:00",
                    "customText": f"Make sure to study for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-03:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-02:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-01:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })
            elif matchfor7[0] == "concert":
                reminders.append({
                    "time": "-07:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-06:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-05:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-04:00:00:00",
                    "customText": f"Make sure to practice for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-03:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-02:00:00:00",
                    "customText": f"Are you sure you're ready for your {matchfor7[0]}?"
                })
                reminders.append({
                    "time": "-01:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]}!"
                })
            else:
                reminders.append({
                    "time": "-07:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-06:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-05:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-04:00:00:00",
                    "customText": f"Make sure to finish for your {matchfor7[0]}!"
                })
                reminders.append({
                    "time": "-03:00:00:00",
                    "customText": f"Are you sure your {matchfor7[0]} is ready?"
                })
                reminders.append({
                    "time": "-02:00:00:00",
                    "customText": f"Are you sure your {matchfor7[0]} is ready?"
                })
                reminders.append({
                    "time": "-01:00:00:00",
                    "customText": f"Good luck with your {matchfor7[0]} submission!"
                })

        matchfor3 = list(set(days_3).intersection(titleWords)) 
        if matchfor3:
            itemType = "3"
            reminders.append({
                "time": "-03:00:00:00",
                "customText": f"You have a {matchfor3[0]} coming up, make sure to prepare!"
            })
            reminders.append({
                "time": "-02:00:00:00",
                "customText": f"You have a {matchfor3[0]} coming up, make sure to prepare!"
            })
            reminders.append({
                "time": "-01:00:00:00",
                "customText": f"Good luck with your {matchfor3[0]}!"
            })

        matchfor2 = list(set(days_2).intersection(titleWords)) 
        if matchfor2:
            itemType = "2"
            reminders.append({
                "time": "-02:00:00:00",
                "customText": f"Make sure to practice your {matchfor2[0]}!"
            })
            reminders.append({
                "time": "-01:00:00:00",
                "customText": f"Make sure to practice your {matchfor2[0]}!"
            })
        
        if reminders == []:
            itemType = ""
            reminders.append({
                "time": "-02:00:00:00",
                "customText": ""
            })
            reminders.append({
                "time": "-01:00:00:00",
                "customText": ""
            })
            
        
        task = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "completed": False,
            "timedue": request.form.get("timedue"),
            "type": itemType,
            "reminders": reminders,
        }

        tasks[id] = task

        ref.set(tasks)

    return redirect('/')

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    id = int(id)
    if not "user" in session.keys():
        return redirect("/signup")

    ref = db.reference(session['user'])
    tasks = ref.get()
    del tasks[id]
    ref.set(tasks)

    return redirect('/')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        error = request.args.get("error")
        return render_template("signup.html", error=error)
    else:
        try:
            form = request.form
            email = form["email"]
            password = form["password"]

            user = auth.create_user(email=email, password=password)
            userId = user.uid

            
            session['user'] = userId
            return redirect("/")

        except exceptions.FirebaseError as e:
            return redirect(f"https://Ace.coolcodersj.repl.co/signup?error={e}")
        
@app.route("/login", methods=['GET', 'POST'])
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
            return redirect(f"https://Ace.coolcodersj.repl.co/login?error={e}")
            
        

app.run(host='0.0.0.0', port=8080)