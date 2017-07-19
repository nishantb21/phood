#generate taste scores
import json
import glob, sys

PROTEIN_SUPPLEMENT_MULTIPLIER = 1
VEGETABLES_MULTIPLIER = 2
MEAT_MULTIPLIER = 1.5

def taste(file):
	if file is not None:
		with open(file) as input_file, open(file + '.json', 'w') as sampled_json:
			try:
				ingredient = json.load(input_file)
				#print('\r', file, sep='', end='')
				ingredient['sweet_score'] = round(ingredient['nf_sugars'] / 100, 4)
				ingredient['salt_score'] = round(ingredient['nf_sodium'] / 39333, 4)
				ingredient['rich_score'] = round((ingredient['nf_total_fat'] + ingredient['nf_saturated_fat']) / 100, 4)
				json.dump(ingredient, sampled_json, indent='\t')
			
			except json.decoder.JSONDecodeError:
				#print('\rDecode error for file {0}'.format(file))
				pass

def match_descriptors(dish_title, descriptor_dict):
	dish_split = dish_title.split(" ")
	final_scores = dict()
	for item in descriptor_dict:
		for pair in itertools.product(dish_split, item['items']):
		#format (dish_word, (descriptor, score))
		if pair[0] in pair[1][0]:
			try:
				final_scores[taste_key] += pair[1][1]
			except KeyError:
				final_scores[taste_key] = pair[1][1]
	return final_scores


def umami(dish_title, nutrition_data, PROTEIN_SUPPLEMENT_MULTIPLIER = 1, VEGETABLES_MULTIPLIER = 2, MEAT_MULTIPLIER = 1.5):
	umami_vegetables = dict()
	umami_meats = dict()
	umami_protein_supps = dict()
	umami_descriptors = utilities.read_json("umami_descriptors.json")	
	for category in umamitypes:
		descriptor_score = match_descriptors(dish_title, umami_descriptors, category)
	#score = 1.5meat + 2veggies + 1protein_supps
	

def salt(dish_nutrition):
	total_weight = dish_nutrition['total_fat'] + dish_nutrition['total_carb'] + dish_nutrition['protein']
	if total_weight == 0:
		return dish_nutrition['sodium'] / dish_nutrition['metric_qty'] / 3.8758
#	return((dish_nutrition['sodium'] / dish_nutrition['metric_qty']))
	#print((dish_nutrition['sodium'] / dish_nutrition['metric_qty']) / 38.758, end=' | ')
	return ((dish_nutrition['sodium'] / total_weight)) / 3.8758

if __name__ == "__main__":
	for file in glob.iglob(sys.argv[1] + "/*.json"):
		print(file, end=': ')
		with open(file) as infile:
			print(salt(json.load(infile)))