import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
#import picamera
from time import sleep
import time
#import RPi.GPIO as GPIO# Import Raspberry Pi GPIO library
import requests
import json
import os
import MySQLdb as mysql
#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("/esp8266/smoke")
    client.subscribe("/esp8266/camera")
    

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
    #socketio.emit('my variable')
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    '''if message.topic == "/esp8266/temperature":
        print("temperature update")
        socketio.emit('dht_temperature', {'data': message.payload})  '''
    if message.topic == "/esp8266/smoke":
        print("smoke update")
        socketio.emit('sensor_smoke', {'data': message.payload})
    if message.topic == "/esp8266/camera":
    	print(message.payload)
    	socketio.emit('camera',{'data':message.payload})

@app.route('/smoke')
def smoke():
    db = mysql.connect("iot.db")
    c = db.cursor()
    c.execute("select smoke from data where smoke is not NULL")
    data = c.fetchall()
    data = data[-10:]
    values = [data[i][0] for i in range(0,10)]
    return render_template('smoke.html',values=values)
@app.route('/temperature')
def smoke():
    db = mysql.connect("iot.db")
    c = db.cursor()
    c.execute("select temperature from temperature where smoke is not NULL")
    data = c.fetchall()
    data = data[-10:]
    values = [data[i][0] for i in range(0,10)]
    return render_template('temperature.html',values=values)
@app.route('/humidity')
def smoke():
    db = mysql.connect("iot.db")
    c = db.cursor()
    c.execute("select humidity from data where humidity is not NULL")
    data = c.fetchall()
    data = data[-10:]
    values = [data[i][0] for i in range(0,10)]
    return render_template('humidity.html',values=values)
@app.route('/pulse')
def smoke():
    db = mysql.connect("iot.db")
    c = db.cursor()
    c.execute("select pulse from data where pulse is not NULL")
    data = c.fetchall()
    data = data[-10:]
    values = [data[i][0] for i in range(0,10)]
    return render_template('pulse.html',values=values)
mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(username="bbhcbdgr",password="EuzikmDn_mJN")
mqttc.connect("m15.cloudmqtt.com",13038,60)
mqttc.loop_start()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# The callback for when the client receives a CONNACK response from the server.

#GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : 'False'},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'},
   12 : {'name' : 'GPIO 12', 'board' : 'esp8266', 'topic' : 'esp8266/12', 'state' : 'False'},
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins
   }

@app.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   #GPIO.cleanup()
   #print("mani")
   return render_template('main.html', async_mode=socketio.async_mode, **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<board>/<changePin>/<action>")
def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "1" execute the code indented below:
   if action == "1" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"1")
      pins[changePin]['state'] = 'True'
   if action == "0" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"0")
      pins[changePin]['state'] = 'False'
   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }
   return render_template('main.html', **templateData)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8183, debug=True)
   #print("sffsd")
   GPIO.cleanup()












