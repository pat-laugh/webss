from libs.constants import lang_dict
from libs.constants import START_LIST, END_LIST
from libs.state_container import StateContainer

from libs.lib_generator import add_package

class StateDataList(StateContainer):
	def conf(self):
		self.id = 5
		self.name = 'Data List'
		self.desc = 'List with optional comma separators.'

		self.start = lang_dict([None] * 2 + ['['] * 2 + [START_LIST])
		self.end = lang_dict([None] * 2 + [']'] * 2 + [END_LIST])
		super().conf()

add_package(StateDataList(), 'data_list', 'StateDataList')
