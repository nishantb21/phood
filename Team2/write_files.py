import json
import collections
import os
import re
import requests
import pickle
import copy
import logging

def write_api_miss(term, file_name):
	term = term.lower()
	handle = open(file_name, "r")
	miss_list = list(map(str.strip, handle.readlines()))
	if term not in miss_list:
		handle = open(file_name, "a+")
		handle.write(term.lower() + "\n")

def write_dict_json(key, value, file_name):
	data = json.load(open(file_name))
	if key in data:
		data[key].append(value)

	else:
		data[key] = [value]

	json.dump(data, open(file_name, "w+"))

def write_json(data, file_name):
	handle = open(file_name, "w+")
	json.dump(data ,handle, indent = 4)
	handle.close()

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

def write_to_list(full_list, file_name):
	handle = open(file_name, "wb")
	pickle.dump(full_list, handle)
	handle.close()

def log_data(message, file_name):
	logging.basicConfig(level=logging.INFO, filename = file_name,format = '%(asctime)s %(message)s')
	logging.info(message)