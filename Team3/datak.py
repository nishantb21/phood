import requests
import re
import hashlib
import os
import json
import utilities
import sys
import glob
from multiprocessing import Pool

query_url = 'https://www.nutritionix.com/track-api/v2/search/instant?branded=true&common=true&self=false&query='
nutrition_url = 'https://www.nutritionix.com/nixapi/items/'
nutrition_common_url = 'https://www.nutritionix.com/track-api/v2/natural/nutrients'

class NutritionixResponse:
	def __init__(self, item_type='common', name='name', item_id=None, nutrition_data = dict()):
		self.name = name
		self.item_id = item_id
		self.item_type = item_type
		self.nutrition_data = nutrition_data

	def __getitem__(self, key):
		try:
			return self.nutrition_data[key]
		except KeyError:
			return self.name

def ingredient(query):
	print('\rQuerying for: ' + query.strip(), end='\r', flush=True)
	response = requests.get(query_url + utilities.parameterize(query))
	response_json = response.json()
	try:
		if response.status_code == 200:
			'''
			if len(response_json['common']) > 0:
				#print("GOT: ", len(response_json['common']), response_json['common'])
				response_json = response_json['common'][0]
				title_hash = utilities.hash(response_json['food_name'])
			
				response_nutrition = requests.post(nutrition_common_url, data = {'query': response_json['food_name']})
				
				response_nutrition = response_nutrition.json()
				try:
					response_nutrition = response_nutrition['foods'][0]
				except json.decoder.JSONDecodeError:
					#print(': ', response_nutrition.text, sep='')
					#print('-'*15)
					pass

				#print(', got ', response_json['food_name'], end=', ', sep='', flush=True)
				return response_nutrition

			'''
			possible_matches = list()
			if len(response_json['common']) > 0:
				for rid in range(min(3, len(response_json['common']))):
					possible_matches.append(NutritionixResponse(item_type = 'common', name = response_json['common'][rid]['food_name'], item_id = None))
				
			elif len(response_json['branded']) > 0:
				for rid in range(min(3, len(response_json['branded']))):
					possible_matches.append(NutritionixResponse(item_type = 'branded', name = response_json['branded'][rid]['brand_name_item_name'], item_id = response_json['branded'][rid]['nix_item_id']))
			#print(query)
			best_match = utilities.modmatchir(query, possible_matches, 0.2)
			if best_match is not None:
				if best_match.item_type == 'common':
					response_nutrition = requests.post(nutrition_common_url, data = {"query": best_match.name})
					response_nutrition = response_nutrition.json()
					try:
						response_nutrition = response_nutrition['foods'][0]
					except json.decoder.DecodeError:
						pass
					return NutritionixResponse(name=response_nutrition['food_name'],
					                           item_type='common',
					                           nutrition_data = response_nutrition
					                           )

				response_nutrition = requests.get(nutrition_url + best_match.item_id)
				response_nutrition = response_nutrition.json()
				return NutritionixResponse(name=best_match.name,
				                           item_type='branded',
				                           item_id=best_match.item_id,
				                           nutrition_data = response_nutrition
				                           )
		else:
			return None
	except KeyError as ke:
		pass
'''
def leech(for_file, folder):
	with open(for_file) as queries, open('misses_' + queries.name, 'w') as misses, open('discards_' + queries.name, 'w') as discards:

		for query in queries:
			returned_ingredient = ingredient(query.strip())
			if returned_ingredient is not None:
				modmatch_result = utilities.modmatch(query, returned_ingredient, 0.4)
				#Found a suitable result
				if modmatch_result is not None:					
					if not os.path.exists(os.path.join(folder, for_file.split('.')[0])):
						os.makedirs(os.path.join(folder, for_file.split('.')[0]))
					with open(os.path.join(folder, os.path.join(for_file.split('.')[0], title_hash)), "w") as ing_file:
						json.dump(response_nutrition, ing_file, indent='\t')
				else:
					#print(len(matched)/len(response['food_name'].split(' ')))
					#print('discarded', end='*'*7)
					discards.write(str((query.strip(), response['food_name'])) + '\n')
			else:
				misses.write(query)

	print('\nDone.')
'''
def leech(for_file, folder):
	with open(for_file) as queries, open('misses_' + queries.name.split("/")[-1], 'w') as misses:

		for query in queries:
			returned_item = ingredient(query.strip())
			title_hash = utilities.hash(query)
			if returned_item is not None:
				if not os.path.exists(folder):
					os.makedirs(folder)
				if not os.path.exists(os.path.join(folder, title_hash + ".json")):
					with open(os.path.join(folder, title_hash + ".json"), "w") as ing_file:
						json.dump(returned_item.nutrition_data, ing_file, indent='\t')
			else:
				misses.write(query)

	#print('\nDone.')

def assign(values):
	leech(values, sys.argv[2])

if __name__ == '__main__':

	with Pool(8) as ppool:
		ppool.map(assign, glob.iglob(sys.argv[1] + "/food_names.*"))