from libs.constants import lang_dict
from libs.constants import START_LIST, END_LIST
from libs.state_container import StateContainer

from libs.lib_generator import add_package

class StateJsx(StateContainer):
	def conf(self):
		self.id = 116
		self.name = 'JSX'
		self.desc = 'To denote JSX so it does not mess with Tab Blocks.'

		# TODO: JS start and end chars are a hack so they don't clash with data
		# tuples...
		self.start = lang_dict([None] * 2 + ['( ', None, '<jsx>'])
		self.end = lang_dict([None] * 2 + [' )', None, '</jsx>'])
		super().conf()
		self.set_consume_all_conf(True)
		self.separators = lang_dict([['\n']] * 5)

add_package(StateJsx(), 'jsx', 'StateJsx')
