from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
from database import connector
from datetime import datetime
from sqlalchemy import or_
import threading

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

contador = 0

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/', methods = ['GET'])
def get_index():
    return render_template('index.html')

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    #obtener data from request
    message = json.loads(request.data)
    username = message['username']
    password = message['password']

    # Chequeando la base de datos
    db_session = db.getSession(engine)
    user = db_session.query(entities.User
            ).filter(entities.User.username==username
            ).filter(entities.User.password==password)
    users = user[:]
    if len(users) !=0:
        session['user'] = json.dumps(users[0], cls=connector.AlchemyEncoder)
        message = {'msg': 'Welcome user!'}
        json_msg = json.dumps(message)
        return Response(json_msg, status=200,mimetype='application/json')
    message = {'message':'Authorized'}
    json_msg = json.dumps(message)
    return Response(json_msg, status=401,mimetype='application/json')


#CRUD users
@app.route('/users', methods = ['POST'])
def create_user():
    #c = json.loads(request.data)
    c = json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    r_msg = {'msg':'UserCreated'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=201)


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')
    message = { 'status': 404, 'message': 'Not Found'}
    return Response(json.dumps(message), status=404, mimetype='application/json')

key_users = 'users'
cache = {}


@app.route('/users', methods = ['GET'])
def get_users():
    data = []
    update_cache: bool = False
    max_time: int = 20
    if key_users in cache and (datetime.now() - cache[key_users]['time']).total_seconds() < 20:
        #GET
        data=cache[key_users]['data']
    else:
        session = db.getSession(engine)
        dbResponse = session.query(entities.User).order_by(entities.User.username)
        data = dbResponse[:]
        #SET CACHE
        cache[key_users] = {'data':data, 'time':datetime.now()}
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c = json.loads(request.form['values'])

    for key in c.keys():
        setattr(user, key, c[key])

    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    return "Deleted User"



#CRUD Message
@app.route('/messages', methods = ['POST'])
def create_message():
    c = json.loads(request.form['values'])
    message = entities.Message(
        content=c['content'],
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id'],
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/messages/chat', methods = ['POST'])
def create_message_chat():
    c = json.loads(request.data)
    message = entities.Message(
        content=c['content'],
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id'],
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/messages/<id>', methods = ['GET'])
def get_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    db_session.close()
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    message = {'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

key_messages = 'messages'
cache_messages = {}

@app.route('/messages', methods = ['GET'])
# @synchronized
def get_messages():
    global contador 
    data = []
    update_cache2: bool = False
    max_time2: int = 20
    #synchronized(db_log)
    lock = threading.Lock()
    lock.acquire()
    print(contador)
    if key_messages in cache and (datetime.now() - cache_messages[key_messages]['time']).total_seconds() < 20:
        #GET
        data=cache_messages[key_messages]['data']
    else:
        contador +=1
        sessionc = db.getSession(engine)
        dbResponse = sessionc.query(entities.Message)
        data = dbResponse[:]
        lock.release()
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/messages/<user_from_id>/<user_to_id>', methods = ['GET'])
def get_messagesfrom(user_from_id, user_to_id ):
    db_session = db.getSession(engine)
    messagesto = db_session.query(entities.Message).filter(or_(
        entities.Message.user_from_id == user_from_id, entities.Message.user_from_id == user_to_id)).filter(or_(
        entities.Message.user_to_id == user_to_id, entities.Message.user_to_id == user_from_id
    ))
    # messages  from = db_session.query(entities.Message).filter(
    #     entities.Message.user_from_id == user_to_id).filter(
    #     entities.Message.user_to_id == user_from_id
    # )
    data = messagesto[:]
    # for messages in messagesfrom:
    #     data.append(messages)
    print(data)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/messages', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'

@app.route('/messages', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    message = session.query(entities.Message).filter(entities.Message.id == id).one()
    session.delete(message)
    session.commit()
    return "Deleted Message"



@app.route('/current', methods = ['GET'])
def current_user():
    user_json = session['user']
    return Response(user_json, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
 