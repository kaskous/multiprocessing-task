from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2
import threading
import sqlite3
import datetime
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Ensure the 'images' directory exists
if not os.path.exists('images'):
    os.makedirs('images')

# Database setup
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mouse_data
                 (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER, timestamp TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Webcam setup
cap = cv2.VideoCapture(0)

def capture_image():
    ret, frame = cap.read()
    if ret:
        filename = f'images/{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        cv2.imwrite(filename, frame)
        return filename
    return None

@socketio.on('mouse_move')
def handle_mouse_move(data):
    x = data['x']
    y = data['y']
    timestamp = datetime.datetime.now().isoformat()
    emit('mouse_update', {'x': x, 'y': y, 'timestamp': timestamp}, broadcast=True)

@socketio.on('capture_image')
def handle_capture_image(data):
    x = data['x']
    y = data['y']
    filename = capture_image()
    timestamp = datetime.datetime.now().isoformat()
    if filename:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO mouse_data (x, y, timestamp, image_path) VALUES (?, ?, ?, ?)",
                  (x, y, timestamp, filename))
        conn.commit()
        conn.close()
        emit('image_captured', {'filename': filename, 'timestamp': timestamp}, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
