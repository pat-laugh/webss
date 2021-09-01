# import threading
# threading.local().env = []
env = []

class Env:
	def __init__(self, lang, indent, compiler_session):
		self.lang = lang
		self.indent = indent
		self.compiler_session = compiler_session
