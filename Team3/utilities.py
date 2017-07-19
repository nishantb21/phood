#utility
import hashlib
import sys
import json
import nltk
import re
import csv
from multiprocessing import Pool
import glob

def standardize_keys(nutrition_information):
	'''
	Standardize nutritional information
	Maps common nutrients to the standard format
	food_name: item_name
	serving_weight_grams:metric_qty
	nf_calories: calories
	nf_total_fat:total_fat
	nf_saturated_fat:saturated_fat
	nf_cholesterol: cholesterol
	nf_sodium:sodium
	nf_total_carbohydrates:total_carb
	nf_dietary_fiber:dietary_fiber
	nf_sugars:sugars
	nf_protein:protein
	'''
	#try: 
	if nutrition_information.__contains__('metric_qty'):
		nutrition_information['iron'] = nutrition_information['iron_dv'] if nutrition_information['iron_dv'] is not None else 0
		return nutrition_information #Key exists, is already in standard format
	full_nutrient_keys = {"iron": 13, "vitamin_c": 40}
	#except KeyError: #Common format, standardize
	standard_keys = ["food_name", "serving_weight_grams", "nf_calories", "nf_total_fat", "nf_saturated_fat", "nf_cholesterol", "nf_sodium", "nf_total_carbohydrate", "nf_dietary_fiber", "nf_sugars", "nf_protein"]
	common_keys = ["item_name", "metric_qty", "calories", "total_fat", "saturated_fat", "cholesterol", "sodium", "total_carb", "dietary_fiber", "sugars", "protein"]
	mappings = zip(standard_keys, common_keys)
	new_nutrition_information = dict()
	for mapping in mappings:
		new_nutrition_information[mapping[1]] = nutrition_information[mapping[0]]	
	for item in full_nutrient_keys.items():
		try:
			new_nutrition_information[item[0]] = nutrition_information['full_nutrients'][item[1]]["value"]
		except IndexError as ie:
			new_nutrition_information[item[0]] = 0.0
	return new_nutrition_information

def read_csv(csv_file):
	with open(csv_file) as cf:
		reader = csv.reader(cf,delimiter=',')
		next(reader)
		txt_file = open('food_names.txt','w')
		for row in reader:
			name = row[0].strip()
			txt_file.write(name+'\n')
			item_dict = dict()
			item_dict['name'] = name
			item_dict['ingredients'] = eval(row[15].strip())
			name_hash = hash(name)
			print('\r', name.lower(), end='\r')
			with open('hashed_foods/'+name_hash+'.json', 'w') as dish_file:
				json.dump(item_dict,dish_file,indent='\t')
	txt_file.close()

def parameterize(qstring):
		return qstring.strip('\n').replace(' ', '+')

def modmatchir(query_string, nriterable, threshold):
	if len(nriterable) == 0:
		return None
	best_match = (None, -1)
	best_match_index = 0
	current_index = -1
	for word in nriterable:
		result = modmatch(query_string, word.name, threshold)
		current_index += 1
		#best_match = result if result is not None and result[1] > best_match[1] else best_match
		if result is not None and result[1] > best_match[1]:
			best_match_index = current_index
			best_match = result
	#print('\r', best_match_index, len(nriterable), end='\r')
	return nriterable[best_match_index]

def modmatchi(query_string, iterable, threshold):
	best_match = (None, -1)
	for word in iterable:
		result = modmatch(query_string, word, threshold)
		best_match = result if result is not None and result[1] > best_match[1] else best_match
	return best_match

def modmatch(query_string, match_string, threshold):
	match_string = re.sub(',','',match_string)
	query_string = re.sub(',','',query_string)
	
	match_string_split = match_string.strip().upper().split(' ')
	query_string_split = query_string.strip().upper().split(' ')
	matched = [word for word in query_string_split if word in match_string_split]
	if len(matched) > 0 or (' ' not in match_string and query_string.upper().strip() in match_string.upper().strip()):
		if len(matched) / len(query_string_split) >= threshold:
			return (match_string, round(len(matched) / len(query_string_split),2))
	return None

def hash(input_title):
	return hashlib.md5(input_title.strip().strip('\n').upper().encode('utf-8')).hexdigest()

def package(input_file):
	contents = dict()
	with open(input_file) as ifile:
		for line in ifile:
			if not contents.__contains__(line[0]):
				contents[line[0]] = set()
			contents[line[0]].add(line.strip('\n'))
			
	for key in contents.keys():
		contents[key] = list(contents[key])
	with open(input_file.split('.')[0] + '.json', 'w') as writer:
		json.dump(contents, writer, indent='\t')

def standardize(input_file):
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
	nutrition_scrubbed = dict()

	with open('nutritionix_data/' + input_file) as json_file, open('nutritionix_data/' + input_file + '_std', 'w') as json_standardized:
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
		return json_standardized.name

def ratio(i_no = 1):
	fractal = round(100/i_no, 4)
	perc_list = list()
	for index in range(i_no):
		perc_list.append(fractal)

	for rrange in range(1, i_no):
		steal = round(((rrange/i_no)*fractal)/2, 4)
		perc_list[rrange] -= steal
		perc_list[0] += steal
	return perc_list

def standardize_files(file):
	nutri = dict()
	with open(file) as raw_file:
		nutri = json.load(raw_file)
	with open("fin/" + file.split("/")[-1], 'w') as stdfile:
		json.dump(standardize_keys(nutri), stdfile, indent='\t')
		print('\r', file, end='')

def read_json(file):
	with open(file) as f:
		return json.load(f)

if __name__ == '__main__':
	#for folder
	with Pool(17) as ppool:
		ppool.map(standardize_files, glob.iglob(sys.argv[1] + "/*.json"))