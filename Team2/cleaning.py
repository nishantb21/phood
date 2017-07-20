'''
	Spoonacular API - called when a dish is 
	not found in the database - returns some
	unwanted tags (tags that don't help in 
	profiling a user), this file determines
	what tags associated with a dish returned
	by the API should be added to the databse. 
	This is done by comparing the metatags 
	returned by the API to the existing database, 
	relevant matches in the database are 
	associated with the dish or a 
	substring of the dish name.
'''

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


d_file = open("h.json") # the tag hierarchy is contained in file h.json

d = json.load(d_file)
d = d[0] # tag hierarchy loaded into variable d

d1 = open("data1.pickle", "rb") # loading database contained in file data1
d2 = open("data2.pickle", "rb") # loading database contained in file data2

data1 = pickle.load(d1) # loading database1 into variable data1
data2 = pickle.load(d2) # loading database2 into variable data2



# function to sanitise the tags returned by the API - takes in a dish name along with the associated tags and returns a list of possible tags

def clean(dish, tags):
	# set of metatags returned by the API that need to be removed
	to_remove = {"dinner", "lunch", "menu item type", "animal by-product", "starter", "main course", "side dish", "meal"}
	
	if dish.lower() != "menulinks":
		cleaned_tags = [] # The value returned by this function

		tags = list(map(str.lower, tags)) # convert tags to lower case
		
		'''
			An API returned tag may contain 
			multiple words, temp_tags holds
			each individual word in a 
			multiword tag - an individual
			word returned by the API may
			be contained in the datase, 
			helps extract more information
			from the existing database
		'''
		temp_tags = [] 

		for i in tags:
			for j in re.split(',| ', i):
				temp_tags.append(j)


		for i in tags:
			for j in data1:
				if j in i:
					if data1[j] not in cleaned_tags:
						# A list of lists, with each list containing tags in a hierarchical fashion, from leaf nodes to top leavel nodes
						cleaned_tags.append(data1[j])

		for i in temp_tags:
			x = len(i)
			for j in data2:
				# find as a substring items of data2 in the individual words of temp_tag, if so, associate tags of item in data2 with the dish

				if (j in i) and (abs(len(j) - x) <=2):
					if data2[j] not in cleaned_tags:
						cleaned_tags.append(data2[j])

		'''
			if no tags in the database match 
			the tags returned by the API, the
			API tags are itself used
		'''

		if len(cleaned_tags) == 0:
			# for i in tags:
			# 	x.append([i])
			cleaned_tags = [tags]

		# remove items listed in to_remove from the list of tags
		for i in to_remove:
			for j in cleaned_tags:
				if i in j:
					j.remove(i)

		# on removing items from the to remove list, if a list in cleaned_tags is empty, remove it
		cleaned_tags = [i for i in cleaned_tags if len(i) > 0]
		
		''' 
			reverse sort the cleaned tags based on length
			of the associated meta tag list, e.g if the 
			dish name is "chianti classico banfi" the tags
			after reverse sorting the lists in order of 
			length are - {[red wine, wine, alcohol, beverage],
			[alcohol, beverage], [beverage]}, here, 
			[red wine, wine, alcohol, beverage] has a length
			of four and is hence at the first postion in the
			cleaned_tags list. The tag list at the first
			position is hence assumed to be the most 
			appropriate for the dish, to which other tags are
			added if required.
		'''
		cleaned_tags = sorted(cleaned_tags, key = lambda x : len(x), reverse = True)

		d1.close() # closing file handlers
		d2.close()

		return cleaned_tags


# function to return the sanitized tags and appropriate key to be added to the database
def clean_and_path_to_hier(dish, tags):
		cleaned_tags = clean(dish, tags) # call function clean to get a list of possible cleaned tags

		final_tags = [] # list of tags to be finally added in the database
		path_in_hier = [] # the path in the hierarchy where the new dish is to be added
		shared_parents = [] # keep track of the list of shared parents for a dish if any, e.g 'milk' is shared between tags, beverage and dairy

		if len(cleaned_tags) != 0:
			final_tags = copy.deepcopy(cleaned_tags[0]) # longest length tag list from the set of cleaned tags, assumed to be the most appropriate (as explained in the previous function)
			path_in_hier = copy.deepcopy(cleaned_tags[0]) # the new dish is placed in the longest path in the hierarchy

			for i in range(1, len(cleaned_tags)):
				prev = 0
				consider = cleaned_tags[i]
				for j in range(len(consider)):
					if consider[j] not in final_tags and consider[j] in d:
						path = consider[prev : j + 1]
						shared_parents.append(path)
						final_tags.extend(path)

					elif consider[j] in d:
						prev = j + 1

		if len(final_tags) == 0:
			final_tags.append(key)
			path_in_hier = copy.deepcopy(final_tags)

		key = copy.deepcopy(tags[0])

		key_changed = 0

		if key not in dish.lower():
			key = copy.deepcopy(dish.lower())
			key_changed = 1

		# dish should go in data2
		if key_changed == 0:
			if key in dish.lower() and ' ' not in key and len(key) <= 4:
				spilt_list = re.split(',| ', dish.lower())
				for i in spilt_list:
					if key in i:
						key = i

		if key != final_tags[0]:
			final_tags.insert(0, dish.lower())
			path_in_hier.insert(0, dish.lower())

		d_file.close()
		return (dish.lower(), key ,final_tags, path_in_hier, shared_parents)

# To test this file individually uncomment the follwing block of code, add the dish name as the first parameter, and the associated tags returned by the API in the list
'''
print(clean_and_path_to_hier('dishNameHere', ['tag1', 'tag2', ...]))
'''