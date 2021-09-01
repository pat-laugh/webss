CC_NEW_STATE, CC_END_STATE = [], []

DEF_VAL = []

COLON = ':'
SPACE = ' '
TAB = '\t'
NEWLINE = '\n'
STRING_ESCAPE = '\\'
SEPARATOR = []

START_DICT = '{'
START_LIST = '['
START_STRING_D = '\"'
START_STRING_S = '\''
START_TUPLE = '('
END_DICT = '}'
END_LIST = ']'
END_STRING_D = '\"'
END_STRING_S = '\''
END_TUPLE = ')'

INDENTATION = set([SPACE, TAB])

IGNORE = set()
for i in list(range(0, 9)) + list(range(11, 32)) + [127]:
	IGNORE.add(i)

LANG_BASH = 'bash'
LANG_CPP = 'cpp'
LANG_JS = 'js'
LANG_PY = 'py'
LANG_WBSS = 'wbss'
LANGS = [LANG_BASH, LANG_CPP, LANG_JS, LANG_PY, LANG_WBSS]

class lang_dict:
	def __init__(self, items=None):
		self.d = {}
		if type(items) is list:
			it = iter(items)
			for lang in LANGS:
				self.d[lang] = next(it)
		elif type(items) is dict:
			for lang, val in items.items():
				self.d[lang] = val
	
	def __getitem__(self, key):
		if key in self.d:
			return self.d[key]
		le = lang_equivalent(key)
		if type(le) is list:
			for item in le[:-1]:
				try:
					return self[item]
				except KeyError:
					pass
			return self[le[-1]]
		assert(type(le) is str)
		return self[le]
	
	def __setitem__(self, key, value):
		self.d[key] = value
	
	def __iter__(self):
		return iter(self.d)
	
	def items(self):
		return self.d.items()

def lang_equivalent(lang):
	return lang_equivalents[lang]

LANG_SQL = 'sql'
LANG_SQAL = 'sqal'

lang_equivalents = {
	LANG_SQL: LANG_CPP,
	LANG_SQAL: LANG_PY,
}
