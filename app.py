from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

# Store video URL and current timestamp
video_url = 'https://e5.animeheaven.me/video.mp4?30dbec1968b1dc0c730f6b64e7920003'
current_timestamp = 0

# Store chat messages
chat_messages = []

@app.route('/')
def index():
    return render_template('u.html', video_url=video_url)

@socketio.on('connect')
def connect():
    print('Client connected')
    join_room('watch_together')
    global current_timestamp
    socketio.emit('play_video', {'timestamp': current_timestamp}, room='watch_together')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
    leave_room('watch_together')

@socketio.on('play_video')
def play_video(data):
    global current_timestamp
    current_timestamp = data['timestamp']
    socketio.emit('play_video', {'timestamp': current_timestamp}, room='watch_together')

@socketio.on('heartbeat')
def heartbeat(data):
    global current_timestamp
    client_timestamp = data['timestamp']
    if abs(client_timestamp - current_timestamp) > 5:  # adjust the tolerance value as needed
        socketio.emit('play_video', {'timestamp': current_timestamp}, room='watch_together')

@socketio.on('send_message')
def send_message(data):
    chat_messages.append(data['message'])
    socketio.emit('receive_message', {'message': data['message']}, room='watch_together')

if __name__ == '__main__':
    socketio.run(app, debug=True)
