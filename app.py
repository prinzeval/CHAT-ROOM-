from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('u.html')

@socketio.on('play')
def play():
    emit('play')

@socketio.on('pause')
def pause():
    emit('pause')

@socketio.on('seek')
def seek(timestamp):
    emit('seek', timestamp)

if __name__ == '__main__':
    socketio.run(app, debug=True)
