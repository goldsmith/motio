def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr 
    return start

@coroutine
def pipe():
	"""
	Create a pipe that takes input asynchronously then yields it.
	"""
	while True:
		data = (yield)
		yield data