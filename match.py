import numpy as np

from sklearn.neighbors import KNeighborsClassifier

clf = KNeighborsClassifier(1)

def train(data, label):
	"""
	Data should be [<>, <>, <>, ...]
	label should be a string
	"""

	flat = np.array(data).flatten()
	clf.fit([flat], [label])

def predict(data):
	"""
	Same form
	"""

	flat = np.array(data).flatten()
	return clf.predict(flat)