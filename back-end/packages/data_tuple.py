from libs.constants import lang_dict
from libs.constants import LANG_PY, START_TUPLE, END_TUPLE
from libs.state_container import StateContainer

from libs.lib_generator import add_package

class StateDataTuple(StateContainer):
	def conf(self):
		self.id = 6
		self.name = 'Data Tuple'
		self.desc = 'Tuple with optional comma separators.'

		self.start = lang_dict(['('] * 4 + [START_TUPLE])
		self.end = lang_dict([')'] * 4 + [END_TUPLE])
		super().conf()

	def skip_last_sep(self):
		return lang_dict([True] * 3 + [False, True])[self.lang]

add_package(StateDataTuple(), 'data_tuple', 'StateDataTuple')
