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
    placeholder = ref.get()

    return render_template("index.html", placeholder=placeholder)


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