import requests
import time
from flask import Flask,jsonify, session, request, redirect,url_for,render_template
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

messages = [{'room':'home','message':[{'name':'vikas', 'text':'hello','timestamp':'11:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'}]},{'room':'office','message':[{'name':'akash', 'text':'hellodfnfdnf','timestamp':'14:30'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'}]},{'room':'school','message':[{'name':'Rakesh', 'text':'hello','timestamp':'1:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'}]},{'room':'office','message':[{'name':'akash', 'text':'hello all','timestamp':'10:30'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hello','timestamp':'10:20'},{'name':'vikas', 'text':'hiiii','timestamp':'10:20'}]}]

channels = [{'home':['vikas','akash']},{'office':['rakesh','neha']},{'school':['rakesh','neha','sonu']}]

# making the routes 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        #if 'username' not in session or 'room' not in session:

        return render_template('index.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        for channel in channels:
            for key in channel:
                for name in channel[key]:
                    if name == username:
                        return render_template('index.html',channels = channels,message ='Username already exist')
        session['username'] = username
        return redirect(url_for('room'))

@app.route('/room', methods=['GET','POST'])
def room():
    if request.method =='GET':
        return render_template('room.html',username=session['username'], channels = channels)   
    elif request.method == 'POST':
        room = request.form.get('room')
        session['room'] = room
        add = 1
        for i in range(len(channels)):
            for key in channels[i]:
                if room == key:
                    add = 0
                    channels[i][key].append(session['username'])
        if add == 1:
            channels.append({session['room']:[session['username']]})
        return redirect(url_for('chat', room=room))

@app.route('/chat/<room>', methods=['GET','POST'])
def chat(room):
    #flash('You were logged in')
    session.pop('messages', None)
    session.pop('count', None)
    name = session['username']
    session['room'] = room
    if name == '' or session['room'] == '':
        return render_template('index.html')
    else:
        return render_template('chat.html',username=name,room=session['room'], channels = channels)

@app.route("/pastposts", methods=["POST"])
def pastposts():

    # Get start and end point for posts to generate.
    room = session['room']
    count = int(request.form.get("start"))
    # Get the messages in session on entering a channel
    #if not session.get('messages')
    if 'messages' not in session:
        for i in range(len(messages)):
            if messages[i]['room'] == room:
                session['count'] = i
                session['messages'] = messages[i]['message']
                break    
                
    l = len(session['messages'])
    data = []
    if l >= count + 10:
       r = 10
    elif count + 10 > l:
        if count > l:
            r = 0
        else:
            r = l % 10

    for i in range(r):            
        #data.append(messages[session['count']]['message'][count+i])
        data.append(session['messages'][count+i])
    
    #data = data.reverse()
    # Return list of posts.
    return jsonify(data)


# Events !!
@socketio.on('joined', namespace='/chat')
def joined(time):
    timestamp = str(time['time'])
    status = dict()
    #status['room'] = session['room']
    status['name'] = session['username']
    status['text'] = 'has joined'
    status['timestamp'] = timestamp
    room = session['room']
    join_room(room)
    emit('status',{'mg':status}, room = room)
    

@socketio.on('post', namespace='/chat')
def post(message):
    text = str(message['msg'])
    timestamp = str(time.localtime().tm_hour) + ':' +  str(time.localtime().tm_min)
    room = session['room']
    for i in range(len(messages)):
        if messages[i]['room'] == room:
            newpost = {'name':session['username'], 'text':text, 'timestamp':timestamp}
            messages[i]['message'].append(newpost)
            break
    emit('showmessage',{'mg':newpost}, room=room) 
