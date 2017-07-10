import requests
import re
import hashlib
import os
import json
import utilities

query_url = 'https://www.nutritionix.com/track-api/v2/search/instant?branded=false&common=true&self=false&query='
#nutrition_url = 'https://www.nutritionix.com/nixapi/items/'
nutrition_common_url = 'https://www.nutritionix.com/track-api/v2/natural/nutrients'

def ingredient(query):
	print('\rQuerying for: ' + query.strip(), end='', flush=True)
	response = requests.get(query_url + utilities.parameterize(query))
	response = response.json()
	try:
		if len(response['common']) > 0:
			response = response['common'][0]
			title_hash = hashlib.md5(response['food_name'].upper().encode('utf-8')).hexdigest()
			if not os.path.exists(os.path.join('nutritionix_data', title_hash)):
				response_nutrition = requests.post(nutrition_common_url, data = {'query': response['food_name']})
				
				try:
					response_nutrition = response_nutrition.json()
					response_nutrition = response_nutrition['foods'][0]
				except json.decoder.JSONDecodeError:
					print(': ', response_nutrition.text, sep='')
					print('-'*15)

				print(', got ', response['food_name'], end=', ', sep='', flush=True)
				return response

		else:
			return None
	except KeyError as ke:
		pass

def leech(for_file):
	with open(for_file) as queries, open('misses_' + queries.name, 'w') as misses, open('discards_' + queries.name, 'w') as discards:

		for query in queries:
			returned_ingredient = ingredient(query.strip())
			if returned_ingredient is not None:
				modmatch_result = utilities.modmatch(query, returned_ingredient, 0.4)
				#Found a suitable result
				if modmatch_result is not None:					
					if not os.path.exists(os.path.join('nutritionix_data', for_file.split('.')[0])):
						os.makedirs(os.path.join('nutritionix_data', for_file.split('.')[0]))
					with open(os.path.join('nutritionix_data', os.path.join(for_file.split('.')[0], title_hash)), "w") as ing_file:
						json.dump(response_nutrition, ing_file, indent='\t')
				else:
					print(len(matched)/len(response['food_name'].split(' ')))
					print('discarded', end='*'*7)
					discards.write(str((query.strip(), response['food_name'])) + '\n')
			else:
				misses.write(query)

	print('\nDone.')