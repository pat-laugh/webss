#!/usr/bin/env python3

import difflib, sys

from libs.constants import LANG_JS
from compile import compile

with open('./test-data/testinput.js.wbss') as f:
	test_input = f.read()

with open('./test-data/testoutput.js') as f:
	expected_output = f.read()

s = compile(test_input, 'config.json', LANG_JS)

# because Vim sillily adds newline
s += '\n'
if s != expected_output:
	print('----output----')
	print(s)
	print('----diff: expected (***) vs output (---)----')
	it = difflib.context_diff(expected_output.splitlines(), s.splitlines())
	while True:
		try:
			print(next(it))
		except StopIteration:
			break
print('Parse and serialize:', s == expected_output)
