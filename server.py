# -*- coding: utf-8 -*-

import os
import flask
import requests
import random
import json
import pickle
from datetime import datetime, timedelta, date
import pytz
from tzlocal import get_localzone

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from oauth2client.client import GoogleCredentials
from oauth2client import GOOGLE_TOKEN_URI

from googleapiclient.discovery import build
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "/home/ganrot/mysite/client_id.json"



# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

app = flask.Flask(__name__, template_folder='template')
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

class User:
    def __init__(self, id, email, givenAccess):
        self.id = id
        self.email = email
        self.givenAccess = givenAccess

class Payload(object):
     def __init__(self, j):
        self.__dict__ = json.loads(j)


def findUser(users, userId):
    for user in users:
        print(user)
        if user.id == userId:
            return user
    return None

def allHasAccepted(users):

    for user in users:
        if user.givenAccess == False:
            return False
    return True


def findDate(users, meetingDate):

    d = datetime.strptime(meetingDate, "%Y-%m-%d").date()
    d = datetime.combine(d, datetime.min.time())

    if d.date() == datetime.today().date():

        currentTime = datetime.today() + timedelta(hours=2)#ad hours for timezone offset
        futureTime = currentTime + timedelta(hours=1)
        h = futureTime.time().hour

        d = d.replace(hour=h, minute=0, second=0, microsecond=0)
    else:
        d = d.replace(hour=8, minute=0, second=0, microsecond=0)


    while True:
        foundDate = True
        print("checking date: ", str(d), d.weekday())
        for user in users:
            creds = None
            with open('mysite/pickles/' + user.email +'_token.pickle', 'rb') as token:
                creds = pickle.load(token)

                s = build('calendar', 'v3', credentials=creds)

                lowerTime = d.isoformat() + '+02:00'
                upperTime = d + timedelta(hours=1)
                upperTime = upperTime.isoformat() + '+02:00'

                events_result = s.events().list(calendarId='primary', timeMin = lowerTime, timeMax = upperTime,
                                                    maxResults=10, singleEvents=True,
                                                    orderBy='startTime').execute()
                events = events_result.get('items', [])

                if len(events) > 0:
                    foundDate = False

        if foundDate:
            break
        else:
            #if day is about to end, change date and make sure it is not a saturday or sunday
            if d.hour >= 16:
                while True:
                    d = d.replace(hour=8)
                    d += timedelta(days=1)

                    if d.weekday() != 5 and d.weekday() != 6:
                        #print("weekday:", str(d.weekday()))
                        break

            else:
                #Lunch is at 12 so if clock is about to hit 12 skip forward to 13
                if d.hour == 11:
                    d += timedelta(hours=2)
                else:
                    d += timedelta(hours=1)

    # create meeting event for all users
    print("the final settled date and time is:", d)
    for user in users:
        creds = None
        with open('mysite/pickles/' + user.email +'_token.pickle', 'rb') as token:

            creds = pickle.load(token)

            calender = googleapiclient.discovery.build(
                API_SERVICE_NAME, API_VERSION, credentials=creds, cache_discovery=False)


            min = d - timedelta(hours=2) #remove 2 hours due to timezone offset
            max = min + timedelta(hours=1)
            event = {
              'summary': 'Meeting',
              'location': 'Karlstad',
              'description': 'A test meeting.',
              'start': {
                  'dateTime': min.isoformat() + 'Z',
              },
              'end': {
                  'dateTime': max.isoformat() + 'Z',
              }}

            result = calender.events().insert(calendarId='primary', body=event).execute()

def sendEmail(user, meetingid):
    print("Sending mail to: ", user.email)
    invitationURL = 'http://ganrot.pythonanywhere.com/joinmeeting?meetingId=' + str(meetingid) + '&userId=' + str(user.id)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("chatbot.demo4@gmail.com", "rasa1234")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = 'Project invitation'
    msg.attach(MIMEText('Click here to join the meeting: ' + invitationURL, "plain", "utf-8"))

    server.sendmail("chatbot.demo4@gmail.com", user.email, msg.as_string().encode('ascii'))
    server.quit()

@app.route('/')
def index():
  return print_index_table()


@app.route('/test')
def test_api_request():

  if flask.request.args["minDate"] != None and flask.request.args["maxDate"] != None:
      flask.session["minDate"] = flask.request.args["minDate"]
      flask.session["maxDate"] = flask.request.args["maxDate"]

  if 'credentials' not in flask.session:
    return flask.redirect('authorize')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  calender = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials, cache_discovery=False)

  event = {
  'summary': 'Summary',
  'location': 'Karlstad',
  'description': 'A test event.',
  'start': {
      'dateTime': flask.session.get('minDate').replace(" ", "+"),
  },
  'end': {
      'dateTime': flask.session.get('maxDate').replace(" ", "+"),
  }}

  result = calender.events().insert(calendarId='primary', body=event).execute()

  calendars = calender.calendarList().list().execute()

  return "Vacation has been added to your calender"


@app.route('/authorize')
def authorize():

  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.

  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  authorization_response = authorization_response.replace('http', 'https')

  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials

  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.redirect(flask.url_for('test_api_request'))



@app.route('/createmeeting')
def invitegrouptomeeting():

    emails = flask.request.args.getlist("email")
    meetingDate = flask.request.args["meetingDate"]
    users = []


    meetindId = random.randint(0,100000)

    for i, email in enumerate(emails):
        u = User(i, email, False)
        users.append(u)

        sendEmail(u, meetindId)

    with open('mysite/meetings/meeting_'+str(meetindId) + '.json', 'w') as f:


        d = {}
        d["users"] = [ob.__dict__ for ob in users]
        d["meetingDate"] = meetingDate

        f.write(json.dumps(d))

    return "I created a meeting for you with the id: " + str(meetindId)

@app.route('/joinmeeting')
def joinmeeting():

    if 'meetingId' in flask.request.args and 'userId' in flask.request.args:
        flask.session["meetingId"] = flask.request.args["meetingId"]
        flask.session["userId"] = flask.request.args["userId"]

    if 'credentials' not in flask.session:
        return flask.redirect('authorizejoinmeeting')


    with open('mysite/meetings/meeting_'+str(flask.session.get('meetingId')) + '.json', 'r') as f:
        data = json.load(f)

    user_data = data["users"]
    meetingDate = data["meetingDate"]

    users = []
    for obj in user_data:
        users.append(User(obj['id'], obj['email'], obj['givenAccess']))

    user = next((x for x in users if x.id == int(flask.session.get('userId'))), None)
    user.givenAccess = True

    with open('mysite/meetings/meeting_'+str(flask.session.get('meetingId')) + '.json', 'w') as f:

        d = {}
        d["users"] = [ob.__dict__ for ob in users]
        d["meetingDate"] = meetingDate

        f.write(json.dumps(d))


    credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

    with open('mysite/pickles/' + user.email + '_token.pickle', 'wb') as token:
        pickle.dump(credentials, token)



    if allHasAccepted(users) == True:
        findDate(users, meetingDate)



    return "You have joined"


@app.route('/authorizejoinmeeting')
def authorizejoinmeeting():

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  flow.redirect_uri = flask.url_for('oauth2callbackjoinmeeting', _external=True)

  authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')

  flask.session['state'] = state

  return flask.redirect(authorization_url)


@app.route('/oauth2callbackjoinmeeting')
def oauth2callbackjoinmeeting():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.

  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

  flow.redirect_uri = flask.url_for('oauth2callbackjoinmeeting', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  authorization_response = authorization_response.replace('http', 'https')

  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  print("creds is type of:", type(credentials))
  flask.session['credentials'] = credentials_to_dict(credentials)
  print("token:", flask.session.get('credentials').get('token'))
  print("refresh_token: ", flask.session.get('credentials').get('refresh_token'))
  print("client_id:", flask.session.get('credentials').get('client_id'))
  print("client_secret:", flask.session.get('credentials').get('client_secret'))
  print("token_uri:", flask.session.get('credentials').get('token_uri'))

  gCreds = GoogleCredentials(
    flask.session.get('credentials').get('token'),
    flask.session.get('credentials').get('client_id'),
    flask.session.get('credentials').get('client_secret'),
    flask.session.get('credentials').get('refresh_token'),
    None,
    flask.session.get('credentials').get('token_uri'),
    'Python client library',
    revoke_uri=None
    )


  return flask.redirect(flask.url_for('joinmeeting'))












@app.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')


@app.route("/google4a1709dbe9a56ce1.html", methods=["GET", "POST"])
def upload_image():
    print("hej")
    return flask.render_template("google4a1709dbe9a56ce1.html")


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  #app.run('http://ganrot.pythonanywhere.com/', 8080, debug=True)
