from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Store video URL and current timestamp
video_url = 'https://eplayvid.net/watch/7a45aed06ae8995'
current_timestamp = 0

# Store chat messages
chat_messages = []

@app.route('/')
def index():
    return render_template('u.html', video_url=video_url)

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('play_video')
def play_video(data):
    global current_timestamp
    current_timestamp = data['timestamp']
    # Broadcast the new timestamp to all connected clients
    socketio.emit('play_video', {'timestamp': current_timestamp}, broadcast=True)

@socketio.on('send_message')
def send_message(data):
    chat_messages.append(data['message'])
    # Broadcast the new message to all connected clients
    socketio.emit('receive_message', {'message': data['message']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)