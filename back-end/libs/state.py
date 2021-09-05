from libs.constants import lang_dict, LANGS, CC_NEW_STATE, LANG_PY, INDENTATION
from libs.re_builder import prod_id, char_id
from libs.env import env

indent_put, item_put = False, False

class State:
	def __init__(self, base=None, parsed_start=None):
		self.base = base
		if base is None:
			self.conf()
		else:
			self.inst(parsed_start)
	
	def conf(self):
		self.prod_id = prod_id()
		self.events = lang_dict([{}, {}, {}, {}, {}])
		self.switch_state_dict = lang_dict([{}, {}, {}, {}, {}])
	
	def inst(self, parsed_start):
		self.children = []
		self.children_ids = []
		self.parsed_start = parsed_start
	
	def make_inst(self, parsed_start):
		return type(self)(self, parsed_start)

	def __call__(self, lines):
		inst = self.make_inst(None)
		inst.lines = lines
		inst.curr_line = []
		inst.ended = True
		return inst
	
	def __getattr__(self, attr):
		if self.base is None:
			raise AttributeError("'%s' object has no attribute '%s'" %
				(type(self).__name__, attr)
			)
		return getattr(self.base, attr)
		
	def __repr__(self):
		s = []
		self.repr(s)
		return ''.join(s)
	
	def repr(self, s, item):
		s.append(type(self).__name__)
		s.append('(')
		s.append(repr(item))
		s.append(')')
	
	def get_char_id(self, c):
		return char_id(c)

	def switch_state(self, token):
		return CC_NEW_STATE, self.switch_state_dict[self.lang][token]
	
	def send_char(self, c):
		self.children.append(c)
		self.children_ids.append(self.get_char_id(c))

	def send_state(self, s):
		self.children.append(s)
		self.children_ids.append(s.prod_id)
	
	def send_item(self, item):
		self.children.append(item)
		self.children_ids.append(char_id(item))

	@property
	def env(self):
		return env[-1]

	@property
	def lang(self):
		return self.env.lang
	
	def compiler_session(self):
		return self.env.compiler_session

	def add_st_to_events(self, st):
		assert(type(st.start) is lang_dict)
		for lang in self.events:
			if lang in st.start:
				key = st.start[lang]
				self._add_st_to_events_lang(st, lang, key)
	
	def _add_st_to_events_lang(self, st, lang, key):
		if key is None or key == '':
			return
		elif isinstance(key, State):
			_key = key.start[lang]
			self._add_st_to_events_lang(key, lang, _key)
			return
		elif type(key) is list:
			for c in key:
				self._add_st_to_events_lang(st, lang, c)
			return
		events = self.events[lang]
		switch_state_dict = self.switch_state_dict[lang]
		if key in events:
			# TOOD: Improve this error message
			# can't put self or st because it calls `repr` in the background,
			# which can cause problems
			# `key` should also be escaped appropriately (like newline)
			raise Exception('duplicate start chars in one container: "%s"' % key)
			raise Exception('key %s already in events: %s %s' % (
				key, self, st))
		if key in switch_state_dict:
			raise Exception('key %s already in switch dict: %s %s' % (
				key, self, st))
		events[key] = type(self).switch_state
		switch_state_dict[key] = st

	def add_event(self, keys, func):
		assert(type(keys) in [dict, lang_dict])
		for lang, events in self.events.items():
			if lang not in keys:
				continue
			key = keys[lang]
			if key is None or key == '':
				continue
			elif isinstance(key, State):
				continue # TODO: improve
			if key in events:
				raise Exception('key %s already in events: %s' % (self, key))
			events[key] = func
		
	def append_item(self, s, item):
		global item_put
		if type(item) is str:
			items = item.split('\n')
			if len(items) > 1:
				for item in items[:-1]:
					self.append_item(s, item)
					self.append_newline(s)
				item = items[-1]
			if not item_put and not self.env.cont.consume_all:
				for i, c in enumerate(item):
					if c not in INDENTATION:
						if i > 0:
							item = item[i:]
						break
				else:
					return
			if len(item) == 0 and self.env.cont.ignore_empty_line():
				return
		self.env.cont.check_append_indent(s)
		s.append(item)
		item_put = True

	def check_append_indent(self, s):
		global indent_put
		if not indent_put:
			if self.env.cont.out_indent() and self.env.cont.out_multiline():
				s.append(self.env.indent.serialize())
			indent_put = True
	
	def append_newline(self, s):
		global indent_put, item_put
		if item_put or not self.env.cont.ignore_empty_line():
			s.append('\n')
			indent_put, item_put = False, False
