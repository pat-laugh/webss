from contextlib import contextmanager

from libs.constants import CC_END_STATE, lang_dict
from libs.constants import IGNORE, INDENTATION, NEWLINE, SEPARATOR
from libs.state import State
from libs.env_wrapper import EnvWrapper

END_LINE_SOFT = []

@contextmanager
def env_cont(self):
	prev_cont = self.env.cont
	self.env.cont = self
	try:
		yield
	finally:
		self.env.cont = prev_cont

class StateContainer(State):
	def conf(self):
		super().conf()
		self.add_event(self.end, type(self).check_end)
		self.cc_consume_end = lang_dict([True] * 5)
		self.productions = []
		self.set_consume_all_conf(False)
		self.sep_last_line = lang_dict([False] * 5)
		
	def inst(self, parsed_start):
		super().inst(parsed_start)
		self.set_consume_all_inst(False)
		self.start_of_line = True
		self.start_after_sep = True
		self.count_bounds = 0
		self.started = True
		self.ended = False

	def set_consume_all_conf(self, s=True):
		self.consume_all = s

		self.ignore_indent = not s
		self._ignore_empty_line = not s
		self.out_multiline_start = not s
		self.out_multiline_end = not s

		if s:
			self.out_eol = ['', '\n']
			self.separators = lang_dict([['']] * 5)
		else:
			self.out_eol = [' ', '\n']
			self.separators = lang_dict([[',']] * 5)
	
	def set_consume_all_inst(self, s=True):
		self.first_line = not s
		self.is_multiline = s # determined on first line
	
	def ignore_empty_line(self):
		return self._ignore_empty_line
	
	def out_indent(self):
		return self.ignore_indent

	def check_first_line(self, is_multiline):
		if self.first_line is True:
			self.is_multiline = is_multiline
			self.first_line = False

	def _send_char(self, c):
		if c == NEWLINE:
			if self.first_line:
				# means first line was empty
				if not self.consume_all:
					self.check_first_line(True)
					return
			self._send_item(c, False, True, True, self.end_line)
		elif c in self.separators[self.lang]:
			self._send_item(c, False, False, True, self.end_line)
		elif c in INDENTATION:
			if not (self.ignore_indent
					and (self.start_of_line or self.start_after_sep)):
				self._send_item(c)
		elif c in IGNORE:
			return # could put warning, but not necessary
		else:
			self._send_item(c)
	
	def _send_item(self, item, first=False, line=False, sep=False, func=None):
		if func is None:
			func = self.append_to_curr_line
		self.check_first_line(first)
		self.start_of_line = line
		self.start_after_sep = sep
		func(item)
	
	def append_to_curr_line(self, s):
		self.curr_line.append(s)
		
	def push_curr_line(self):
		if len(self.curr_line) > 0 or not self.ignore_empty_line():
			self.lines.append(self.curr_line)
			self.curr_line = []
	
	def end_line(self, end=END_LINE_SOFT):
		if end in self.separators[self.lang]:
			self.curr_line.append(SEPARATOR)
		self.push_curr_line()
	
	def write_start_end(self, s, start=True):
		if start:
			c = self.start[self.lang]
			if self.out_indent():
				self.env.indent = self.env.indent.inc()
		else:
			c = self.end[self.lang]
			if self.out_indent():
				self.env.indent = self.env.indent.dec()
		if c is None:
			raise Exception('cannot serialize %s in language %s' % (
				type(self).__name__, self.lang))
		if isinstance(c, State):
			raise Exception('not implemented yet!')
		if not start:
			if self.out_multiline_end and self.out_multiline():
				self.append_newline(s)
		
		self.append_item(s, c)
		if start:
			if self.out_multiline_start and self.out_multiline():
				self.append_newline(s)
	
	def all_lines(self):
		lines = self.lines[:]
		if len(self.curr_line) > 0:
			lines.append(self.curr_line)
		return lines

	def serialize(self, s, complete=True):
		if not self.started:
			return
		if not self.ended:
			if complete:
				raise Exception('structure not ended')
			self.end_state(False)

		with env_cont(self):
			self.write_start_end(s, True)
			lines = self.all_lines()
			if len(lines) > 0:
				for line in lines[:-1]:
					self.serialize_line(s, complete, line)
				else:
					self.serialize_line(s, complete, lines[-1],
						not self.sep_last_line[self.lang])
			if self.ended:
				self.write_start_end(s, False)
	
	def serialize_line(self, s, complete, line, last_line=False):
		self.check_append_indent(s)
		if line is SEPARATOR:
			self.serialize_separator(s, complete, line, last_line)
		elif type(line) is list:
			self.serialize_list(s, complete, line, last_line)
		else:
			self.serialize_item(s, complete, line)

		if not last_line:
			seps = self.separators[self.lang]
			i = 0 if not self.out_multiline() else 1
			if len(seps) < 2:
				sep = seps[0]
			else:
				sep = seps[i]
			eol = self.out_eol[i]
			if sep != eol:
				self.append_item(s, sep)
			self.append_item(s, eol)
	
	def serialize_separator(self, s, complete, line, last_line=False):
		if last_line and not self.skip_last_sep():
			self.append_item(s, self.separators[self.lang][0])
		
	def serialize_list(self, s, complete, line, last_line=False):
		line = line[:]
		i = 0
		while i < len(line):
			c = line[i]
			if c is SEPARATOR:
				assert(i == len(line) - 1)
				self.serialize_separator(s, complete, line, last_line)
			elif type(c) is list:
				line = c + line[i+1:]
				i = 0
				continue
			else:
				self.serialize_item(s, complete, c)
			i += 1
	
	def serialize_item(self, s, complete, c):
		if isinstance(c, State) or type(c) is EnvWrapper:
			c.serialize(s, complete)
		else:
			assert(c != NEWLINE)
			self.append_item(s, str(c))

	def parse_children(self):
		if len(self.productions) > 0:
			children = self.parse_productions()
		else:
			children = self.children
		self.lines = []
		self.curr_line = []
		with env_cont(self):
			for c in children:
				if type(c) is not str:
					self._send_item(c)
				else:
					self._send_char(c)
			self.end_line()
	
	def parse_productions(self):
		if self.ended:
			children = self.children
			children_ids = self.children_ids
		else:
			children = self.children[:]
			children_ids = self.children_ids[:]
		for prod in self.productions:
			str_tokens = ''.join(children_ids)
			it = prod.re_ids.finditer(str_tokens)
			matches = []
			try:
				while True:
					m = next(it)
					matches.append(m)
			except StopIteration:
				pass
			for m in reversed(matches):
				indices, groupdict = m.span(), m.groupdict()
				i1, i2 = indices
				items = children[i1:i2]
				for key, val in groupdict.items():
					if val is None:
						continue
					i = m.start(key)
					assert(i >= 0)
					groupdict[key] = children[i]
				del children[i1:i2]
				del children_ids[i1:i2]
				p = prod.make_inst((items, groupdict))
				children.insert(i1, p)
				children_ids.insert(i1, p.prod_id)
				# p.end_state()
		return children

	def end_state(self, ended=True):
		# set ended to False to do as if was ended
		if ended:
			self.ended = ended
		# <T(687)>
		if len(self.children) > 0:
			if isinstance(self.children[-1], State):
				self.children[-1].end_state()
		# </T(687)>
		self.parse_children()

	def check_end(self, c):
		if self.count_bounds == 0:
			self.end_state()
			return CC_END_STATE, self.cc_consume_end[self.lang]
		self.count_bounds -= 1
		self.send_char(c)
		return None, None
	
	def check_start(self, c):
		self.count_bounds += 1
		self.send_char(c)
		return None, None
	
	def out_multiline(self):
		return self.is_multiline
	
	def skip_last_sep(self):
		return True
	
	def repr(self, s):
		State.repr(self, s, self.lines)
	
	def __add__(self, o):
		if self.base is not o.base:
			raise TypeError('TypeError: operand +: states must have same base')
		return self.base(self.lines + o.lines)
