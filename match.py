import numpy as np
import pickle
import urlparse
import os

from sklearn.neighbors import KNeighborsClassifier
import redis

REDIS_URL = os.environ.get('REDISCLOUD_URL')

if not REDIS_URL:
	r = redis.Redis()
else:
	url = urlparse.urlparse(REDIS_URL)
	r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

clf = KNeighborsClassifier(1)
if not r.get("clf"):
	r.set("clf", pickle.dumps(clf))

def train(data, label):
	"""
	Data should be [<>, <>, <>, ...]
	label should be a string
	"""

	print 'training with data'
	print 'label', label
	print data[0]


	clf = pickle.loads(r.get("clf"))

	print "len", len(data)
	print "flat", np.array(data).flatten()[:100]

	flat = np.array(data).flatten()[:1000]
	clf.fit([flat], [label])

	r.set("clf", pickle.dumps(clf))

def predict(data):
	"""
	Same form
	"""

	print 'predicting from data'
	print data[0]
	print len(data)

	clf = pickle.loads(r.get("clf"))

	flat = np.array(data).flatten()
	return clf.predict([flat])

