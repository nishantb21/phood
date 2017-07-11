import json
import re
import itertools
import functools

ACCEPT_THRESHOLD = 0.32


class Rejector:
	def __init__(self, kb='rejects.json'):
		self.kb_file = kb
		self.rejects = open(self.kb_file)
		self.alphabets = json.load(self.rejects) or dict()
		self.punctuations = [',', '.', '{', '}', '[', ']', '(', ')', '\'', '"', ':', ';', '-', '/']

	def add(self, words):
		for word in words.strip().split(' '):
			self.alphabets[word.strip()[0]].extend(word.strip().split(' '))
			self.alphabets[word.strip()[0]] = list(set(self.alphabets[word.strip()[0]]))
		

	def close(self):
		with open(self.kb_file, 'w') as kb_file:			
			json.dump(self.alphabets, kb_file, indent='\t')

	def process(self, dirty_string):
		dirty_string = re.sub("\(.*\)", "", dirty_string)
		dirty_string = re.sub("[,.\{.*\}\[.*\]\'\"\:\;\-\\/&]*[0-9]*", "", dirty_string)
		dirty_string = re.sub("\(.*", "", dirty_string)
		dirty_string = re.sub(".*\)", "", dirty_string)
		dirty_string = re.sub("[ ]+", " ", dirty_string).strip().strip('\n')
		
		rejected_words = list()
		input_words = dirty_string.split(' ')
		for word in input_words:
			rejected_words.extend(self.alphabets[word[0].upper()])
		for product in itertools.product(rejected_words, input_words):
			
			if product[0] in product[1]:
				rejector.add(product[0])
				try:
					input_words.remove(product[1])
				except ValueError:
					pass
		if len(input_words) == 0:
			return ''
		clean_string = functools.reduce(lambda s,a: s+ ' ' + a, input_words)
		return clean_string

class Acceptor:
	def __init__(self, kb="condensed_file.json"):
		self.kb_file = kb
		self.accepted = open(self.kb_file)
		self.alphabets = json.load(self.accepted) or dict()

		def __enter__(self):
			return Acceptor()

	def add(self, word):
		self.alphabets[word.strip().upper()[0]].append(word.strip())
		self.alphabets[word.strip().upper()[0]] = list(set(self.alphabets[word.strip().upper()[0]]))

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def close(self):
		with open(self.kb_file, 'w') as kb_file:
			json.dump(self.alphabets, kb_file, indent='\t')		

	def process(self, dirty_string):
		clean_string = rejector.process(dirty_string)
		parts = clean_string.split(' ')
		parts_matched = 0
		for word in parts:
			match_candidates = self.alphabets[word.strip().upper()[0]]
			word = word.strip().upper()
			if word in match_candidates:
				parts_matched += 1
			else:
				rejector.add(word)

		if parts_matched / len(parts) > ACCEPT_THRESHOLD: 
			acceptor.add(clean_string)

class Matcher:
	def close(self):
		with open(self.kb_file, 'w') as kb_file:
			json.dump(self.hashes, kb_file, indent='\t')

	def __init__(self, kb="matches.json"):
		self.kb_file = kb
		self.matched = open(self.kb_file)
		self.hashes = json.load(self.matched)

	def add(self, title, match):
		main_key = self.hashes[title.upper()[0]]
		try:
			if title.upper()[0] == match[0].upper():
				list(set(main_key[title.upper()]["matches"])).append(match.upper())
				
		except KeyError:
			main_key[title.upper()] = dict({"matches": [match.upper()]})	
			

	def match(self, match_query):
		keys = self.hashes[match_query[0]]
		
		for key in keys.keys():
			if match_query.upper() in keys[key].get("matches"):
				return key
		return None

def end():
	matcher.close()
	rejector.close()
	acceptor.close()

matcher = Matcher()
rejector = Rejector()
acceptor = Acceptor()