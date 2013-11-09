def pipe():
	"""
	Create a pipe that takes input asynchronously then yields it.
	"""
	while True:
		data = (yield)
		yield data