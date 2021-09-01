#!/usr/bin/env python3

import json, os, sys

from libs.lib_generator import get_packages
from libs.compiler import CompilerEngine
from libs.constants import LANG_JS

FILE_CONFIG = 'config.json'
ID_ROOT = '0'
IDS_TO_IGNORE = [ID_ROOT, 'next_id']

def state_var_name(id):
	return 's_%s' % id

def compiler_conf_content(file_config):
	pkgs_classes = get_packages()

	with open(file_config) as f:
		data_config = json.loads(f.read())
	
	conf_root = data_config[ID_ROOT]
	ids_to_check = []
	for id, is_active in conf_root['pkgs_ids'].items():
		if is_active:
			ids_to_check.append(id)
	if len(ids_to_check) != 1:
		raise Exception('there can be only one active root package')
	root_state = state_var_name(ids_to_check[0])

	ids_checked = set()
	i = 0
	imports = []
	definitions = []
	assigns = []
	state_file_seen = False
	while i < len(ids_to_check):
		id = ids_to_check[i]
		i += 1
		if id in ids_checked:
			continue
		if id in IDS_TO_IGNORE:
			raise Exception('Incorrect ID among packages: %s' % id)
		ids_checked.add(id)

		conf = data_config[id]

		_, f_name, cls_name = pkgs_classes[int(conf['type'])]
		imports.append('from packages.%s import %s' % (f_name, cls_name))
		if not state_file_seen:
			if f_name == 'file' and cls_name == 'StateFile':
				state_file_seen = True
		curr_state = state_var_name(id)
		definitions.append('%s = %s()' % (curr_state, cls_name))
		for next_id, is_active in conf['pkgs_ids'].items():
			if is_active:
				ids_to_check.append(next_id)
				next_state = state_var_name(next_id)
				assigns.append('%s.add_st_to_events(%s)' % (curr_state, next_state))

	lines_out = [] + imports

	lines_out.append('''\

### State Stream 0

state_file = StateFile()
base_state_stream_0 = state_file
bss_0 = base_state_stream_0

### State Stream 1
''')

	lines_out += definitions + assigns

	lines_out.append('base_state_stream_1 = ' + root_state)
	lines_out.append('bss_1 = base_state_stream_1')

	return '\n'.join(lines_out)

def compile(input, file_conf, out_lang):
	g = {}
	exec(compiler_conf_content(file_conf), g, g)
	engine = CompilerEngine(g['bss_0'], g['bss_1'])
	compiler = engine.get_session(out_lang=out_lang)
	return compiler.parse(input, complete=True)

if __name__ == '__main__':
	USAGE = sys.argv[0] + ' file-in'
	if len(sys.argv) != 2 or sys.argv[1][-4:] == 'help':
		print(USAGE)
		sys.exit(2)
	file_in = sys.argv[1]
	with open(file_in) as f:
		print(compile(f.read(), FILE_CONFIG, LANG_JS))
