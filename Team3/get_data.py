import json
import datak
import utilities
import os

SWEET_FACTOR_X = 0.9
SWEET_FACTOR_Y = 0.1

RICHNESS_FACTOR_X = 0.5
RICHNESS_FACTOR_Y = 0.7
RICHNESS_FACTOR_Z = 50

SOURNESS_FACTOR_X = 0.1
SOURNESS_FACTOR_Y = 0.25
SOURNESS_FACTOR_Z = 0.5

BITTERNESS_FACTOR_X = 1
BITTERNESS_FACTOR_Y = 1

def normalize(nutrition_data,weight):
	for key in nutrition_data.keys():
		try:
			nutrition_data[key] = 100 * (nutrition_data[key] / weight)
		except TypeError:
			pass
	return nutrition_data


def get_nutrition_data(dish_title):
	dish_title = dish_title.upper()
	dish_title_hash = utilities.hash(dish_title)
	if(os.path.exists('branded_dishes/' + dish_title_hash + '.json')):
		#print("offline")
		with open('branded_dishes/' + dish_title_hash + '.json') as food_file:
			food_data = json.load(food_file)
		return food_data
	else:
		#print("online")
		return(datak.ingredient(dish_title).nutrition_data)

def sweet(nutrition_data, SWEET_FACTOR_X=0.85, SWEET_FACTOR_Y=0.1):
	try:
		total_weight = nutrition_data['metric_qty']
		sweet_score_x1 = abs(nutrition_data['sugars'] - nutrition_data['dietary_fiber']) / total_weight
		sweet_score_y = nutrition_data['sugars'] / nutrition_data['total_carb'] 
		sweet_score_1 = (SWEET_FACTOR_X * sweet_score_x1) + (SWEET_FACTOR_Y * sweet_score_y)
		#	print(sweet_score_1)
	except Exception as e:
		sweet_score_1 = 0
	return round(sweet_score_1 / 0.998,3)

def rich(nutrition_data, RICHNESS_FACTOR_X=0.5, RICHNESS_FACTOR_Y=0.7,RICHNESS_FACTOR_Z=50):
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

	return round((richness_score_1 / 0.992),3)
	## Normalize to butter which has highest score

def sour(dish_title, nutrition_data, SOURNESS_FACTOR_X=0.1, SOURNESS_FACTOR_Y=0.25, SOURNESS_FACTOR_Z=0.5):
	total_weight = nutrition_data['total_carb'] + nutrition_data['protein'] + nutrition_data['total_fat']
	food_words = dish_title.upper().split(' ')
	#print(food_words)
	try:
		vitamin_c = nutrition_data['vitamin_c']
	except KeyError as ke:
		vitamin_c = 0.0
	print(vitamin_c)
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
	return sour_score 

def spicy(dish_title):
	food_words = dish_title.upper().split(' ')
	with open('spicy.json') as f:
		spice = json.load(f)
	for word in food_words:
		if word in spice[word[0]]:
			return True
	return False

def profile_taste(dish_title):
	nutrition_data = get_nutrition_data(dish_title)
	for key in nutrition_data.keys():
		if not nutrition_data[key]:
			nutrition_data[key] = 0.0
	print(nutrition_data)
	total_weight_1 = nutrition_data['metric_qty']

		#print(key, nutrition_data[key])
	#print("2",sweet_score_2)
	sweet_score = sweet(nutrition_data, SWEET_FACTOR_X, SWEET_FACTOR_Y)
	richness_score = rich(nutrition_data, RICHNESS_FACTOR_X, RICHNESS_FACTOR_Y, RICHNESS_FACTOR_Z)
	#salt_score = salt(nutrition_data, total_weight_2)
	sour_score = sour(dish_title, nutrition_data, SOURNESS_FACTOR_X, SOURNESS_FACTOR_Y, SOURNESS_FACTOR_Z)
	print(nutrition_data['item_name'],sweet_score,richness_score,sour_score)
	#print("\nName",nutrition_data['item_name'])
	#print("Sweet",sweet_score)
	#print("Salty1", salt_score)
	#print("Richness", richness_score_1)
	#print("Salty2", salt_score_2)

foods = ['hot and sour soup','sour patch kids','pickle','iced tea','lime','lime juice','lemonade','lemon','orange juice','hamburger','vinegar','margarine','lard','butter','orange','potato chips','salt','casein','kielbasa','salted jellyfish','whey protein','sugar','oil','big fish sandwich','chicken salad','cheeseburger','oreos','chocolate chip cookie','gobstopper','caramel fudge','french fries','bread','coffee','tofu']
for food in foods:
	#print(food)
	try:
		profile_taste(food.upper())
	except AttributeError as ae:
		pass
	print()