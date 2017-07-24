#generate taste scores
import json
import glob, sys
import utilities
import itertools
import numpy
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

SWEET_FACTOR_X = 0.9
SWEET_FACTOR_Y = 0.1

RICHNESS_FACTOR_X = 0.5
RICHNESS_FACTOR_Y = 0.7
RICHNESS_FACTOR_Z = 50

SOURNESS_FACTOR_X = 0.1
SOURNESS_FACTOR_Y = 0.25
SOURNESS_FACTOR_Z = 0.5

def sweet(nutrition_data, SWEET_FACTOR_X=0.85, SWEET_FACTOR_Y=0.1):
	for key in nutrition_data.keys():
		if nutrition_data[key] is None:
			nutrition_data[key] = 0
	try:
		total_weight = nutrition_data['metric_qty']
		sweet_score_x1 = abs(nutrition_data['sugars'] - nutrition_data['dietary_fiber']) / total_weight
		sweet_score_y = nutrition_data['sugars'] / nutrition_data['total_carb']
		sweet_score_1 = (SWEET_FACTOR_X * sweet_score_x1) + (SWEET_FACTOR_Y * sweet_score_y)
		#	print(sweet_score_1)
	except Exception as e:
		sweet_score_1 = 0
	return round(sweet_score_1*10 / 0.998,3)

def rich(nutrition_data, RICHNESS_FACTOR_X=0.2, RICHNESS_FACTOR_Y=1.3,RICHNESS_FACTOR_Z=50):
	for key in nutrition_data.keys():
		if nutrition_data[key] is None:
			nutrition_data[key] = 0
	try:
		total_weight = nutrition_data['metric_qty']
		richness_score_x = nutrition_data['saturated_fat'] / nutrition_data['total_fat'] #high
		#Why consider sat_fat if we're considering total fat anyway? Would make more sense if total fat wasn't available
		richness_score_y = nutrition_data['total_fat'] / total_weight #low
		#Why is this not enough to work off of?
		richness_score_z = nutrition_data['cholesterol'] / (total_weight * 1000)
		#I'll admit that this is a good idea anyway
		richness_score_1 = (RICHNESS_FACTOR_X * richness_score_x) + (RICHNESS_FACTOR_Y * richness_score_y) + (RICHNESS_FACTOR_Z * richness_score_z)
	except Exception as e:
		richness_score_1 = 0

	return round((richness_score_1 * 10/ 0.992),3)
	## Normalize to butter which has highest score

def sour(dish_title, nutrition_data, SOURNESS_FACTOR_X=0.1, SOURNESS_FACTOR_Y=0.25, SOURNESS_FACTOR_Z=0.5):
	total_weight = nutrition_data['total_carb'] + nutrition_data['protein'] + nutrition_data['total_fat']
	food_words = dish_title.upper().split(' ')
	#print(food_words)
	try:
		vitamin_c = nutrition_data['vitamin_c']
	except KeyError as ke:
		vitamin_c = 0.0
	#print(vitamin_c)
	with open('sour.json') as f:
		sour = json.load(f)
		#print(sour)
	with open('too_sour.json') as f:
		too_sour = json.load(f)
	try:
		sour_score_x = vitamin_c / total_weight
	except ZeroDivisionError as zde:
		sour_score_x = 0

	sour_score_y = 0
	sour_score_z = 0

	for word in food_words:
		if word in sour[word[0]]:
			#print("found s", word)
			sour_score_y += 1
		if word in too_sour[word[0]]:
			sour_score_z += 1
	sour_score = round(((SOURNESS_FACTOR_X * sour_score_x) + (SOURNESS_FACTOR_Y * sour_score_y) + (SOURNESS_FACTOR_Z * sour_score_z)) / 0.995,3)
	#print(sour_score)
	if sour_score > 1 :
		sour_score = 1
	return round(sour_score * 10, 3)

def spicy(dish_title):
	food_words = dish_title.upper().split(' ')
	with open('spicy.json') as f:
		spice = json.load(f)
	for word in food_words:
		if word in spice[word[0]]:
			return True
	return False

def taste(file):
	if file is not None:
		with open(file) as input_file, open(file + '.json', 'w') as sampled_json:
			try:
				ingredient = json.load(input_file)
				#print('\r', file, sep='', end='')
				ingredient['sweet_score'] = round(ingredient['nf_sugars'] / 10, 4)
				ingredient['salt_score'] = round(ingredient['nf_sodium'] / 39333, 4)
				ingredient['rich_score'] = round((ingredient['nf_total_fat'] + ingredient['nf_saturated_fat']) / 10, 4)
				json.dump(ingredient, sampled_json, indent='\t')

			except json.decoder.JSONDecodeError:
				#print('\rDecode error for file {0}'.format(file))
				pass

def match_descriptors(dish_title, descriptor_dict):
	dish_split = dish_title.split(" ")
	final_scores = dict()
	for item in descriptor_dict:
		for pair in itertools.product(item['items'].items(),dish_split):
		#format ((descriptor, score), dish_word)
			if pair[0][0].lower() in pair[1].lower():
				try:
					final_scores[item["name"]] += pair[0][1]
				except KeyError:
					final_scores[item["name"]] = pair[0][1]
	return final_scores


def umami(dish_title, nutrition_data, PROTEIN_SUPPLEMENT_MULTIPLIER = 0.80, VEGETABLES_MULTIPLIER = 2.40, MEAT_MULTIPLIER = 3.45, STRING_MULTIPLIER = 9.45):
	for key in nutrition_data.keys():
		if nutrition_data[key] is None:
			nutrition_data[key] = 0

	umami_descriptors = utilities.read_json("umami_descriptors.json")
	descriptor_score = match_descriptors(dish_title, umami_descriptors)
	#print(descriptor_score)
	umamiscore =  nutrition_data["protein"] / total_weight(nutrition_data)

	pairings = zip([PROTEIN_SUPPLEMENT_MULTIPLIER, VEGETABLES_MULTIPLIER, MEAT_MULTIPLIER, STRING_MULTIPLIER], ["protein_supps", "vegetables", "meat", "savory_strings"])
	for pair in pairings:
		#umamiscore = 1.5meat + 2veggies + 1protein_supps
		if descriptor_score.__contains__(pair[1]):

			umamiscore += pair[0] * descriptor_score[pair[1]] * 1
	umamiscore *= 10
	#return round(umamiscore, 3) if umamiscore <= 10 else round(umamiscore%10, 3)
	return round(umamiscore, 3)

def total_weight(dish_nutrition):
	return dish_nutrition['total_fat'] + dish_nutrition['total_carb'] + dish_nutrition['protein']

def salt(dish_nutrition):
	for key in dish_nutrition.keys():
		if dish_nutrition[key] is None:
			dish_nutrition[key] = 0
	totalweight = total_weight(dish_nutrition)
	if totalweight == 0:
		return dish_nutrition['sodium'] / dish_nutrition['metric_qty'] / 3.8758
	#return((dish_nutrition['sodium'] / dish_nutrition['metric_qty']))
	#print((dish_nutrition['sodium'] / dish_nutrition['metric_qty']) / 38.758, end=' | ')
	return round((dish_nutrition['sodium'] / totalweight) / 3.8758, 3)

def bitter(dish_title, nutrition_data, LEVEL1_MULTIPLIER = 0.80, LEVEL2_MULTIPLIER = 1.40, MULTI_WORD_MULTIPLIER=2.3):
	bitter_descriptors = utilities.read_json("bitter_descriptors.json")
	descriptor_score = match_descriptors(dish_title, bitter_descriptors)
	#print(LEVEL1_MULTIPLIER, LEVEL2_MULTIPLIER, end=': ')
	bitterscore = nutrition_data["iron"] / total_weight(nutrition_data)
	pairings = zip([LEVEL1_MULTIPLIER, LEVEL2_MULTIPLIER, MULTI_WORD_MULTIPLIER], ["bitter_l1", "bitter_l2", "multi_words"])
	for pair in pairings:
		if descriptor_score.__contains__(pair[1]):
			bitterscore += pair[0] * descriptor_score[pair[1]] * 1
	return round(bitterscore / 1.4571, 3)

def taste_dish(jv):
	return {
			"sweet": sweet(jv),
			"rich": rich(jv),
			"sour": sour(jv["item_name"], jv),
			"spicy": spicy(jv["item_name"]),
			"umami": umami(jv["item_name"], jv),
			"bitter": bitter(jv["item_name"], jv),
			"salt": salt(jv)
}
if __name__ == "__main__":
	for taste in ["sweet", "rich", "sour", "spicy", "umami", "bitter", "salt"]:
		results = list()
		for file in glob.iglob(taste + "/*.json"):
			with open(file) as infile:
				# print(file, end=': ')
				# print(salt(json.load(infile)))
				jv = json.load(infile)
				result = taste_dish(jv)
				print(result)
				results.append({"name": file.split("/")[-1].split(".")[0], "value": result})
'''
		print(taste, results)
		objects = tuple([title["name"] for title in results])
		performance = [value[taste] for value in [title["value"] for title in results]]
		print(objects, performance)

		y_pos = np.arange(len(objects))
		plt.bar(y_pos, performance, align='center', alpha=0.5)
		plt.xticks(y_pos, objects)
		plt.ylabel('Usage')
		plt.title('Taste: {}'.format(taste))

		plt.show()
'''