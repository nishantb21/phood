import kb
import os
import sys
import treesta
import hashlib
import utilities
import datak

class Result:
	def __init__(self, method=-1, match='', confidence = 0):
		self.method = method
		self.match = match
		self.confidence = confidence

	def success(self, method, match, confidence):
		self.method = method
		self.match = match
		self.confidence = confidence

	def __str__(self):
		return str(self.method) + str(self.match) + str(self.confidence)

def nearest_ingredient(ingredient):
	'''
	Flow:
	1. hash and check for exact match
	2. Query prefix tree and match closest ingredient
	3. Query nutritionix
	4. Ignore
	'''
	match = Result()
	#check 1
	title_hash = utilities.hash(ingredient.upper())
	if os.path.exists(os.path.join('nutritionix_data', title_hash + '_std.json')):
		match.success(method = 1, match = str(title_hash), confidence = 1)
		return match
	
	#hash check failed, try previous matches
	matched_title = kb.matcher.match(ingredient)
	if matched_title is not None:
		return utilities.hash(matched_title)

	'''
	cleaned_ingredient = kb.rejector.process(ingredient)
	print(cleaned_ingredient)
	matches = treesta.check_ingredient(cleaned_ingredient)
	modmatch_result = utilities.modmatch(cleaned_ingredient, matches, 0.6) if matches is not None else (None,)

	#match found with 2/3rd match
	if modmatch_result[0] is not None: 
		match.success(method = 2, match = hash(modmatch_result), confidence = modmatch_result[1])
		return match
'''
	#No approximate or exact match found, query nutritionix
	nutritionix_query = datak.ingredient(ingredient)
	nutritionix_query_result = treesta.check_ingredient(nutritionix_query['food_name'])
	if nutritionix_query_result is not None:
		match.success(method = 3, match = hash(nutritionix_query_result), confidence = 1)
		return match
	kb.matcher.add(nutritionix_query['food_name'], ingredient)
	return match

if __name__ == '__main__':
	with open(sys.argv[1]) as input_file:
		for line in input_file:
			print(nearest_ingredient(line.strip()))
	kb.end()