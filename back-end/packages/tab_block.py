from libs.constants import lang_dict, CC_END_STATE, LANG_JS
from libs.constants import COLON, NEWLINE, INDENTATION, IGNORE, SEPARATOR
from libs.indent import Indent
from libs.state_container import StateContainer
from packages.exec_list import StateExecList

from libs.lib_generator import add_package

END_CONT = []
global_indent = [Indent()]

class StateTabBlock(StateContainer):
	def conf(self):
		self.id = 2
		self.name = 'Tab Block'
		self.desc = 'Use indentation to denote blocks instead of braces.'

		self.start = lang_dict([None, None, None, None, COLON + '\n'])
		self.end = lang_dict([None] * 5)
		super().conf()
		self.separators = lang_dict([['']] * 4 + [[';']])
		self.conf_exec_list = StateExecList()
		self.conf_exec_list.end[LANG_JS] = '}\n'

	def inst(self, parsed_start):
		super().inst(parsed_start)
		self.started_parsing = False
		self.indent = None
		self.lines = []
		self.curr_line = []

	def send_char(self, c):
		return self.send_item(c, self._send_char)

	def send_state(self, s):
		return self.send_item(s, self._send_item)
	
	def send_item(self, s, func):
		if not self.started_parsing:
			# workaround for setting env indent to 0 when parsing
			global_indent[0] = Indent()
			self.started_parsing = True
		if func(s) is END_CONT:
			self.end_state()
			return CC_END_STATE, False
	
	def _send_char(self, c):
		if c == NEWLINE:
			global_indent[0] = Indent()
			if self.start_of_line:
				# mostly ignore empty lines
				return c if self.consume_all else None
			return self._send_item(c, False, True, True, self.end_line)
		elif c in self.separators[self.lang]:
			return self._send_item(c, False, False, True, self.end_line)
		elif c in INDENTATION:
			if self.start_of_line:
				curr_indent = Indent(1, c)
				if global_indent[0].count > 0:
					curr_indent = global_indent[0].merge(curr_indent)
				global_indent[0] = curr_indent
				return
			elif self.start_after_sep:
				if self.ignore_indent:
					return # ignore
		elif c in IGNORE:
			return # could put warning, but not necessary
		return self._send_item(c)

	def _send_item(self, item, first=False, line=False, sep=False, func=None):
		if not line:
			if self.first_line:
				self.indent = global_indent[0]
			elif self.indent > global_indent[0]:
				return END_CONT
			elif self.indent < global_indent[0]:
				raise Exception('more indent than expected')
		if func is None:
			func = self.append_to_curr_line
		self.check_first_line(first)
		self.start_of_line = line
		self.start_after_sep = sep
		func(item)

	def serialize(self, s, complete=True):
		if not self.started:
			return
		if not self.ended:
			# does not matter if ended or not
			self.end_state(False)
		self.exec_list.serialize(s, complete)
	
	def end_state(self, ended=True):
		if ended:
			self.ended = ended
		self.children = []
		self.children_ids = []
		for line in self.lines:
			for item in line:
				if item is SEPARATOR:
					break
				super().send_item(item)
			super().send_item('\n')
		for item in self.curr_line:
			super().send_item(item)
		self.parse_children()
		self.exec_list = self.conf_exec_list(self.lines)

	def parse_children(self):
		if len(self.productions) > 0:
			children = self.parse_productions()
		else:
			children = self.children
		self.lines = []
		self.curr_line = []
		for item in children:
			if item == '\n':
				self.push_curr_line()
			else:
				self.append_to_curr_line(item)
		self.end_line()

	def repr(self, s):
		self.exec_list.repr(s)

add_package(StateTabBlock(), 'tab_block', 'StateTabBlock')
