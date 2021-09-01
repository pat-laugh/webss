from libs.constants import lang_dict
from libs.constants import LANG_CPP
from libs.constants import COLON, START_LIST, END_LIST
from libs.state_container import StateContainer

from libs.lib_generator import add_package

class StateExecList(StateContainer):
	def conf(self):
		self.id = 3
		self.name = 'Exec List'
		self.desc = 'List containing commands, instead of data.'

		self.start = lang_dict([' {', ' {', ' {', ':', COLON + START_LIST])
		self.end = lang_dict(['}', '}', '}', '', END_LIST])
		super().conf()
		self.sep_last_line = lang_dict([False, True, True] + [False] * 2)
		self.separators = lang_dict([[';', '\n']]
			+ [[';']] * 2
			+ [[';', '\n']]
			+ [[';', '']]
		)
	
	def out_multiline(self):
		return True

add_package(StateExecList(), 'exec_list', 'StateExecList')
