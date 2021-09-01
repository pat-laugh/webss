from libs.constants import lang_dict
from libs.state_container import StateContainer

from libs.lib_generator import add_package

class StateLineComment(StateContainer):
	def conf(self):
		self.id = 1
		self.name = 'Line Comment'
		self.desc = 'Consumes all chars up to a newline or end of file.'
		self.start_char = '# '
		self.end_char = '\\n,$EOF'
		self.consume_end = False

		self.start = lang_dict(['#', '//', '//', '#', '#'])
		self.end = lang_dict(['\n'] * 5)
		super().conf()
		self.cc_consume_end = lang_dict([False] * 5)
		self.set_consume_all_conf()

	def inst(self, parsed_start):
		super().inst(parsed_start)
		self.set_consume_all_inst()
		self.is_multiline = False

add_package(StateLineComment(), 'line_comment', 'StateLineComment')
