from trie_tree_tweaked import Trie, Node

class TrieTest():
	def __init__(self):
		'''		s = "DARK CHOCOLATE; SUGAR; CHOCOLATE; COCOA BUTTER; MILK FAT; COCOA PROCESSED WITH ALKALI; SOY LECITHIN; MILK; SALT; NATURAL VANILLA FLAVOR; SUGAR; CORN SYRUP; FRUIT JUICE CONCENTRATE POMEGRANATE; APPLE; CRANBERRY; LEMON JUICE CONCENTRATES; MALTODEXTRIN; DEIONIZED APPLE JUICE CONCENTRATE; NATURAL FLAVORS; PECTIN; MALIC ACID; CANOLA OIL; SODIUM BICARBONATE; SODIUM CITRATE; ASCORBIC ACID; RESINOUS GLAZE; CITRIC ACID"
		for ing in s.split(";"):
			print(ing, TrieTree(ing))
		'''
		trie = Trie()
		words = 'i in int intuit inuit'
		for word in words.split():
				trie.add(word)
		print(trie.start_with_prefix('int'))

TrieTest()