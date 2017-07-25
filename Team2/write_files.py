# Refer readme.md for brief information about each file.
# Refer files.md for detailed information about each file and functions used in each file.

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

# Takes an item which missed the API (term) and a file name as input parameters. Checks if the file contains the term and if it does not, appends it to that file.
def write_api_miss(term, file_name):
	term = term.lower()
	handle = open(file_name, "r")
	miss_list = list(map(str.strip, handle.readlines()))
	if term not in miss_list:
		handle = open(file_name, "a+")
		handle.write(term.lower() + "\n")

# Takes a json file along with key-value pair as input. Checks if the key already exists in the json file. If yes, its value is appended. Otherwise, itself is added as its value
def write_dict_json(key, value, file_name):
	data = json.load(open(file_name))
	if key in data:
		data[key].append(value)

	else:
		data[key] = [value]

	json.dump(data, open(file_name, "w+"))

# Input parameters are file name and data. This function adds the data into the file in json format with proper indentation.
def write_json(data, file_name):
	handle = open(file_name, "w+")
	json.dump(data ,handle, indent = 4)
	handle.close()

# Takes a file name along with a key-value pair as input. Creates a handler which is used to load the pickle file in a user readable format. Adds the key-value pair as a dictionary item into the file and dumps it in its original format (pickle file) . Generates logs for each update to the file.
def write_to_dict(key, tags, file_name):
	handle = open(file_name, "rb")
	data = pickle.load(handle)
	if key not in data:
		data[key] = tags

	handle.close()

	handle = open(file_name, "wb")
	pickle.dump(data, handle)
	handle.close()

	message = "adding key " + key + " with tags [" + ";".join(tags) + "] to file " + file_name
	log_data(message, "infoLogFile.txt")

# Takes a list as parameter along with a pickle file, as input. Creates a handler to open the pickle file in write mode and then adds the list to the file and dumps it back as pickle file.
def write_to_list(full_list, file_name):
	handle = open(file_name, "wb")
	pickle.dump(full_list, handle)
	handle.close()

# Inputs for this function are message and file name. Any append to the knowledge base, hierarchy, API miss, is logged into a separate file with the timestamp.
def log_data(message, file_name):
	logging.basicConfig(level=logging.INFO, filename = file_name,format = '%(asctime)s %(message)s')
	logging.info(message)