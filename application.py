import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# index.html contains the login/sign-up forms
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def login():
    Username = request.form.get('username')
    Password = request.form.get('password')

    # Check all the usernames in the user_profile table if it can locate the (request form input = username)
    # Return only the id and 1 row since there should be no duplicate usernames in the database (for faster query)
    query = "SELECT id FROM userprofile WHERE username='{}'".format(Username)
    checkusername = db.execute(query).fetchone()

    # SUCCESS : Proceed for password checking
    # FAIL : Return a "User does not exist" error
    if checkusername is not None:

        # Check if there's a match in the password by extending the query and run again
        query += "AND password='{}'".format(Password)
        checkpassword = db.execute(query).fetchone()

        # SUCCESS : Successful login move to home.html
        # FAIL : Return an "Incorrect Password" error
        if checkpassword is not None:
            return render_template('home.html', Username=Username)
        else:
            return render_template('index.html', Error='Incorrect Password')
    else:
        return render_template('index.html', Error='User does not exist')
