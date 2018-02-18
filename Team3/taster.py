import json
import re
import utilities
import argparse

SWEET_FACTOR_X = 0.9
SWEET_FACTOR_Y = 0.1

RICHNESS_FACTOR_X = 0.5
RICHNESS_FACTOR_Y = 0.7
RICHNESS_FACTOR_Z = 50

SOURNESS_FACTOR_X = 0.1
SOURNESS_FACTOR_Y = 0.25
SOURNESS_FACTOR_Z = 0.5


def sweet(nutrition_data, SWEET_FACTOR_X=0.9, SWEET_FACTOR_Y=0.1):
	try:
		total_weight = nutrition_data['Weight']
		fibtg = 0
		if 'Dietary_Fiber' in nutrition_data:
				fibtg = nutrition_data['Dietary_Fiber']
		sweet_score_x1 = abs(nutrition_data['Sugar'] - fibtg) / total_weight
		sweet_score_y = nutrition_data['Sugar'] / nutrition_data['Carbs']
		sweet_score_1 = (SWEET_FACTOR_X * sweet_score_x1) + (SWEET_FACTOR_Y * sweet_score_y)

	except Exception:
		sweet_score_1 = 0
	return round(sweet_score_1 / 0.998,3) * 10


def rich(nutrition_data, RICHNESS_FACTOR_X=0.5, RICHNESS_FACTOR_Y=0.7,RICHNESS_FACTOR_Z=50):
	try:
		#total_weight = nutrition_data['metric_qty']
		total_weight = nutrition_data['Weight']
		richness_score_x = 0
		if 'Sat_Fat' in nutrition_data:
			richness_score_x = nutrition_data['Sat_Fat'] / nutrition_data['Fat'] #high
		#Why consider sat_fat if we're considering total fat anyway? Would make more sense if total fat wasn't available
		richness_score_y = nutrition_data['Fat'] / total_weight #low
		#Why is this not enough to work off of?
		richness_score_z = 0
		if 'Cholesterol' in nutrition_data:
			richness_score_z = nutrition_data['Cholesterol'] / (total_weight * 1000)
		#I'll admit that this is a good idea anyway
		richness_score_1 = (RICHNESS_FACTOR_X * richness_score_x) + (RICHNESS_FACTOR_Y * richness_score_y) + (RICHNESS_FACTOR_Z * richness_score_z)
	except Exception:
		richness_score_1 = 0

	return round((richness_score_1 / 0.992),3) * 10
	# Normalize to butter which has highest score


def salt(dish_nutrition):
	totalweight = dish_nutrition['Weight']
	if totalweight == 0:
		return 0
	return ((1000 * dish_nutrition['Sodium'] / totalweight)) / 3.8758


def get_dishes():
	with open('testset.json') as json_file:
		foods_list = json.load(json_file)

	return foods_list


def total_weight(dish_nutrition):
	totalweight = 0
	for nutrient in dish_nutrition:
		if dish_nutrition[nutrient] is not None and 'g' in dish_nutrition[nutrient][0]:
			number = re.findall('(\d+\.\d+|\d+)', dish_nutrition[nutrient][0])
			numeric_value = 0
			if len(number) > 0:
				numeric_value = float(number[0])
				if 'mg' in dish_nutrition[nutrient][0]:
					numeric_value /= 100
			totalweight += numeric_value
	return totalweight


def get_nutrients(food):
	nutrients = food['nutrients']
	totalweight = total_weight(nutrients)
	for nutrient in nutrients:
		if nutrients[nutrient] is not None:
			nutrient_str = nutrients[nutrient][0]
			number = re.findall('(\d+\.\d+|\d+)', nutrient_str)
			if len(number) > 0 :
				if 'mg' in nutrients[nutrient][0]:
					nutrients[nutrient] = float(number[0]) / 1000
				else:
					nutrients[nutrient] = float(number[0])
			else:
				nutrients[nutrient] = 0
	nutrients['Weight'] = totalweight
	return nutrients


def taste(food):
		nutrients = get_nutrients(food)
		taste_scores = {
		"sweet": round(sweet(nutrients), 2),
		"salt": round(salt(nutrients), 2),
		"rich": round(rich(nutrients), 2)
		}
		tags = get_cuisine_tags(food)
		cuisine_multipliers = get_cuisine_multipliers(tags)
		taste_scores = update_scores(taste_scores, cuisine_multipliers)
		return taste_scores


def update_scores(taste_scores, cuisine_multipliers):
	for taste in taste_scores:
		taste_scores[taste] = taste_scores[taste] * cuisine_multipliers[taste]
	return taste_scores


def get_cuisine_multipliers(tags):
	with open('cuisine_multipliers.json') as json_file:
		cuisine_multipliers = json.load(json_file)
	default =  {
		"salt":1.0,
		"sweet":1.0,
		"rich":1.0
		}
	if tags is not None:
		if len(tags) == 0:
			return default
		if len(tags) == 1:
			return cuisine_multipliers[tags[0]]
		elif len(tags) == 2:
			return cuisine_multipliers[tags[0]][tags[1]]
	else:
		return default


def get_cuisine_tags(food):
	with open('first_50_tags.json') as json_file:
		tags = json.load(json_file)
	closest_match = utilities.modmatchi(food['dish_name'], list(tags), threshold=0.5)
	if closest_match[0] is not None:
		return tags[closest_match[0]]


def main():
	foods_list = get_dishes()
	max_taste = ['', 0]
	for food in foods_list:
		#if food['dish_id'] == 39:
		#print(food['dish_name'])
		profile = taste(food)
		print(food['dish_name'],profile)
			#if profile['salt'] > max_taste[1]:
			#	max_taste = [food['dish_name'],profile['salt']]
	print(max_taste)


if __name__ == '__main__':
	# main()
	parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
	parser.add_argument("-f", "--file", help="Load the dish from the file specified", action='append')
	parser.add_argument("-p", "--profile", help="Profiles the JSON", action='append')
	arguments = parser.parse_args()

	if arguments.file:
		for file in arguments.file:
			with open(file) as inputfile:
				print(json.dumps(taste(json.load(inputfile)), sort_keys=True))