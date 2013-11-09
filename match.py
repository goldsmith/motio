import numpy as np
import pickle

from sklearn.neighbors import KNeighborsClassifier
from server import r

clf = KNeighborsClassifier(1)
if not r.get("clf"):
	r.set("clf", pickle.dumps(clf))

def train(data, label):
	"""
	Data should be [<>, <>, <>, ...]
	label should be a string
	"""

	clf = pickle.loads(r.get("clf"))

	flat = np.array(data).flatten()
	clf.fit([flat], [label])

	r.set("clf", pickle.dumps(clf))

def predict(data):
	"""
	Same form
	"""

	clf = pickle.loads(r.get("clf"))

	flat = np.array(data).flatten()
	return clf.predict(flat)

