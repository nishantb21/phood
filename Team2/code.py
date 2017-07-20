import json
import collections
import os
import re
import requests
import pickle
import copy
import logging
import sys
import ast

import cleaning
import write_files
import findleaves
import call_api
import GetLogs
import toPlot
import tasteProfile

def printuserscore():
	userscore = json.load(open("userscore.json"))
	for i in sorted(userscore):
		for j in sorted(userscore[i]):
			print(j, i.upper(), end = " - ")
			for k in sorted(userscore[i][j]):
				print(k, userscore[i][j][k], sep = " : ", end = "; ")
			print("\n")
		print("")

def add_to_hier(tags):
	handle = open("h.json")
	hierarchy = json.load(handle)
	hier = hierarchy[0]

	newly_added = []
	for i in range(len(tags) - 1, -1, -1):
		if tags[i] in hier:
			hier = hier[tags[i]][0]

		else:
			hier[tags[i]] = [{}]
			newly_added.append(tags[i])
			hier = hier[tags[i]][0]

	handle.close()
	write_files.write_json(hierarchy, "h.json")

	for item in newly_added:
		write_files.log_data(item + " added to the tag hierarchy", "infoLogFile.txt")

def add_to_database(key, tags):
	spaces = key.count(' ')

	if(len(key) < 5 and spaces == 0):
		file_name = "data2.pickle"
	else:
		file_name = "data1.pickle"
	
	write_files.write_to_dict(key, tags, file_name)

def add_shared_parent(key, value):
	write_files.write_dict_json(key, value, "sharedparents.json")

def check_nonveg(key, tags):
	vegnonveg_file = open("vegnonveg.pickle", "rb")
	vegnonveg = pickle.load(vegnonveg_file)

	for i in tags:
		if i in vegnonveg:
			if key not in vegnonveg:
				vegnonveg.append(key)

	vegnonveg_file.close()
	write_files.write_to_list(vegnonveg, "vegnonveg.pickle")

def tag_dish(dish, ingredients = "", restaurant = ""):
	cui = []
	tag = []
	veg = 1
	size = None

	negations = {"without", "instead", "monkey"}
	free = {"free"}

	dishLower = dish.lower()
	print('falafel' in dishLower)

	ingredientsLower = ingredients.lower()

	dl = re.split(',| ',dishLower)
	il = re.split(',| ',ingredientsLower)
	dl = list(map(str.strip, dl))
	il = list(map(str.strip, il))

	data1_file = open("data1.pickle", "rb")
	data2_file = open("data2.pickle", "rb")
	data1 = pickle.load(data1_file)
	data2 = pickle.load(data2_file)

	cuisine_file = open("cuisine.pickle", "rb")
	cuisine = pickle.load(cuisine_file)

	nonveg_list_file = open("vegnonveg.pickle", "rb")
	nonveg_list = pickle.load(nonveg_list_file)

	sizes_file = open("size.pickle", "rb")
	sizes = pickle.load(sizes_file)

	### tags ###

	for i in data1:
		if i in dishLower:
			tag.extend(data1[i])

		if i in ingredientsLower:
			tag.extend(data1[i])

	for i in data2:
		if i in dl:
			tag.extend(data2[i])

		if i in il:
			tag.extend(data2[i])

	for i in negations:
		if i in dl:
			nx = dl.index(i) + 1
			if nx < len(dl):
				next = dl[nx]
				if next in data1:
					tag = list(set(tag) - set(data1[next]))
				if next in data2:
					tag = list(set(tag) - set(data2[next]))

	for i in free:
		dl = re.split(',| ',dishLower)
		if i in dl:
			next = dl[dl.index(i) - 1]
			if next in data1:
				tag = list(set(tag) - set(data1[next]))

			if next in data2:
				tag = list(set(tag) - set(data2[next]))

	tag = set(tag)
	
	### cuisine ###

	for i in cuisine:
		if i in dishLower:
			cui.append(cuisine[i])

	for i in tag:
		if i in cuisine:
			cui.append(cuisine[i])

	cui = set(cui)

	### veg - NonVeg ###

	for i in nonveg_list:
		if i in tag:
			veg = 0
			break

		if i in ingredientsLower:
			veg = 0
			break

	### size ###

	for i in sizes:
		if i in dl:
			size = sizes[i]

	data1_file.close()
	data2_file.close()
	cuisine_file.close()
	nonveg_list_file.close()
	sizes_file.close()

	return (list(tag), list(cui), veg, size)

def tagging_dish(term, ingredients = ""):
	returned_data = tag_dish(term, ingredients)
	tags = returned_data[0]
	cuisine = returned_data[1]

	# call api code
	if(len(tags)) == 0:
		api_tags = call_api.call_api_tags(term)
		if api_tags is not None:
			if(len(api_tags) == 0):
				message = term + " unamrked by API"
				write_files.log_data(message, "infoLogFile.txt")
				write_files.write_api_miss(term, "API_miss.txt")

			else:
				cleaned_tags = cleaning.clean_and_path_to_hier(term, api_tags)
				tags = cleaned_tags[2]
				add_to_database(cleaned_tags[1], cleaned_tags[2])
				add_to_hier(cleaned_tags[3])
				if len(cleaned_tags[4]) != 0:
					for i in cleaned_tags[4]:
						for j in i:
							add_shared_parent(j, cleaned_tags[1])
	return (tags, cuisine)

def score(dish, userID = "", factor = 1 ,type = 0):
	# print(dish, userID)
	userscore = json.load(open("userscore.json"))

	# metatags
	if type == 0:
		data = json.load(open("h.json"))
		returned_data = findleaves.find_node(dish, data[0])
		if returned_data is not None:
			leaves_in = returned_data[3][0]
			leaves = findleaves.find_leaves(returned_data[2], {returned_data[2] : leaves_in})
			shared_parent_count = findleaves.shared_parents(returned_data[2])
			total_leaves = leaves + shared_parent_count
			if "tags" in userscore:
				if userID in userscore["tags"]:
					find_in = userscore["tags"][userID]
					if dish in find_in:
						increase_for = find_in[dish]
						updated_value = increase_for + (factor / total_leaves)
						find_in[dish] = round(updated_value, 3)
					else:
						find_in[dish] = round((factor / total_leaves), 3)

				else:
					newvalues = {}
					newvalues[dish] = round((factor / total_leaves), 3)
					userscore["tags"][userID] = newvalues
			else:
				newvalues = {}
				newvalues[dish] = round((factor / total_leaves), 3)
				userscore["tags"] = {userID : newvalues}

	# cuisine
	else:
		data = json.load(open("cuisine_hierarchy.json"))
		returned_data = findleaves.find_cuisine_node(dish, data[0])
		if returned_data is not None:
			if "cuisine" in userscore:
				if userID in userscore["cuisine"]:
					find_in = userscore["cuisine"][userID]
					if dish in find_in:
						increase_for = find_in[dish]
						updated_value = increase_for + (factor / returned_data)
						find_in[dish] = round(updated_value, 3)
					else:
						find_in[dish] = round((factor / returned_data), 3)

				else:
					newvalues = {}
					newvalues[dish] = round((factor / returned_data), 3)
					userscore["cuisine"][userID] = newvalues

			else:
				newvalues = {}
				newvalues[dish] = round((factor / returned_data), 3)
				userscore["cuisine"] = {userID : newvalues}

	open("lastedit.txt", "w+").write(userID)
	write_files.write_json(userscore, "userscore.json")

def tag_score_user(log, factor):
	if factor == 1:
		search_term_in = log["resource"]
		if search_term_in.startswith("search/restaurant/location"):
			if 'keyword' in search_term_in:
				start = search_term_in.index('keyword') + len('keyword') + 1
				tempString = search_term_in[start:]
				if '&' in tempString:
					search_term = search_term_in[start:start + tempString.index('&')]
				else:
					search_term = search_term_in[start : ]

				search_term = search_term.replace("+", " ")
				returned_tags = tagging_dish(search_term.lower())

				# meta tags for dishes
				if len(returned_tags[0]) != 0:
					for i in returned_tags[0]:
						score(i,log["userId"], factor)

				# cuisine tags for dishes
				if len(returned_tags[1]) != 0:
					for i in returned_tags[1]:
						score(i, log["userId"], factor, 1)
				
		
		if search_term_in.startswith("search/location/"):
			if '?' in search_term_in:
				search_term = search_term_in[len("search/location/") : search_term_in.index('?')]
			else:
				search_term = search_term_in[len("search/location/"):]
			
			returned_tags = tagging_dish(search_term.lower())

			# meta tags for dishes
			if len(returned_tags[0]) != 0:
				for i in returned_tags[0]:
					score(i, log["userId"], factor)

			# cuisine tags for dishes
			if len(returned_tags[1]) != 0:
				for i in returned_tags[1]:
					score(i, log["userId"], factor, 1)

	elif factor == 2:
		used += 1
		search_term = log["dishName"]
		returned_tags = tagging_dish(search_term.lower())

		# meta tags for dishes
		if len(returned_tags[0]) != 0:
			for i in returned_tags[0]:
				score(i,log["userId"], factor)

		# cuisine tags for dishes
			if len(returned_tags[1]) != 0:
				for i in returned_tags[1]:
					score(i, log["userId"], factor, 1)

	elif factor == 3:
		pass
		# TODO when purchases are made

def from_server():
	# GetLogs.get_new_log()

	userscore = json.load(open("userscore.json"))
	oldscore = copy.deepcopy(userscore)
	json.dump(oldscore, open("oldscore.json", "w+"), indent = 4)
	overrideDict = {}
	if "tags" in userscore:
		overrideDict["tags"] = {}
		if "dummyUser" in userscore["tags"]:
			overrideDict["tags"]["dummyUser"] = userscore["tags"]["dummyUser"]

	if "cuisine" in userscore:
		overrideDict["cuisine"] = {}
		if "dummyUser" in userscore["cuisine"]:
			overrideDict["cuisine"]["dummyUser"] = userscore["cuisine"]["dummyUser"]

	json.dump(overrideDict, open("userscore.json", "w+"))

	logs = json.load((open("logs.json")))
	for i in range(len(logs)):
		j = i + 1
		for log_item in logs[i]:
			tag_score_user(log_item, j)

	# printuserscore()

def in_flow(dish, ingredients = ""):
	userscore = json.load(open("userscore.json"))
	oldscore = copy.deepcopy(userscore)
	json.dump(oldscore, open("oldscore.json", "w+"), indent = 4)

	returned_tags = tagging_dish(dish, ingredients)
	print(returned_tags)
	# meta tags for dishes
	if len(returned_tags[0]) != 0:
		for i in returned_tags[0]:
			score(i, "dummyUser", 1)

	# cuisine tags for dishes
	if len(returned_tags[1]) != 0:
		for i in returned_tags[1]:
			score(i, "dummyUser", 1, 1)

	# printuserscore()

def main():
	x = len(sys.argv)
	if x <= 3:
		if x == 1:
			from_server()

		elif x == 2:
			in_flow(sys.argv[1])

		elif x == 3:
			in_flow(sys.argv[1], sys.argv[2])
	
		final_result = toPlot.makeDataToPlot(0)

	else:
		in_flow(sys.argv[1], sys.argv[2])
		tasteProfile.categoriseTaste(sys.argv[3])
		final_result = toPlot.makeDataToPlot(1)

	print(final_result)

main()