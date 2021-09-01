from libs.constants import INDENTATION, SPACE, TAB

DEF_INDENT = TAB
INDENT_REPEAT = {
	SPACE: 4,
	TAB: 1,
}

class Indent:
	def __init__(self, count=0, val=DEF_INDENT):
		self.count = count
		self.val = val
	
	def merge(self, o):
		if self.val is DEF_INDENT:
			val = o.val
		elif o.val is DEF_INDENT:
			val = self.val
		elif self.val == o.val:
			val = self.val
		else:
			raise Exception('mixed indent')
		return Indent(self.count + o.count, val)
	
	def _mixed_indent(self, o):
		return not (DEF_INDENT in [self.val, o.val] or self.val == o.val)
	
	def __lt__(self, o):
		if self._mixed_indent(o):
			raise Exception('mixed indent')
		return self.count < o.count

	def __gt__(self, o):
		if self._mixed_indent(o):
			raise Exception('mixed indent')
		return self.count > o.count

	def count_indent(s):
		n_spaces, n_tabs, n_def = 0, 0, 0
		for c in s:
			if c == DEF_INDENT:
				n_def += 1
			elif c == TAB:
				n_tabs += 1
			elif c == SPACE:
				n_spaces += 1
			else:
				break
		items = [n_spaces, n_tabs, n_def]
		n_total = sum(items)
		if n_total != max(items):
			raise Exception('mixed indent')
		if n_spaces > 0:
			c = SPACE
		elif n_tabs > 0:
			c = TAB
		else:
			c = DEF_INDENT
		return Indent(n_total, c)
	
	def inc(self):
		return Indent(self.count + 1, self.val)
	
	def dec(self):
		return Indent(max(0, self.count - 1), self.val)
	
	def serialize(self):
		return self.val * self.count * INDENT_REPEAT[self.val]
