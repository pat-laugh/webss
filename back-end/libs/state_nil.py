from libs.state_container import StateContainer

class StateNil(StateContainer):
	def conf(self):
		super().conf()
		self.set_consume_all_conf()
	
	def inst(self, parsed_start):
		super().inst(parsed_start)
		self.set_consume_all_inst()
