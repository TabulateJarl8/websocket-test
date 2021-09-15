from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@socketio.on('message_send')
def send_message(data):
	print('RECIEVED ' + data['data'])
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

#if __name__ == '__main__':
#	socketio.run(app, port=int(os.environ.get('PORT', '5000')), debug=True)
