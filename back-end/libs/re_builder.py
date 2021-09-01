import re

ids_chars = {}
ids = 127
def prod_id():
	global ids
	ids += 1
	return chr(ids)

def char_id(c):
	if type(c) is not str:
		return c.prod_id
	if c not in ids_chars:
		ids_chars[c] = prod_id()
	return ids_chars[c]

T_SINGLE, T_OR, T_AND, M_BOOL, M_PLUS, M_STAR = 0, 1, 2, 3, 4, 5
types = { 'and': T_AND, 'or': T_OR, 'single': T_SINGLE}
mods = {'?': M_BOOL, '+': M_PLUS, '*': M_STAR}
mod_to_str = {M_BOOL: '?', M_PLUS: '+', M_STAR: '*'}

class ReBuilder:
	def __init__(self, t, items, mod=None, name=None):
		if type(t) is str:
			self.t = types[t]
		else:
			self.t = t
		if self.t is T_SINGLE and type(items) is not list:
			self.items = [items]
		else:
			self.items = items
		if type(mod) is str:
			self.mod = mods[mod]
		else:
			self.mod = None
		self.name = name

	def serialize(self):
		s = ['(']
		if self.name is not None:
			s.append('?P<%s>' % self.name)
		chars = []
		for item in self.items:
			if type(item) is type(self):
				chars.append(item.serialize())
			else:
				chars.append(char_id(item))

		if self.t is T_SINGLE or self.t is T_AND:
			out = ''.join(chars)
		elif self.t is T_OR:
			out = '|'.join(chars)
		s += [out, ')', mod_to_str.get(self.mod, '')]
		return ''.join(s)

	def compile(self):
		return re.compile(self.serialize())
