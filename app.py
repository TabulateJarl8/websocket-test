from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
socketio = SocketIO(app)

#@socketio.on('connect')
#def show_connect_status(data):
#	print(f'Connected: {data!r}')

@socketio.on('message_send')
def send_message(data):
	print('RECIEVED ' + data)
	username = session.get('username', 'unknown')
	data['data'] = username + ': ' + data['data']
	emit('new_message', data, broadcast=True)

@socketio.on('change_username')
def change_username(data):
	print('change username')
	old_username = session.get('username', 'unknown')
	session['username'] = data['data']
	emit('new_message', {'data': f'{old_username} changed their name to {data["data"]}'}, broadcast=True)

@app.route('/')
def index():
	return render_template('index.html')