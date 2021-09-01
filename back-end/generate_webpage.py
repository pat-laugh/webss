#!/usr/bin/env python3

import json, os

from libs.lib_generator import get_packages
from libs.constants import LANG_WBSS

DIR_BE = '.'
DIR_FE = '../front-end'
DIR_HTML = os.path.join(DIR_FE, 'data')
DIR_OUT = os.path.join(DIR_FE, 'out')
FILE_HTML_1 = os.path.join(DIR_HTML, 'index-part-1.html')
FILE_HTML_2 = os.path.join(DIR_HTML, 'index-part-2.html')
FILE_CONFIG = os.path.join(DIR_BE, 'config.json')
FILE_INDEX = os.path.join(DIR_OUT, 'index.html')

def escape_chars(s):
	if s is None:
		return ''
	if type(s) is bool:
		return s
	s = s.replace('\n', '\\\\n') # React bug?
	s = s.replace(' ', '\u2423') # https://en.wikipedia.org/wiki/Unicode_control_characters
	return s

def read_file(f_name):
	with open(f_name) as f:
		return f.read()

def make_pkg_conf_dict(cls, selected_lang):
	return {
		'id': str(cls.id),
		'name': cls.name,
		'desc': cls.desc,
		'langs': {
			LANG_WBSS: {
				'start_char': escape_chars(cls.start[selected_lang]),
				'end_char': escape_chars(cls.end[selected_lang]),
				'consume_end': escape_chars(cls.cc_consume_end[selected_lang]),
			},
		},

		'selected_lang': selected_lang,
	}

def webpage_content():
	pkgs_classes = get_packages()

	pkgs = {}
	selected_lang = LANG_WBSS
	for id, pkg in pkgs_classes.items():
		cls, _, _ = pkg
		pkgs[id] = make_pkg_conf_dict(cls, selected_lang)

	html_1, html_2 = [read_file(x) for x in [FILE_HTML_1, FILE_HTML_2]]
	data_s = json.dumps(pkgs)
	with open(FILE_CONFIG) as f:
		data_config = json.dumps(json.loads(f.read()), separators=(',', ':'))
	
	return '\n'.join([
		html_1,
		'let ALL_PKGS = JSON.parse(\'%s\');' % data_s,
		'let CONFIG = \'%s\';' % data_config,
		html_2,
	])

if __name__ == '__main__':
	content = webpage_content()
	with open(FILE_INDEX, 'w') as f:
		f.write(content)
	print('Webpage: file://%s' % os.path.abspath(FILE_INDEX))
