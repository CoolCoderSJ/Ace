# Ace

Many task keeper and reminder apps already exist, but are usually complicated, or filled with too many features to use. Ace is a minimalistic task manager and reminder app that is easy to use and has a clean and simple interface. With Ace, you can create a task and set a task type, and Ace will take care of the rest. If you enable notifications for your tasks, Ace will send you a notification to your devices every day for a few days based on your task to keep you on track.


## Getting Started
- You can visit an instance of Ace currently running [here](https://ace.coolcodersj.repl.co/), or by going to https://ace.coolcodersj.repl.co/.
- Start by signing up with an email and password
- Allow Ace to send you notifications so that you can keep track of your tasks
- ![image](https://sjcdn.is-a.dev/file/vftukt)
- Click the `Add something new...` button
- ![image](https://sjcdn.is-a.dev/file/eippdl)
- Fill in the fields 
- That's it! Ace will remind you when it's time


## Tools Used
- Python/Flask
    - Used for making the backend for the web server
- PYwebpush
    - Used for sending push notifications
- Bootstrap, MDBootstrap
    - Used for making and styling the web page
- Firebase
    - Used for authentication, the database, and accessing push notification certificates
- SocketIO
    - Used so that the page doesnt need to reload when the user allows notifications
- APSCheduler
    - Used for scheduling the task notification checks
- Bootstrap Studio
    - Used for the initial wireframing of the pages

## Self Hosting
Ace uses Firebase for its authentication and database. To get started, head over to [Firebase](https://firebase.google.com/) and click `Get Started`. 
- Click `Add Project`
- Enter a name for your project and click `Continue`
- Ace did not use the analytics firebase provides, so you can disable the toggle then click Create Project
- When your project has been created, click `Continue`

___

- Start by going to the Authentication tab on the left
- ![image](https://sjcdn.is-a.dev/file/pyycdq)
- Click `Get Started`
- The screen should open to the `Sign-in method` tab
- Here, click `Email/password`
- Enable the first toggle, and leave the second one untoggled
- ![image](https://sjcdn.is-a.dev/file/vquixa)
- Click `Save`
- Next, on the left where you clicked `Authentication`, click `Realtime Database`
- Click ` Create Database`
- Click `Next`
- Select the `start in test mode` option and click `Enable`
- Copy the database URL that shows on the screen, it should look something like ` https://project-id-default-rtdb.firebaseio.com`
- On line 29 of the code in the file `main.py` of this repository, replace the database URL with the one you copied
- Now, go back to Firebase, and click the settings cog next to `Project Overview`
- Click `Project Settings`
- Copy the `Web API Key`
- Set an environment variable that your app can read, and name the variable `FIREBASE_API_KEY`. Set the value of the variable to the `Web API Key` you copied.

___

- You also need Firebase credentials for this project.
- In the project settings, click the `Service accounts` tab
- Scroll down to where you see the `Generate new private key` button, and click it
- Click `Generate key`
- Firebase downloads your credentials as a file after this step
- Rename this file to `firebase_cred.json` and move it to your project directory root

___

- Finally, you need to setup your push notification credentials
- Go to the `Cloud Messaging` tab in your Firebase project settings
- Scroll down to the `Web Push Certificates` section and click `Generate key pair`
- Copy the value that comes up underneath the `key pair` table header
- In the `/templates/index.html` file on line 55, replace the public key value with the value you just copied
- Back in your firebase settings, next to the table entry for your key pair, click the three dots and click `Show private key`
- Copy the value
- Make a new environment variable for your project
    - Name the variable `VAPID`, and set the value to the private key you just copied

___

- That should be it for all of the Firebase configuration.
- Now, install Python from the website found [here](https://www.python.org/downloads/)
- In your command prompt/terminal, navigate to the root of the directory of the project
- Install all of the required dependencies by running `pip install -r requirements.txt`
- Run the file with python
    - Windows Command Prompt: `python main.py`
    - macOS Terminal: `python3 main.py`

- Navigate to https://localhost:5000/