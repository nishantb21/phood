#utility
import hashlib
import sys
import json
import nltk

def parameterize(qstring):
		return qstring.strip('\n').replace(' ', '+')
		
def modmatchi(query_string, iterable, threshold):
	best_match = (None, -1)
	for word in iterable:
		result = modmatch(query_string, word, threshold)
		best_match = result if result[1] > best_match[1] else best_match
	return best_match

def modmatch(query_string, match_string, threshold):
	match_string_split = match_string.strip().upper().split(' ')
	query_string_split = query_string.strip().upper().split(' ')
	matched = [word for word in query_string_split if word in match_string_split]
	if len(matched) > 0 or (' ' not in match_string and query_string.upper().strip() in match_string.upper().strip()):
		if len(matched) / len(query_string_split) >= threshold:
			return (query_string, round(len(matched) / len(query_string_split)), 2)
	return None

def modmatchi2(query_string, iterable, threshold):
	best_match = (None, None, -1)
	for word in iterable:
		result = modmatch2(query_string, word, threshold)
		best_match = result if (result) and (result[2] > best_match[2]) else best_match
	return best_match

def modmatch2(query_string, match_string, threshold):
	if match_string == query_string:
		return (match_string, query_string, 1)
	ps = nltk.PorterStemmer()
	match_string_split = set([ps.stem(word) for word in match_string.strip().upper().replace(',',' ').split(' ')])
	query_string_split = set([ps.stem(word) for word in query_string.strip().upper().replace(',',' ').split(' ')])
	match_string_split = list(filter(lambda x: x,match_string_split))
	query_string_split = list(filter(lambda x: x,query_string_split))
	if len(query_string_split) == 2:
		threshold = 0.5
	if len(query_string_split) == 3:
		threshold = 0.66
	matched = [word for word in query_string_split if word in match_string_split]
	if len(matched) > 0 or (' ' not in match_string and query_string.upper().strip().replace(',',' ') in match_string.upper().strip().replace(',',' ')):
		if len(matched) / len(query_string_split) >= threshold:
			return (match_string, query_string, round(len(matched) / len(query_string_split), 2))
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
if __name__ == '__main__':
	package(sys.argv[1])