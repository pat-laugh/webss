from libs.constants import lang_dict
from libs.state_nil import StateNil

from libs.lib_generator import add_package

class StateFile(StateNil):
	def conf(self):
		self.id = 0
		self.name = 'File'
		self.desc = 'Consumes all chars from the start to the end of file.'
		self.start_char = '$SOF'
		self.end_char = '$EOF'
		self.consume_end = False

		self.start = lang_dict([''] * 5)
		self.end = lang_dict([''] * 5)
		super().conf()

add_package(StateFile(), 'file', 'StateFile')
