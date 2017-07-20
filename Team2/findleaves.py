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


# function find_node() is used to locate a node in the food tag hierarchy - h.json
# the function takes in the node being searched for, the dictionary in which the 
# node is to be looked for and the current depth. the function returns, the node
# being searched for, along with the depth at which it was found in the food tag
# hierarchy, the number of siblings and all children of the node found. If the node
# is not found, the function returns None.

def find_node(i, d, dep = 1):
	dep = dep + 1 

	# if node being looked for is found in the dictionary d, return the number of sibblings, the depth the node itself and children of the node
	if i in d: 
		return (len(d), dep, i, d[i])

	else:
		for j in d: # recursively look for all nodes in the dictionary d for the node 'i'
			if len(d[j]) != 0:
				x = find_node(i, d[j][0], dep)
				if x != None:
					return x

# function find_leaves returns a count of the number of leaves of the 
# node being passed as the first parameter of the function in dictionary d
def find_leaves(node, d):
	if len(d[node]) == 0: # if the node has no chidren it is the leaf, 1 leaf hence returned
		return 1

	else:
		x = 0 # variable to keep track of the leaves of all children of a node if it is not the leaf itself
		for i in d[node]: # loop through all children of the node
			x += find_leaves(i, {i : d[node][i][0]}) # add the number of leaves of child 'i' to x

		return x

# return the number of dish's of a particular cuisine
# function takes in the dish name and a cuisine hierarchy
# finds the cuisine for the dish name in hierarchy and returns 
# the number of dishes for that cuisine
def find_cuisine_node(i, d):
	for j in d:
		if i in d[j]:
			return len(d[j])

# function returns the number of shared parents for a particular dish
def shared_parents(find):
	data = json.load(open("sharedparents.json"))
	return_value = 0 
	if find in data:
		return_value = len(data[find])

	return return_value