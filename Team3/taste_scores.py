#generate taste scores
import json

def generate(file):
	with open(file) as input_file, open(file.split('_')[0] + '.json') as sampled_json:
		ingredient = json.load(input_file)
		ingredient['sweet_score'] = ingredient['nf_sugars'] / 100
		ingredient['salt_score'] = ingredient['nf_sodium'] / 39333
		ingredient['rich_score'] = (ingredient['nf_total_fat'] + ingredient['nf_saturated_fat']) / 100
		json.dump(ingredient, sampled_json, indent='\t')