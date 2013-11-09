import os
import redis
import gevent

from flask import Flask, request
from flask_sockets import Sockets

from match import train, predict
from utils import pipe

app = Flask(__name__)
sockets = Sockets(app)

REDIS_URL = os.environ.get('REDISCLOUD_URL')
REDIS_CHAN = 'motio'

if not REDIS_URL:
	redis = redis.Redis()
else:
	redis = redis.from_url(REDIS_URL)

socket = None
# socket_pipe = ("foo", "bar", "foobar", "barfoo", "bar food", "nighttime")

class SocketBackend(object):

	def __init__(self):
		self.clients = []
		self.pubsub = redis.pubsub()
		self.pubsub.subscribe(REDIS_CHAN)

	def __iter_data(self):
		for message in self.pubsub.listen():
			data = message.get('data')
			print 'data received: {}'.format(data)
			if message['type'] == 'message':
				yield data

	def register(self, client):
		self.clients.append(client)

	def send(self, client, data):
		try:
			client.send(data)
		except:
			self.clients.remove(client)

	def run(self):
		for data in self.__iter_data():
			for client in self.clients:
				gevent.spawn(self.send, client, data)

	def start(self):
		gevent.spawn(self.run)

socket = SocketBackend()
socket.start()

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

	redis.publish(REDIS_CHAN, {
		"name": name,
		"action": "add_gesture"
	})

@app.route("/damn")
def damn():
	redis.publish(REDIS_CHAN, "foo")
	print socket

	return "bye!"

@app.route("/do_gesture")
def do_gesture():
	data = request.form['data']
	name = predict(data)
	# test the model
	# let the client know of the command name
	redis.publish(REDIS_CHAN, {
		"name": name,
		"action": "do_gesture"
	})

@sockets.route("/client_socket")
def web_socket(ws):
	socket.register(ws)

	while ws.socket is not None:
		gevent.sleep()



# if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)