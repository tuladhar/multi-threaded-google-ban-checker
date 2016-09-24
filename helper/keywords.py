import random

# TODO: load from file
with open('helper/ipcheck_keywords.txt', 'r') as f:
	keywords = [keyword.strip() for keyword in f if keyword.strip()]

def get_random_keyword():
	# NOTE: spaces are converted to '+'
	return random.choice(keywords).replace(' ', '+')