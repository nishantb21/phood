from trie_tree_tweaked import TrieTree, TrieTreeNode

class TrieTest():
	def __init__(self):
		'''		s = "DARK CHOCOLATE; SUGAR; CHOCOLATE; COCOA BUTTER; MILK FAT; COCOA PROCESSED WITH ALKALI; SOY LECITHIN; MILK; SALT; NATURAL VANILLA FLAVOR; SUGAR; CORN SYRUP; FRUIT JUICE CONCENTRATE POMEGRANATE; APPLE; CRANBERRY; LEMON JUICE CONCENTRATES; MALTODEXTRIN; DEIONIZED APPLE JUICE CONCENTRATE; NATURAL FLAVORS; PECTIN; MALIC ACID; CANOLA OIL; SODIUM BICARBONATE; SODIUM CITRATE; ASCORBIC ACID; RESINOUS GLAZE; CITRIC ACID"
		for ing in s.split(";"):
			print(ing, TrieTree(ing))
		'''
		t = TrieTree("")
		t.add_word("i")
		t.add_word("in")
		t.add_word("inu")
		t.add_word("int")
		t.add_word("inui")
		t.add_word("inuit")
		t.add_word("intuit")
		print(t)

TrieTest()