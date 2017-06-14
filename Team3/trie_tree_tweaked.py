'''
Todoh:
[x] Build tree
[ ] Search Tree
[ ] Store and return taste scores
[ ] Condense 
'''
print(__doc__)

class TrieTreeNode():
	"""TrieTreeNode"""
	child_dict = dict()
	string = '$'
	def __init__(self, string):
		self.string = string

	def add_child(self, string):
		if not self.child_dict.__contains__(string): 
			self.child_dict[string] = TrieTreeNode(string)
			return self.child_dict[string]

	def __str__(self):
		self.class_print = dict()
		#self.class_print['child_dict'] = self.child_dict
		self.class_print['string'] = self.string
		return str(self.class_print)

	def get_index(self, string):
		if self.child_dict.__contains__(string):
			return self.child_dict[string]
		return None

	def get_children(self):
		print(len(self.child_dict))
		if len(self.child_dict) == 0:
			return None
		return self.child_dict.values()

class TrieTree():
	"""TrieTree main"""
	argument = "#"
	root = TrieTreeNode("#")
	head = None
	def __init__(self, argument):
		self.argument = argument
		self.add_word(argument)

	def add_word(self, word):
		self.head = self.root
		for letter in word:
			#print(self.head)
			if letter != ' ' and self.head.get_index(letter) is not None:
				self.head = self.head.get_index(letter)
			elif letter != ' ' and self.head.get_index(letter) is None:
				self.head = self.head.add_child(letter)

	def __str__(self):
		self.dft(self.root)
		return ''

	def dft(self, root):
		if root.get_children() is not None:	
			for node in root.get_children():
				self.dft(node)
		return None

		return str(return_list)

	def search_string(self, string):
		self.head = self.root		