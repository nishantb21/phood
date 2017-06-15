'''
Todoh:
[x] Build Tree
[x] Search the tree
[ ] Rainsum
( ) Condense
'''
print(__doc__)
taste_list = [
					'richness', 'sweet', 'sour', 'salt', 'umami', #Quantified
					'spicy', 'bitter', 'sour','wasabi'						#Boolean
				 ]

class Node:
	def __init__(self, letter = None, word = None, taste_dict = dict()):
		self.letter = letter
		self.word = word
		self.children = dict()
		self.taste_dict = taste_dict

	def add_child(self, letter, taste_dict = dict()):
		if not self.children.__contains__(letter):
			self.children[letter] = Node(letter, taste_dict = taste_dict)
		return self.children[letter]

	def __getitem__(self, key):
		if key in self.tastes.keys():
			return tastes[key]
		return 0

	def __str__(self):
		str_dict = dict()
		str_dict['letter'] = self.letter
		str_dict['taste_dict'] = self.taste_dict

class Trie:
	def __init__(self):
			self.head = Node("#")
	
	def __getitem__(self, key):
			return self.head.children[key]
	
	def add(self, word):
			current_node = self.head

			for letter in word:
					current_node = current_node.add_child(letter = letter)
			current_node.word = word
	
	def has_word(self, word):
		if word == '':
			return False
		if word == None:
			raise ValueError('Trie.has_word requires a not-Null string')

		# Start at the top
		current_node = self.head
		exists = True
		for letter in word:
			if letter in current_node.children:
					current_node = current_node.children[letter]
			else:
					exists = False
					break

		# Still need to check if we just reached a word like 't'
		# that isn't actually a full word in our dictionary
		if exists:
				if current_node.word == None:
						exists = False

		return exists
	
	def start_with_prefix(self, prefix):
		""" Returns a list of all words in tree that start with prefix """
		words = list()
		if prefix == None:
			raise ValueError('Requires not-Null prefix')
		
		# Determine end-of-prefix node
		top_node = self.head
		for letter in prefix:
			if letter in top_node.children:
				top_node = top_node.children[letter]
			else:				
				return words
				'''
				todoh:
				[ ] Add generalization (Common prefix success, 65% match)
				(?) Autocorrect
				'''
		
		# Get words under prefix
		if top_node == self.head:
			queue = [node for node in top_node.children.values()]
		else:
			queue = [top_node]
		
		while queue:
			current_node = queue.pop()
			if current_node.word != None:
				words.append(current_node.word)
			
			queue = [node for node in current_node.children.values()] + queue
		
		return words