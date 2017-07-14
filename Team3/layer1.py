import csv
import glob
import utilities
import layer2
import os
import json
import re
import datak
import sys
import kb

SEARCH_THRESHOLD = 0.4
foodDict = dict()
rejector = kb.Rejector('dish_rejects.json')
acceptor = kb.Acceptor('dish_matches.json')
matcher = kb.Matcher('dish_matches.json')

def end():
	rejector.close()
	acceptor.close()
	matcher.close()
	
def get_data_from_JSON(foodItem):
	foodItem_hash = utilities.hash(foodItem)
	if os.path.exists('tasted_dishes/'+foodItem_hash+'.json'):
		with open('tasted_dishes/'+foodItem_hash+'.json') as f:
			return json.load(f)
	return None

def write_data_to_JSON(foodItem, nutri_info):
	foodItem_hash = utilities.hash(foodItem)
	with open('tasted_dishes/'+foodItem_hash+'.json','w') as f:
		json.dump(nutri_info,f,indent='\t')

	
def query_JSON(foodItem):
	if foodItem == '':
		return None

	result = get_data_from_JSON(foodItem)
	if result is not None:
		return result
	#2 - Check for aliases
	foodItem_match = matcher.match(foodItem.upper().strip())
	if foodItem_match is not None:
		return get_data_from_JSON(foodItem_match)
	#4 - return None
	return None

def return_score(foodItem):
	foodItem = re.sub(r"(without | WITHOUT) [A-Za-z]+",'',foodItem)
	print(foodItem)

	#Make sure it runs faster
	score = query_JSON(foodItem)
	if score:
		return score 

	score = query_nutritionix(foodItem)
	if score:
		return score
	return None

def query_nutritionix(foodItem):
	#3 - Query nutritionix to get nutritional info, but return an empty list for ingredients, and append it to the existing file

	nutri_info = dict()
	query_result = dict()
	food_hash = utilities.hash(foodItem)
	if os.path.exists("matched_dishes/" + food_hash + ".json"):
		with open("matched_dishes/" + food_hash + ".json") as queried_file:
			query_result = json.load(queried_file)
	else:
		query_result = datak.ingredient(foodItem)

	if query_result:
		if query_result['food_name'] != foodItem:
			matcher.add(query_result["food_name"], foodItem)
		food_weight = query_result['serving_weight_grams']
		nutri_info = dict()

		nutri_info["name"] = foodItem
		nutri_info['sweet'] = (query_result['nf_sugars'] / food_weight) if query_result['nf_sugars'] else 0
		nutri_info['salt'] = (query_result['nf_sodium'] / 39333) if query_result['nf_sodium'] else 0
		nutri_info['fat'] = (query_result['nf_total_fat'] / food_weight) if query_result['nf_total_fat'] else 0
		nutri_info['ingredients'] = list()
		write_data_to_JSON(foodItem, nutri_info)
		return nutri_info
	return None

if __name__ == "__main__":
	return_score(sys.argv[1])	
