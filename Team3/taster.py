#generate taste scores
import json

def taste(file):
	with open(file) as input_file, open(file + '.json', 'w') as sampled_json:
		try:
			ingredient = json.load(input_file)
			print('\r', file, sep='', end='')
			ingredient['sweet_score'] = round(ingredient['nf_sugars'] / 100, 4)
			ingredient['salt_score'] = round(ingredient['nf_sodium'] / 39333, 4)
			ingredient['rich_score'] = round((ingredient['nf_total_fat'] + ingredient['nf_saturated_fat']) / 100, 4)
			json.dump(ingredient, sampled_json, indent='\t')
		
		except json.decoder.JSONDecodeError:
			print('\rDecode error for file {0}'.format(file))