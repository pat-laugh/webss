from libs.constants import CC_NEW_STATE, CC_END_STATE, LANG_PY, LANG_WBSS
from libs.env_wrapper import EnvWrapper
from libs.state import State
from libs.indent import Indent
from libs.env import env, Env

indent = Indent()

class CompilerStream:
	def __init__(self, session, base_state, lang):
		self.base_state = base_state
		self.session = session
		self.lang = lang
		self.file_line_num = 0
		self.file_col_num = 0
	
	def new_state(self):
		self.states = [self]
		self.children = []
		self.push_state(self.base_state, None)
		self.first_state = self.states[1]
		self.s_in = []
		self.s_idx = 0
	
	@property
	def start_of_line(self):
		return self.file_col_num == 0
	
	@property
	def curr_state(self):
		return self.states[-1]
	
	def send_state(self, s):
		self.children.append(s)
	
	def push_state(self, state_conf, token):
		s = state_conf.make_inst(token)
		action = self.curr_state.send_state(s)
		action, item = self.get_action_and_item(action)
		if action is None:
			consume = True
			self.states.append(s)
			self.prepare_state()
		elif action is CC_NEW_STATE:
			assert(False)
		elif action is CC_END_STATE:
			consume = item
			self.pop_state()
		return consume
	
	def pop_state(self):
		del self.states[-1]
		self.prepare_state()
	
	@property
	def curr_events(self):
		return self.curr_state.events[self.lang]
	
	def prepare_state(self):
		# determine how many chars to look ahead
		self.length_token = max([1] + [len(x) for x in
				self.curr_events])

	def get_next_token(self):
		max_index = min(len(self.s_in), self.s_idx + self.length_token)
		str_token = []
		for c in self.s_in[self.s_idx:max_index]:
			if type(c) is str:
				assert(len(c) == 1)
				str_token.append(c)
			else:
				assert(isinstance(c, State) or type(c) is EnvWrapper)
				break
		return ''.join(str_token)

	def find_matches(self, token):
		matches = []
		while len(token) > 0:
			if token in self.curr_events:
				matches.append((token, self.curr_events[token]))
			token = token[:-1]
		return matches

	def serialize(self, complete=True):
		s = []
		self.first_state.serialize(s, complete)
		return s
	
	def last_child_ended(self):
		if len(self.first_state.children) == 0:
			return False
		return self.first_state.children[-1].ended

	def open_document(self):
		self.new_state()
	
	def close_document(self):
		self.first_state.end_state()
	
	def has_input(self):
		return self.s_idx < len(self.s_in)

	def _inc_stream(self, str_token):
		if type(str_token) is str:
			amount = len(str_token)
			for c in str_token:
				if c == '\n':
					self.file_line_num += 1
					self.file_col_num = 0
				else:
					self.file_col_num += 1
		else:
			assert(type(str_token) is int)
			amount = str_token
		self.s_idx += amount
	
	def get_next(self):
		return self.s_in[self.s_idx]
	
	def insert(self, s, idx_offset=0):
		# first have to "break down" any string of more
		# than one char within the stream
		l = []
		for c in s:
			if type(c) is not str or len(c) == 1:
				l.append(c)
			else:
				l += list(c)

		i, s = self.s_idx + idx_offset, self.s_in
		self.s_in = s[:i] + l + s[i:]
		return len(l)
	
	def get_action_and_item(self, action):
		if action is not None:
			assert(type(action) is tuple and len(action) == 2)
			action, item = action
		else:
			item = None
		return action, item

	def parse(self, s_in):
		self.insert(s_in)
		while self.has_input():
			item = self.get_next()
			if isinstance(item, State) or type(item) is EnvWrapper:
				action = self.curr_state.send_state(item)
				action, item = self.get_action_and_item(action)
				_inc_stream_val = 1
			else:
				assert(type(item) is str)
				token = self.get_next_token()
				matches = self.find_matches(token)
				if len(matches) == 0:
					token = self.get_next()
					action = self.curr_state.send_char(token)
					action, item = self.get_action_and_item(action)
				else:
					token, func = matches[0]
					action, item = func(self.curr_state, token)
				_inc_stream_val = token
			if action is None:
				consume = True
			elif action is CC_NEW_STATE:
				new_state = item
				consume = self.push_state(new_state, token)
			elif action is CC_END_STATE:
				consume = item
				self.pop_state()
			if consume:
				self._inc_stream(_inc_stream_val)

class CompilerSession:
	def __init__(self, engine, in_lang=LANG_WBSS, out_lang=LANG_PY, sessions=None):
		if sessions is None:
			sessions = []
		self.id = len(sessions)
		sessions.append(self)
		self.sessions = sessions
		self.engine = engine
		self.in_lang = in_lang
		self.out_lang = out_lang
		self.st_0 = engine.base_state_stream_0
		self.st_1 = engine.base_state_stream_1
		self.dict_globals = {}
		self.dict_locals = {}
		self.stream_0 = CompilerStream(self, self.st_0, LANG_WBSS)
		self.stream_1 = CompilerStream(self, self.st_1, self.in_lang)
		self.names_global = {}
	
	def parse(self, str_in, complete=True, get_state=False):
		s_in = list(str_in) if type(str_in) is not list else str_in
		envs = [[Env(x, indent, self) for x in [LANG_WBSS, self.in_lang]],
				[Env(x, indent, self) for x in [LANG_PY, self.out_lang]]]
		cmpls = [[True, complete], [True, complete]]
		for i, stream in enumerate([self.stream_0, self.stream_1]):
			env.append(envs[0][i])
			cmpl = cmpls[0][i]
			# if cmpl:
			stream.open_document()
			env[-1].cont = stream.first_state
			stream.parse(s_in)
			# if cmpl:
			stream.close_document()
			env.pop()

			env.append(envs[1][i])
			env[-1].cont = stream.first_state
			cmpl = cmpls[1][i]
			s_out = stream.serialize(cmpl)
			s_in = s_out
			env.pop()

		str_out = ''.join(s_out)
		if get_state:
			return self.stream_1.first_state, str_out
		return str_out
	
	def session(self, id):
		while id >= len(self.sessions):
			CompilerSession(self.engine, LANG_WBSS,  LANG_PY, self.sessions)
		return self.sessions[id]
	
	def layer(self, layer=1):
		if layer == 0:
			return self.stream_0
		if layer == 1:
			return self.stream_1
		assert(False)

	def last_child_ended(self):
		return self.stream_1.last_child_ended()
	
class CompilerEngine:
	def __init__(self, base_state_stream_0, base_state_stream_1):
		self.base_state_stream_0 = base_state_stream_0
		self.base_state_stream_1 = base_state_stream_1
	
	def get_session(self, in_lang=LANG_WBSS, out_lang=LANG_PY):
		return CompilerSession(self, in_lang, out_lang)
