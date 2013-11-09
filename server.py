import os
import redis
import gevent

import os
import urlparse

from flask import Flask, request
from flask_sockets import Sockets

from match import train, predict
from utils import pipe

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

sockets = Sockets(app)

REDIS_URL = os.environ.get('REDISCLOUD_URL')
REDIS_CHAN = 'motio'

if not REDIS_URL:
	r = redis.Redis()
else:
	url = urlparse.urlparse(REDIS_URL)
	r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

print r

class SocketBackend(object):

	def __init__(self):
		self.clients = []
		self.pubsub = r.pubsub()
		self.pubsub.subscribe(REDIS_CHAN)

	def __iter_data(self):
		for message in self.pubsub.listen():
			data = message.get('data')
			print 'data received: {}'.format(data)
			print (str(message))
			if message['type'] == 'message':
				yield data

	def register(self, client):
		self.clients.append(client)

	def send(self, client, data):
		# try:
		os.system('say foobar')
		client.send(data)

	def run(self):
		for data in self.__iter_data():
			print 'data!', data
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

@app.route("/add_gesture", methods=['POST'])
def add_gesture():
	# get the data from the post
	# train the model
	# let the client know that there is a new model
	name = request.form['name']
	data = eval(request.form['data'])
	assert isinstance(data, list)

	print 'got your data!', name, data

	train(data, name)

	key = '{"name": "%s", "action": "add_gesture"}' % name
	r.publish(REDIS_CHAN, key)

	return "thanks a lot!\n"

@app.route("/do_gesture", methods=['POST'])
def do_gesture():
	data = eval(request.form['data'])
	assert isinstance(data, list)
	name = predict(data)
	# test the model
	# let the client know of the command name
	r.publish(REDIS_CHAN, '{"name": {},"action": "do_gesture"}'.format(name))

	return ''

@sockets.route("/client_socket")
def web_socket(ws):

	socket.register(ws)

	while ws.socket is not None:
		gevent.sleep()



# if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)