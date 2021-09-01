import importlib, os, sys

DIR_PKGS = './packages/'

packages = {}

class Package:
	def __init__(self):
		self.pkgs = []

def add_package(cls, f_name, cls_name):
	packages[cls.id] = (cls, f_name, cls_name)

def get_packages():
	try:
		files_pkgs = os.listdir(DIR_PKGS)
	except FileNotFoundError:
		raise

	sys.path.insert(0, DIR_PKGS)
	for file_pkg in files_pkgs:
		if len(file_pkg) < 3 or file_pkg[-3:] != '.py':
			continue
		file_pkg = file_pkg[:-3]
		# https://stackoverflow.com/a/42402095
		importlib.import_module(file_pkg)
	del sys.path[0]

	return packages
