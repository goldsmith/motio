import os

from flask import Flask, request
from flask_sockets import Sockets

from match import train, predict
from utils import pipe

app = Flask(__name__)
sockets = Sockets(app)

web_socket = None
# web_socket_pipe = ("foo", "bar", "foobar", "barfoo", "bar food", "nighttime")

@app.route("/")
def index():
	print request
	return 'hi!'

@app.route("/add_gesture")
def add_gesture():
	# get the data from the post
	# train the model
	# let the client know that there is a new model
	name = request.form['name']
	data = request.form['data']

	train(data, name)

	web_socket_pipe.send({
		"name": name,
		"action": "add_gesture"
	})

	return

@app.route("/do_gesture")
def do_gesture():
	data = request.form['data']
	name = predict(data)
	# test the model
	# let the client know of the command name
	web_socket.send({
		"name": name,
		"action": "do_gesture"
	})

@sockets.route("/web_socket")
def web_socket(ws):
	print "connected", ws

	web_socket = ws

	while True:
		continue

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)