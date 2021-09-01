from libs.state import State
from libs.env import env

class EnvWrapper:
	def __init__(self, env, child):
		self.env = env
		assert(type(child) is not str)
		self.child = child
		self.called_child = False

	def __getattr__(self, attr):
		try:
			if not self.called_child:
				self.called_child = True
				return getattr(self.child, attr)
			raise AttributeError("'%s' object has no attribute '%s'" %
				(type(self).__name__, attr)
			)
		finally:
			self.called_child = False
	
	def serialize(self, *args):
		env.append(self.env)
		self.child.serialize(*args)
		env.pop()

