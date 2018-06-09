#!/usr/bin/python

import rospy
from std_msgs.msg import String
from diagnostic_msgs.msg import DiagnosticArray

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import yaml


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pepper'
socketio = SocketIO(app)


@socketio.on('connect')
def test_connect():
    print("Connected")
    emit('res', {'text': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnostics')
def diagnostics():
    return render_template('diagnostics.html')

def callback(data):
    new_data = dict()
    new_data['data'] = data.data
    socketio.emit('ros_msg', new_data)

def diagnostics(data):
    y = yaml.load(str(data))
    j = json.dumps(y, indent=4)
    socketio.emit('ros_diagnostics', j)

if __name__ == '__main__':

    rospy.init_node('webserver', anonymous=True)
    rospy.Subscriber("/speech", String, callback)
    rospy.Subscriber("/diagnostics", DiagnosticArray, diagnostics)

    app.run(host='0.0.0.0', threaded=True)
    rospy.spin()
