from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth, OAuthException
from flask.ext.mail import Mail, Message
import datetime
import requests
import json

from keys import DrChrono_APP_ID, DrChrono_APP_SECRET

base = "https://drchrono.com"
patien = "/api/patients"
userdat = None # (access_token ,refresh_token , expires_timestamp)
useracct = None # (username, isdoctor, docnum, isstaff)

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

accesstoken = ""


oauth = OAuth(app)

DrChrono = oauth.remote_app(
    'DrChrono',
    consumer_key=DrChrono_APP_ID,
    consumer_secret=DrChrono_APP_SECRET,
    access_token_url='https://drchrono.com/o/token/',
    access_token_method='GET',
    authorize_url='https://drchrono.com/o/authorize/'
)


@app.route('/')
def index():
    return render_template('index.html')
    #return redirect(url_for('login'))

@app.route('/login')
def login():
    callback = url_for(
        'DrChrono_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return DrChrono.authorize(callback=callback)

@app.route('/login/authorized')
def DrChrono_authorized():

    if 'error' in request.args:
        return 'An Error occured during Authentication'

    accesscode = request.args.get('code')
    print(accesscode)
    r = requests.post('https://drchrono.com/o/token/', data={
        'code': accesscode,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:5000/login/authorized',
        'client_id': 'Ml395hDo9JI4qypj57l2hWeTJWzVPEVr5If1mz2A',
        'client_secret': 'jDdNxRuGs749TdhkhdmA4YCXMQFBkRvhbQoOKp4hex12eOAbda1hABxbJI4s4iJ0RqHxks5GFWFOafOzFJZY9dDtnf85ugnLId7Rysi1jUhPq7PXFRlzO8WETASAP0qO',
    })

    data = json.dumps(r.json(), indent=4)
    access_token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']
    expires_timestamp = str(r.json()['expires_in'])
    
    global userdat
    userdat = (access_token ,refresh_token , expires_timestamp)

    return redirect(url_for('account'))
    #return str( ' '.join(i+" " for i in userdat))

@app.route('/account')
def account():
    global useracct

    if(userdat == None):
        return redirect(url_for('index'))
    if(useracct == None):
        set_doctor_name()


    output = "Logged in as"
    if(useracct[1]):
        output += " Dr. "
    output += useracct[0]

    return render_template('account.html', get_patients=get_patients, format_user=(get_name, get_birth_date, get_photo_url, get_email) )

def set_doctor_name():
    global useracct

    users_url = 'https://drchrono.com/api/users'
    headers = {
    'Authorization': 'Bearer '+ userdat[0],
    }

    r = requests.get(users_url, headers=headers).json()
    un = r['results'][0]['username']
    idoc = r['results'][0]['is_doctor']
    docnum = r['results'][0]['doctor']
    staff = r['results'][0]['is_staff']
    useracct = (un, idoc, docnum, staff)
    return 

def get_photo_url(patient):
    photourl = patient['patient_photo']
    if(photourl == None or True):
        if(patient['gender'] == None or patient['gender'] == 'Male' ):
            photourl = "static/assets/img/generic_male.jpg"
        else:
            photourl = "static/assets/img/generic_female.jpg"
    return photourl

def get_birth_date(patient):
    return patient['date_of_birth']

def get_name(patient):
    output = patient['first_name'] 
    midd = patient['middle_name']
    if(midd != '' and midd != None):
        output += " "+midd
    output += " "+patient['last_name']
    return output 

def get_contact(patient):
    return patient['']

def get_email(patient):
    return patient['email']

def format_user(patient):
    print(patient['last_name'])
    return patient['last_name']

def get_patients():
    global userdat
    if(userdat == None):
        return redirect(url_for('index'))
    headers = {
    'Authorization': 'Bearer '+ userdat[0],
    }

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        r = requests.get(patients_url, headers=headers).json()
        patients.append(r['results'])
        patients_url = r['next'] # A JSON null on the last page
    print(patients[0])
    pat = patients[0]
    return pat



@DrChrono.tokengetter
def get_DrChrono_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()