import kb
import os
import sys
import treesta
import hashlib
import utilities
import datak
import taster
import json

class Result:
	def __init__(self, method=-1, query = '', match='', confidence = 0):
		self.method = method
		self.match = match
		self.confidence = confidence
		self.query = query

	def success(self, method, match, confidence, query):
		self.method = method
		self.match = match
		self.confidence = confidence
		self.query = query

	def __str__(self):
		return "Matched " + self.query + " with " + str(self.match) + " using method "  + str(self.method) + " with confidence " + str(self.confidence)

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
		match.success(method = 1, match = str(title_hash), confidence = 1, query = ingredient)
		return match
	
	ingredient = kb.rejector.process(ingredient.strip('\n'))
	#hash check failed, try previous matches
	print(ingredient)
	if ingredient == '':
		return None
	matched_title = kb.matcher.match(ingredient.upper().strip())
	if matched_title is not None:
		match.success(query = ingredient, method = 2, match = matched_title, confidence = 1)
		return match

	#No approximate or exact match found, query nutritionix
	nutritionix_query = datak.ingredient(ingredient)
	print(nutritionix_query)
	if nutritionix_query is not None and nutritionix_query['food_name'][0].upper() == ingredient[0].upper():
		#Save the new nutrition information after standardizing and quantifying it
		if not os.path.exists(os.path.join('nutritionix_data', utilities.hash(nutritionix_query['food_name']))):
			print("Added new file for " + nutritionix_query['food_name'])
			with open(os.path.join('nutritionix_data', utilities.hash(nutritionix_query['food_name'])), 'w') as json_file:
				json.dump(nutritionix_query, json_file, indent='\t')
			taster.taste(utilities.standardize(utilities.hash(nutritionix_query['food_name'])))
		match.success(query = ingredient, method = 3, match = matched_title, confidence = 0.5)
		return match
	print("Nothing found for " + ingredient)
	#kb.matcher.add(nutritionix_query['food_name'], ingredient)
	return match

if __name__ == '__main__':
	with open(sys.argv[1]) as input_file:
		for line in input_file:
			print(nearest_ingredient(line.strip('\n')))
	kb.end()