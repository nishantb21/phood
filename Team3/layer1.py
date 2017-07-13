import csv
import glob
import utilities
import pickle
import os
import nltk
import json
import datak
import sys
import kb

SEARCH_THRESHOLD = 0.3
foodDict = dict()
ps = nltk.PorterStemmer()
rejector = kb.Rejector('food_rejects.json')

def init_food_dict(foodItems):
	foodDict = dict()
	##print(type(foodsList))
	##print(foodItems.keys())
	if(isinstance(foodItems,dict)):
		for key in foodItems.keys(): 
			for food in foodItems[key]:
				foodDict[food] = dict()
				foodDict[food]['sweet'] = 0.0
				foodDict[food]['fat'] = 0.0
				foodDict[food]['salt'] = 0.0
				foodDict[food]['count'] = 0
				foodDict[food]['matches'] = list()
				foodDict[food]['ings'] = list()
	##print(foodDict.keys())
	return foodDict

def genRows(csvFile):
	#Pickle dump the rows file maybe
	#If timestamp modified, reload, else load pickle
	rows = dict()
	lines = 0
	a_time = 0
	m_time = 0
	with open('Layer1/'+csvFile+'.csv') as csv_file:
		lines = sum(1 for _ in csv_file)
		a_time = os.path.getatime(csv_file.name)
		m_time = os.path.getmtime(csv_file.name)

	#print("Generating Rows List...")
	'''
	if(m_time < a_time):
		with open('Layer1/'+csvFile+'.csv') as csv_file:
			reader = csv.reader(csv_file,delimiter=',')
			next(reader)
			for row in reader:
				name = rejector.process(row[0].strip())
				rows[name] = dict()
				rows[name]['sweet'] = row[4].strip()
				rows[name]['salt'] = row[5].strip()
				rows[name]['richness'] = row[6].strip()
				rows[name]['ings'] = eval(row[15].strip())
			with open('Layer1/generatedRows','wb') as rowsFile:
				pickle.dump(rows,rowsFile)
			return rows
	else:
	'''
	with open('Layer1/generatedRows','rb') as rowsFile:
		#print("\nDone.")
		return pickle.load(rowsFile)

	#return [rows[0]]

def getFoods(foodFile):
	#Clean via nutritionix
	foodsList = []
	#print("Reading Food File...")
	with open('Layer1/'+foodFile +'.json') as foods:
		foodItems = json.loads(foods.read())
		return foodItems

def query_JSON(foodItem):
	#1 - Check the json file for a match, if found, then return the food
	with open('Layer1/scores2.json') as scoreFile:
		scores = json.loads(scoreFile.read())
		try:
			if scores[foodItem]:
				scores[foodItem]['ings'].extend(checkIngredient(foodItem))
				scores[foodItem]['salt'] /= scores[foodItem]['count']
				#print(scores[foodItem]['salt'])
				#print("matched here")
				return scores[foodItem]
		except KeyError as ke:
			for food in scores.keys():
				if utilities.modmatch2(foodItem, food, SEARCH_THRESHOLD):
					result = utilities.modmatch2(foodItem, food, SEARCH_THRESHOLD)
					#print(scores[food])
					scores[food]['salt'] /= scores[food]['count']
					scores[food]['ings'].extend(checkIngredient(foodItem))
					scores[food]['src'] = 'json'
					#print("ke, matchee here")
					return scores[food]
		return None

def query_USDA(foodItem):
	#2 - If the food doesn't match, add it to the foods.json, and run assignScore, and append it
	with open('Layer1/foods.json','r+') as foodsFile:
		data = json.loads(foodsFile.read())
		data[foodItem[0]] = foodItem
		data["name"] = foodItem
		return find_score(foodItem=foodItem)
	return None

def query_nutritionix(foodItem):
	#3 - Query nutritionix to get nutritional info, but return an empty list for ingredients, and append it to the existing file
	#print("Not found in USDA, querying Nutritionix")
	nutri_info = dict()
	query_result = datak.ingredient(foodItem)
	if query_result:
		food_weight = query_result['serving_weight_grams']
		#nutri_info["name"] = foodItem
		nutri_info[foodItem] = dict()
		#print(query_result)
		nutri_info[foodItem]['sweet'] = (query_result['nf_sugars'] / food_weight) if query_result['nf_sugars'] else 0
		nutri_info[foodItem]['salt'] = (query_result['nf_sodium'] / 39333) if query_result['nf_sodium'] else 0
		nutri_info[foodItem]['fat'] = (query_result['nf_total_fat'] / food_weight) if query_result['nf_total_fat'] else 0
		nutri_info[foodItem]['count'] = 1
		nutri_info[foodItem]['ings'] = checkIngredient(foodItem)
		nutri_info[foodItem]['src'] = 'nutritionix'
		return nutri_info
	return None

def return_score(foodItem):	
	foodItem = rejector.process(foodItem).upper()
	#Make sure it runs faster
	#print(foodItem)
	score = query_JSON(foodItem)
	if score:
		return score 
	#print("Querying USDA")
	score = query_USDA(foodItem)
	if score:
		return score
	score = query_nutritionix(foodItem)
	if score:
		return score
	else:
		#print("\nNot found anywhere, please consult your local chef")
		return None

def loadIngredientFile():
	with open('condensed_file.json') as f2:
		data = json.loads(f2.read())
		return data

foodItems = getFoods('foods')
ingredientItems = loadIngredientFile()
rows = genRows('tasteScores - Copy')

def checkIngredient(food):
	ingredients_in_name = list()
	food_split = list(set(food.split(' ')))
	food_split = [ps.stem(word).upper() for word in food_split]
	for food in food_split:
		if food and food in foodItems[food[0]]:
			food_split.remove(food)
	##print(food_split)
	for food in food_split:
		if food and food in ingredientItems[food[0]]:
			ingredients_in_name.append(food)
	return ingredients_in_name

def find_score(foodItem, rows=rows, testsize=len(rows)):

	foodDict = init_food_dict(foodItems)
	itemDict = {foodItem[0]:[foodItem]}
	##print(itemDict)
	foodDict.update(init_food_dict(itemDict))
	#print("Not Found, checking USDA")
	ingredients_in_name = checkIngredient(foodItem)
	for row in rows.keys():
		##print(row.split(' '))
		first_letters = set([i[0] for i in row.split(' ') if i and i[0] is foodItem[0]])
		#except Exception as e:
		#	#print(str(e) + ' ' + rows[row][0])
		search_space = create_search_space(first_letters, itemDict) #[foods[i] for i in first_letters if i in foods.keys()]
		##print(search_space)
		##print(first_letters)
		result = utilities.modmatchi2(row,search_space,SEARCH_THRESHOLD)
		##print(first_letters)
		##print(search_space)		
			#ofile.write(name + " " + str(result)+ "\n")
		if result[0] is not None:
			##print(result[0])
			##print(foodDict)
			foodDict[result[0]]['sweet'] += float(rows[row]['sweet'])
			foodDict[result[0]]['fat'] += float(rows[row]['richness'])
			foodDict[result[0]]['salt'] += float(rows[row]['salt'])
			foodDict[result[0]]['count'] += 1
			foodDict[result[0]]['matches'].append(row)
			if foodDict[result[0]]['ings'] == []:
				##print("Not found, creating")
				foodDict[result[0]]['ings'] = rows[row]['ings']
			else:
				##print("Found, adding to")
				foodDict[result[0]]['ings'] = set(foodDict[result[0]]['ings']).difference(set(rows[row]['ings']))
				##print(foodDict[result[0]]['ings'])
			##print(row+ ' ' + str(foodDict[result[0]]['ings']))
		#else:
			##print(rows[row][0])
			##print(result)
	#			with open(foodsFile.name,'a+') as foodsFile:
	#				foodsFile.write(rows[row][0]+'\n')
	#print("Populated.\nAssigning Scores and writing...")
	keys = list(foodDict.keys())
	index = keys.index(foodItem)
	food = keys[index]
	#print(food)
	if foodDict[food]['count'] > 0 :
		with open('Layer1/scores2.json') as f:
			data = json.loads(f.read())
		with open('Layer1/scores2.json', 'w+') as f:
			data[food] = dict()
			data[food]["name"] = food
			data[food]['sweet'] = foodDict[food]['sweet'] / foodDict[food]['count']
			data[food]['fat'] = foodDict[food]['fat'] / foodDict[food]['count']
			data[food]['ings'] = list(foodDict[food]['ings'])
			data[food]['ings'].extend(ingredients_in_name)
			data[food]['salt'] = foodDict[food]['salt'] / foodDict[food]['count']
			data[food]['count'] = foodDict[food]['count']
			data[food]['src'] = 'usda'
			##print(ingredients_in_name)
			json.dump(data,f,indent='\t')

		return foodDict
	else:
		#foodDict.pop(food)
		return None
		##print(type(foodDict[food]['ings']))
	#print("\nDone.")
	#print("Done.")
	if foodDict == {}:
		return None

def create_search_space(first_letters,food_items):
	search_space = []
	for i in first_letters:
		if i in food_items.keys():
			search_space.extend(food_items[i])
	return search_space

def assign_score(rows=rows, foodItems = foodItems):
	foodDict = init_food_dict(foodItems)
	##print(foodDict.keys())
	#print("Populating Dictionary...")
	for row in rows.keys():
		first_letters = set([i[0] for i in row.split(' ') if i and i[0] in foodItems.keys()])
		search_space = create_search_space(first_letters,foodItems)
		result = utilities.modmatchi2(row,search_space,SEARCH_THRESHOLD)
		if result[0] is not None:
			#ofile.write(name + " " + str(result)+ "\n")
			try:
				foodDict[result[0]]['sweet'] += float(rows[row]['sweet'])
				foodDict[result[0]]['fat'] += float(rows[row]['richness'])
				foodDict[result[0]]['salt'] += float(rows[row]['salt'])
				foodDict[result[0]]['count'] += 1
				foodDict[result[0]]['matches'].append(row)
			except Exception as e:
				pass
				##print(foodDict)
				#print(str(e) + ' ' + str(result))
			if foodDict[result[0]]['ings'] == []:
				##print("Not found, creating")
				foodDict[result[0]]['ings'] = rows[row]['ings']
			else:
				foodDict[result[0]]['ings'] = set(foodDict[result[0]]['ings']).difference(set(rows[row]['ings']))
			##print(row + ' ' + str(foodDict[result[0]]['ings']))
		#else:
			##print(rows[row][0])
			##print(result)
			#	with open(foodsFile.name,'a+') as foodsFile:
			#		foodsFile.write(rows[row][0]+'\n')
		#except Exception as e:
		#	#print(str(e) + ' ' + rows[row][0])
		
		##print(first_letters)
		##print(search_space)		
	#print("Populated.\nAssigning Scores and writing...")
	for food in list(foodDict):
		if foodDict[food]['count'] > 0  :
			foodDict[food]['sweet'] /= foodDict[food]['count']
			foodDict[food]['fat'] /= foodDict[food]['count']
			foodDict[food]['salt'] /= foodDict[food]['count']
			foodDict[food]['ings'] = list(foodDict[food]['ings'])
		else:
			del foodDict[food]
		#prin	t(type(foodDict[food]['ings']))
	#print("\nDone.")
	#print("Writing to file...")
	with open('Layer1/scores2.json', 'a+') as f:
		json.dump(foodDict,f,indent='\t')
	#print("Done.")
	return foodDict

def main():
	#print("Reassign Scores?")
	if input() == 'Y':
		assign_score()

	#print("Enter Food Name: ")
	print(return_score(input()))

if __name__ == "__main__":
	main()	