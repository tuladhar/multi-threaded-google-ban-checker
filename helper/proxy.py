import re

TIMEOUT = 30
REGEX = re.compile(r'(?P<username>.+):(?P<password>.+)@(?P<proxy>.+):(?P<port>\d+)')

def is_valid(proxy):
	""" Proxy format:
	username:password@proxy:port
	"""
	proxy = proxy.strip()
	return REGEX.match(proxy)