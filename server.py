from flask import Flask, request
from flask_sockets import Sockets

from match import train, predict
from utils import pipe

app = Flask(__name__)
sockets = Sockets(app)

client_socket_pipe = pipe()

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

	client_socket_pipe.send({
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
	client_socket.send({
		"name": name,
		"action": "do_gesture"
	})

@sockets.route("/client_socket")
def client_socket(ws):
	for data in client_socket_pipe:
		ws.send(data)

if __name__ == '__main__':
    app.run()