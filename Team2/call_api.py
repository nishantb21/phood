'''
	Call Spoonacular API if the dish is not found in the database,
	6 API keys made with 50 free calls per day from each key.
	DO NOT CROSS CALL LIMIT, check calls made on a day in file
	api_call_count.txt
'''

import json
import collections
import os
import re
import requests
import pickle
import copy
import logging

import write_files

# list of all API keys
# api_keys = ["BxIhdO07nbmshbjwe9tVirbI7DCip1BQPiGjsnmmjhdyUFtnVp", "208chbJvInmshPKp7BOAykKRmPZgp1s2LSajsnqYx4qGrmgC1U", "OhL8bc1jEmmshOJ4iVuGYCcJg8FLp1g2WIjjsnlWuYQp0ujiPF", "0Y9Zg0SAyvmshUaKiBdIf3czFN3Bp1mKtlVjsnjZHZB6FbB8h0", "7JTdJTOMygmshkjAxSgkxUViVmlWp1ZqEOCjsnUiOIMyEsSe2G", "eQc8SyWLUXmshglkKykBBtAHBq1Mp1HbPbqjsn3bMVCryverwp"]

# function to read each line of a file as a separate list element
def get_list_from_file(file_name):
	handle = open(file_name, "r")
	api_key_list = list(map(str.strip, handle.readlines()))
	return api_key_list

# read from file "api_call_count.txt" how many calls have been made in the day
def api_call_count():
	handle = open("api_call_count.txt", "r")
	count = int(handle.read().strip())
	return count

# write back to file the updated api call count
def api_count_update(count):
	handle = open("api_call_count.txt", "w")
	handle.write(str(count))

# function calls the spoonacular API, and gets tags associated with it
def call_api_tags(dish):
	dish = dish.lower().strip()
	result_tags = [] # result of the API call stored in result_tags
	miss_list = get_list_from_file("API_miss.txt") 
	# check if the API has been called on the same dish earlier and missed if
	# so, do not call the API on the dish again, to avoid wasting API calls
	if dish in miss_list:
		return result_tags

	else:
		api_keys = get_list_from_file("api_key.txt") # get list of all API keys, 6 avaliable with 50 calls each

		api_url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/products/classify" # URL to be invoked
		api_headers = {"Content-Type": "application/json","Accept": "application/json"}	# headers the URL should be called with
		api_data = {"upc": "","plu_code": ""} # the data to contain the dish name along with these keys, check API documentation at https://market.mashape.com/spoonacular/recipe-food-nutrition

		api_calls = api_call_count() # get calls made today
		api_current_key = (api_calls // 45) # make 45 calls from each key in a day (limit - 50)
		if api_calls >= 270: # if 45 calls made from each key, log - API could not be called
			message = "failed to call API on " + dish + ", daily limit crossed"
			write_files.log_data(message, "infoLogFile.txt")
		else:
			api_calls += 1
			api_count_update(api_calls)
			api_headers["X-Mashape-Key"] = api_keys[api_current_key] # Add API key to header

			api_data["title"] = dish # add dish name to the API call body
			api_data = json.dumps(api_data) # convert data to json object

			message = "calling API with key " + api_keys[api_current_key] + " for : " + dish
			write_files.log_data(message, "infoLogFile.txt") # log API called on dishname
			
			r = requests.post(api_url, data = api_data, headers = api_headers) # API called using POST method with data and headers
			r = r.text.replace(":null,", ":None,") # replace null in the returned API text by None
			r = eval(r) # convert returned text to a python dictionary 
			if "breadcrumbs" in r: # keyname that holds set of tags returned by the API is breadcrumbs - check API documentation at https://market.mashape.com/spoonacular/recipe-food-nutrition
				result_tags = r["breadcrumbs"]
			return result_tags # return API tags