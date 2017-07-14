import kb
import os
import sys
import hashlib
import utilities
import datak
import taster
import json
import itertools

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
		return str(self.match)

def nearest_ingredient(ingredient):
	'''
	Flow:
	1. hash and check for exact match
	2. Query match closest ingredient with known aliases
	3. Query nutritionix
	4. Ignore
	'''
	original_ingredient = ingredient
	match = Result()
	#check 1
	title_hash = utilities.hash(ingredient.upper())

	if os.path.exists(os.path.join('nutritionix_data', title_hash + '_std.json')):
		match.success(method = 1, match = ingredient, confidence = 1, query = ingredient)
		return match

	
	ingredient = kb.rejector.process(ingredient.strip('\n'))

	#hash check failed, try previous matches
	if ingredient == '':
		return None
	matched_title = kb.matcher.match(ingredient.upper().strip())
	if matched_title is not None:
		match.success(query = ingredient, method = 2, match = matched_title, confidence = 1)
		return match

	#No approximate or exact match found, query nutritionix
	nutritionix_query = datak.ingredient(ingredient)

	if nutritionix_query is not None and nutritionix_query.name.upper()[0] == ingredient[0].upper():
		#Save the new nutrition information after standardizing and quantifying it
		if not os.path.exists(os.path.join('nutritionix_data', utilities.hash(nutritionix_query.name))):

			with open(os.path.join('nutritionix_data', utilities.hash(nutritionix_query.name)), 'w') as json_file:
				json.dump(nutritionix_query.nutrition_data, json_file, indent='\t')
			taster.taste(utilities.standardize(utilities.hash(nutritionix_query.name)))
			kb.acceptor.add(nutritionix_query.name)
		else:

			kb.matcher.add(nutritionix_query.name, ingredient)
		match.success(query = ingredient, method = 3, match = nutritionix_query.name, confidence = 0.8)
		return match

	kb.rejector.add(ingredient)
	return match

def profile(dish_title, ingredient_list):
	if len(ingredient_list) == 0 or ingredient_list is None:
		return None
	taste_keys = ["sweet_score", "salt_score", "rich_score"]
	json_keys = ["sweet", "salt", "fat"]

	dish_hash = utilities.hash(dish_title)

	#format: [(ingredient, ratio%)]
	ingredient_pair = zip(ingredient_list, utilities.ratio(len(ingredient_list)))
	if not os.path.exists(os.path.join("tasted_dishes", dish_hash)):
		
		#format: ((ingredient, ratio%), taste_key)
		taste_ingredient_pair = itertools.product(ingredient_pair, taste_keys)
		profile = dict()
		for pair in taste_ingredient_pair:
			matched_ingredient = nearest_ingredient(pair[0][0])

			if matched_ingredient is not None and matched_ingredient.match != '':

				#read ingredient details from file
				print(matched_ingredient.match)
				with open("nutritionix_data/" + utilities.hash(matched_ingredient.match) + "_std.json") as ing_file:
					ing_dict = json.load(ing_file)
					try:
						profile[pair[1]] += round(ing_dict[pair[1]] * pair[0][1], 4) / 100
					except KeyError:
						profile[pair[1]] = round(ing_dict[pair[1]] * pair[0][1], 4) / 100
					finally:
						if pair[1] == taste_keys[-1]:
							profile['ingredients'] = ingredient_list
							profile['name'] = dish_title
							with open(os.path.join("tasted_dishes", dish_hash), 'w') as tasted_dish_file:
								json.dump(profile, tasted_dish_file, indent='\t')

		return (dish_title, ingredient_list, profile)

	#Read from precomputed file and return 

	dish_values = dict()
	with open("tasted_dishes/" + dish_hash) as dish_json:
		dish_values = json.load(dish_json)
		print(dish_values)
	return (dish_title, ingredient_list, dish_values)

def assign(values):
	profile(values, sys.argv[2])

if __name__ == '__main__':
	with open(sys.argv[1]) as input_file:
		with Pool(10) as ppool:
			ppool.map(assign, input_file)
	kb.end()