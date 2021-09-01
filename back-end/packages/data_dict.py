from libs.constants import lang_dict
from libs.constants import START_DICT, END_DICT
from libs.state_container import StateContainer

from libs.lib_generator import add_package

class StateDataDict(StateContainer):
	def conf(self):
		self.id = 4
		self.name = 'Data Dict'
		self.desc = 'Dictionary with optional comma separators.'

		self.start = lang_dict([None] * 2 + ['{'] * 2 + [START_DICT])
		self.end = lang_dict([None] * 2 + ['}'] * 2 + [END_DICT])
		super().conf()

add_package(StateDataDict(), 'data_dict', 'StateDataDict')
