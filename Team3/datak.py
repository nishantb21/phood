import requests
import re
import hashlib
import os
import json

query_url = 'https://www.nutritionix.com/track-api/v2/search/instant?branded=false&common=true&self=false&query='
#nutrition_url = 'https://www.nutritionix.com/nixapi/items/'
nutrition_common_url = 'https://www.nutritionix.com/track-api/v2/natural/nutrients'

def leech(for_file):
	with open(for_file) as queries, open('misses_' + queries.name, 'w') as misses, open('discards_' + queries.name, 'w') as discards:
		def parameterize(qstring):
			return qstring.strip('\n').replace(' ', '+')

		for query in queries:
			print('\rQuerying for: ' + query.strip(), end='', flush=True)
			response = requests.get(query_url + parameterize(query))
			response = response.json()
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
					matched = [word for word in query.strip().split(' ') if word in response['food_name'].upper().split(' ')]
					#print(matched, end=' : ')
					if len(matched)/len(response['food_name'].split(' ')) < 0.4:
						print(len(matched)/len(response['food_name'].split(' ')))
						print('discarded', end='*'*7)
						discards.write(str((query.strip(), response['food_name'])) + '\n')
					else:
						with open(os.path.join('nutritionix_data', title_hash), "w") as ing_file:
							json.dump(response_nutrition, ing_file)
			else:
				misses.write(query)
	print('\nDone.')