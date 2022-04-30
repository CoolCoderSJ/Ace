import os
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
    decks = ref.get()

    return render_template("index.html", decks=decks)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if not "user" in session.keys():
        return redirect("/signup")

    if request.method == "GET":
        return render_template("add.html")
    
    else:
        ref = db.reference(session['user'])
        decks = ref.get()

        form = request.form

        deck = {
            "name": form['name'],
            "description": form['description'],
            "created": form['created'],
            "cards": []
        }

        for k, v in form.items():
            if k != "name" and k != "description" and k != "created":
                deck['cards'].append({
                    "term": k,
                    "description": v,
                    "starred": False
                })

        decks.append(deck)
        ref.set(decks)

        return redirect(f"/deck/{len(decks)}")


@app.route("/edit/<deckId>", methods=['GET', 'POST'])
def edit(deckId):
    if not "user" in session.keys():
        return redirect("/signup")

    if request.method == "GET":
        ref = db.reference(session['user'])
        decks = ref.get()
        deck = decks[deckId]

        return render_template("edit.html", deck=deck)
    
    else:
        ref = db.reference(session['user'])
        decks = ref.get()

        form = request.form

        deck = {
            "name": form['name'],
            "description": form['description'],
            "created": form['created'],
            "cards": []
        }

        for k, v in form.items():
            if k != "name" and k != "description" and k != "created":
                deck['cards'].append({
                    "term": k,
                    "description": v,
                    "starred": False
                })

        decks[deckId] = deck
        ref.set(decks)

        return redirect(f"/deck/{deckId}")


@app.route("/delete/<deckId>", methods=['DELETE'])
def delete(deckId):
    if not "user" in session.keys():
        return redirect("/signup")
    ref = db.reference(session['user'])
    decks = ref.get()
    del decks[deckId]
    ref.set(decks)

    return redirect(f"/")

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