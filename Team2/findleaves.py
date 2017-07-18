import json
import collections
import os
import re
import requests
import pickle
import copy
import logging

# data = json.load(open("h.json"))
# data = json.load(open("cuisine_hierarchy.json"))

def find_node(i, d, dep = 1):
	dep = dep + 1

	if i in d:
		return (len(d), dep, i, d[i])

	else:
		for j in d:
			if len(d[j]) != 0:
				x = find_node(i, d[j][0], dep)
				if x != None:
					return x

def find_leaves(node, d):
	if len(d[node]) == 0:
		return 1

	else:
		x = 0
		for i in d[node]:
			x += find_leaves(i, {i : d[node][i][0]})

		return x

def find_cuisine_node(i, d):
	for j in d:
		if i in d[j]:
			return len(d[j])

def shared_parents(find):
	data = json.load(open("sharedparents.json"))
	return_value = 0 
	if find in data:
		return_value = len(data[find])

	return return_value

# returned_data = find_cuisine_node("pizza", data[0])
# leaves_in = returned_data[3][0]
# leaves = find_leaves(returned_data[2], {returned_data[2] : leaves_in})