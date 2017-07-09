import json

ACCEPT_THRESHOLD = 0.32


class Rejector:
	def __init__(self, kb='rejects.json'):
		self.kb_file = kb
		self.rejects = open(self.kb_file)
		self.alphabets = json.load(self.rejects) or dict()
		self.punctuations = [',', '.', '{', '}', '[', ']', '(', ')', '\'', '"', ':', ';']

	def add(self, word):
		self.alphabets[word.strip()[0]].add(word.strip())

	def close(self):
		with open(self.kb_file, 'w') as kb_file:			
			json.dump(self.alphabets, kb_file, indent='\t')

	def process(self, dirty_string):
		for punctuation in self.punctuations:
			dirty_string = dirty_string.replace(punctuation, '')
		
		for rword in self.rejects:			
			dirty_string = dirty_string.replace(rword, '\b')

		return dirty_string

class Acceptor:
	def __init__(self, kb="condensed_file.json"):
		self.kb_file = kb
		self.accepted = open(self.kb_file)
		self.alphabets = json.load(self.accepted) or dict()

		def __enter__(self):
			return Acceptor()

	def add(self, word):
		self.alphabets[word.strip()[0]].add(word.strip())

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def close(self):
		with open(self.kb_file, 'w') as kb_file:
			json.dump(self.alphabets, kb_file, indent='\t')		

	def process(dirty_string):
		clean_string = rejector.process(dirty_string)
		parts = clean_string.split(' ')
		parts_matched = 0
		for word in parts:
			word = word.strip().upper()
			if word in self.alphabets[word[0]]:
				parts_matched+= parts_matched
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
		#print(title)
		main_key = self.hashes[title.upper()[0]]
		try:
			if title.upper()[0] is match[0].upper():
				list(set(main_key[title.upper()]["matches"])).append(match.upper())
		except KeyError:
			main_key[title.upper()] = dict({"matches": [match.upper()]})	
		#print(title, match)		

	def match(self, match_query):
		keys = self.hashes[match_query[0]]
		#print(keys)
		for key in keys.keys():
			if match_query.upper() in keys[key].get("matches"):
				print('Matched: ', key, ' with ', match_query)
				return key
		return None


def end():
	matcher.close()
	rejector.close()
	acceptor.close()

matcher = Matcher()
rejector = Rejector()
acceptor = Acceptor()