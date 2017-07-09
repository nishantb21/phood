import json
'''
food name: food_name
serving size: serving_weight_grams
fat:
	nf_total_fat
	nf_saturated_fat
Salt: nf_sodium, nf_potassium
sugar: nf_sugars
protein: nf_protein
calories: nf_calories
---pairwise calculation:
carbs: nf_total_carbohydrate
'''
def standardize(input_file):
	nutrition_scrubbed = dict()
	with open(input_file) as json_file, open(input_file + '_std', 'w') as json_standardized:
		#print(input_file)
		nutrition = json.load(json_file)
		if nutrition['serving_weight_grams'] is not None:
			multiplier = round(100 / nutrition['serving_weight_grams'], 3)
		else:
			return None
		print('\r', input_file, ' : ', multiplier, sep='', end='\r', flush=True)
		key_list = ['nf_calories', 'nf_total_fat', 'nf_cholesterol', 'nf_sodium', 'nf_total_carbohydrate', 'nf_saturated_fat', 'nf_dietary_fiber', 'nf_sugars', 'nf_protein', 'nf_potassium']
		nutrition_scrubbed['food_name'] = nutrition['food_name']
		nutrition_scrubbed['nf_ndb_no'] = nutrition['ndb_no']
		nutrition_scrubbed['nf_upc'] = nutrition['upc']
		for key in key_list:			
			nutrition_scrubbed[key] = round(nutrition[key] * multiplier, 3) if nutrition[key] is not None else 0.0

		json.dump(nutrition_scrubbed, json_standardized, indent = '\t')