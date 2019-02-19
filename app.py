from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, System, GameItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps



app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "System Game Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///systemgamewithusers.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function

def getAllSystems():
    systems = session.query(System).all()
    return systems


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase+string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# google oauth


@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade auth code'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # is access_token valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # store the result of request
    result = json.loads(h.request(url, 'GET')[1])
    # if result contains any errors the message is sent to server
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # verify if this the right access_token
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps('Users ids do not match'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # is this token was issued for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps('Token id does not match app id'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # checks is the user already logged in not to reset all info
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    return output


@app.route('/gdisconnect/')
def gdisconnect():
    access_token = login_session.get('access_token')
    print access_token
    if access_token is None:
        response = make_response(json.dumps('User is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['picture']
        del login_session['email']
        response = make_response(json.dumps("You are disconnected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/system')
    else:
        response = make_response(json.dumps("Error occured"), 400)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/system')


# User helper functions

def createUser(login_session):
    user = User(name=login_session['username'],
                email=login_session['email'],
                picture=login_session['picture'])
    session.add(user)
    session.commit()
    user_db = session.query(User).filter_by(email=login_session['email']).one()
    return user_db.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# JSON APIs to view System Information


@app.route('/system/<int:system_id>/game/JSON')
def systemGameJSON(system_id):
    system = session.query(System).filter_by(id=system_id).one()
    items = session.query(GameItem).filter_by(
        system_id=system_id).all()
    return jsonify(GameItems=[i.serialize for i in items])


@app.route('/system/<int:system_id>/game/<int:game_id>/JSON')
def gameItemJSON(system_id, game_id):
    Game_Item = session.query(GameItem).filter_by(id=game_id).one()
    return jsonify(Game_Item=Game_Item.serialize)


@app.route('/system/JSON')
def systemsJSON():
    systems = session.query(System).all()
    return jsonify(systems=[r.serialize for r in systems])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Show all systems
@app.route('/')
@app.route('/system/')
def showSystems():
    systems = session.query(System).order_by(asc(System.name))
    if 'username' not in login_session:
        return redirect('/login')
    else:
        return render_template('systems.html', systems=systems)

# Create a new system


@app.route('/system/new/', methods=['GET', 'POST'])
def newSystem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newSystem = System(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newSystem)
        flash('New System %s Successfully Created' % newSystem.name)
        session.commit()
        return redirect(url_for('showSystems'))
    else:
        return render_template('newSystem.html')

# Edit a system

@login_required
@app.route('/system/<int:system_id>/edit/', methods=['GET', 'POST'])
def editSystem(system_id):
    editedSystem = session.query(
        System).filter_by(id=system_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedSystem.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized "
                "to edit this system. Please create your own system in order "
                "to edit.');}</script><body onload='myFunction()'>")
    if request.method == 'POST':
        if request.form['name']:
            editedSystem.name = request.form['name']
            flash('System Successfully Edited %s' % editedSystem.name)
            return redirect(url_for('showSystems'))
    else:
        return render_template('editSystem.html', system=editedSystem)


# Delete a system
@login_required
@app.route('/system/<int:system_id>/delete/', methods=['GET', 'POST'])
def deleteSystem(system_id):
    systemToDelete = session.query(
        System).filter_by(id=system_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if systemToDelete.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized"
                "to delete this system. Please create your own system in order"
                "to delete.');}</script><body onload='myFunction()'>")
    if request.method == 'POST':
        session.delete(systemToDelete)
        flash('%s Successfully Deleted' % systemToDelete.name)
        session.commit()
        return redirect(url_for('showSystems', system_id=system_id))
    else:
        return render_template('deleteSystem.html', system=systemToDelete)

# Show a system game


@app.route('/system/<int:system_id>/')
@app.route('/system/<int:system_id>/game/')
def showGame(system_id):
    system = session.query(System).filter_by(id=system_id).one()
    creator = getUserInfo(system.user_id)
    items = session.query(GameItem).filter_by(
        system_id=system_id).all()
    if ('username' not in login_session or
       creator.id != login_session['user_id']):
        return render_template('publicgame.html',
                               items=items, system=system, creator=creator)
    else:
        return render_template('game.html', items=items, system=system,
                               creator=creator)


# Create a new game item
@app.route('/system/<int:system_id>/game/new/', methods=['GET', 'POST'])
def newGameItem(system_id):
    if 'username' not in login_session:
        return redirect('/login')
    system = session.query(System).filter_by(id=system_id).one()
    if login_session['user_id'] != system.user_id:
        return ("<script>function myFunction() {alert('You are not authorized"
                "to add game items to this system. Please create your own "
                "system in order to add items.');}</script>"
                "<body onload='myFunction()'>")
    if request.method == 'POST':
        newItem = GameItem(name=request.form['name'],
                           description=request.form['description'],
                           genre=request.form['genre'], system_id=system_id,
                           user_id=system.user_id)
        session.add(newItem)
        session.commit()
        flash('New Game %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showGame', system_id=system_id))
    else:
        return render_template('newgameitem.html', system_id=system_id)

# Edit a game item

@login_required
@app.route('/system/<int:system_id>/game/<int:game_id>/edit',
           methods=['GET', 'POST'])
def editGameItem(system_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(GameItem).filter_by(id=game_id).one()
    system = session.query(System).filter_by(id=system_id).one()
    if login_session['user_id'] != system.user_id:
        return ("<script>function myFunction() {alert('You are not authorized"
                "to edit game items to this system. Please create your own"
                "system in order to edit items.');}</script>"
                "<body onload='myFunction()'>")
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['genre']:
            editedItem.genre = request.form['genre']
        session.add(editedItem)
        session.commit()
        flash('Game Item Successfully Edited')
        return redirect(url_for('showGame', system_id=system_id))
    else:
        return render_template('editgameitem.html', system_id=system_id,
                               game_id=game_id, item=editedItem)


# Delete a game item
@login_required
@app.route('/system/<int:system_id>/game/<int:game_id>/delete',
           methods=['GET', 'POST'])
def deleteGameItem(system_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')
    system = session.query(System).filter_by(id=system_id).one()
    itemToDelete = session.query(GameItem).filter_by(id=game_id).one()
    if login_session['user_id'] != system.user_id:
        return ("<script>function myFunction() {alert('You are not authorized"
                "to delete game items to this system. Please create your own"
                "system in order to delete items.');}</script>"
                "<body onload='myFunction()'>")
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Game Item Successfully Deleted')
        return redirect(url_for('showGame', system_id=system_id))
    else:
        return render_template('deleteGameItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showSystems'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showSystems'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    # allows for https in localhost
    #app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
    app.run(host = '35.182.6.123.xip.io')
