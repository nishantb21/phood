from trie_tree_tweaked import Trie, Node
import sys
import utilities
trie = Trie()
fin_trie = Trie()
def condense(input_files):
	with open('condensed_file.txt', 'w') as fin_file:
		for file in input_files:
			with open(file) as ing_file:
				for ing in ing_file:
						trie.add(ing.strip('\n'))
						#print(ing)
			with open(file) as ing_file:
				for ing in ing_file:
					ing_list = trie.start_with_prefix(ing.strip('\n'))
					ing_len = map(lambda ingred: (ingred.strip('\n'), len(ingred)), ing_list)
					max_ing_len = ing_len.__next__()
					for ingred_len in ing_len:
						max_ing_len = ingred_len if ingred_len[1] > max_ing_len[1] else max_ing_len
					swp_result = fin_trie.start_with_prefix(max_ing_len[0])
					
					if len(swp_result) < 1:
						fin_trie.add(max_ing_len[0])			
						fin_file.write(max_ing_len[0] + '\n')

def check_ingredient(ingredient):
	matches = fin_trie.start_with_prefix(ingredient.upper())
	print(matches)	
	return ingredient if ingredient.upper() in matches else None

if __name__ == '__main__':
	condense(sys.argv[1:])
else:
	with open('condensed_file.txt') as trie_file:
		for line in trie_file:
			fin_trie.add(line.strip('\n'))