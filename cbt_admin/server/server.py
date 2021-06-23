#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from server.login import Login
from server.choice import PostChoice
from server.timer import PostTimer, StartTime, EndTime,UserDisconnect, Submit
import json

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret+_'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

Clients = {}
    

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/admin')
def admin():
    return render_template('admin.html', async_mode=socketio.async_mode)

@app.route("/test_conn",methods=["GET","POST"])
def test_conn():
    return {'login':'connected'}

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        return Login()

@socketio.on('join')
def on_join(data):
    userId = data['room']['id']
    room = data['room']['room']
    if Submit(data['room']) == 'submitted':
        emit('my_response', {'data':{'server':'203'}})
        
        return False
    join_room(room)
    Clients[request.sid] = data['room']
    StartTime(data['room'])
    #PostTimer(data)
    #send(username + ' has entered the room.', room=room)
  

@socketio.on('leave')
def on_leave(data):
    userId = data['room']['id']
    room = data['room']['room']
    leave_room(room)
    EndTime(data['room'])
    del Clients[request.sid]
    
    #PostTimer(data)
    #send(username + ' has left the room.', room=room)

@socketio.event
def my_event(message):
    emit('my_response',{'data': PostChoice(message)})
    print(PostChoice(message))

@socketio.on('user-connected')
def test_connect(msg):
    print('Client connected') 

@socketio.on('user-disconnected')
def test_disconnect():
    print('Client disconnected') 

@socketio.on('disconnect')
def disconnect():
    UserDisconnect(Clients[request.sid])
    print('disconnected')
    del Clients[request.sid]


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        #socketio.emit('my_response',
                      #{'data': 'Server generated event', 'count': count})

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)



def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def StartServer():
    try:
        port=int(json.load(open("json/port.json", "r")))
        #print(port)
        socketio.run(app,host='localhost', port=port)
    except Exception as e:
        print(e)
    
