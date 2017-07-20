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

# function to get user logs
def get_new_log():
	# to suppress insecure warnings as the end point uses https - to 
	# access the end point without an SSL certificate
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

	# end points for the userlog, wishlist and purchased items
	urls = ['https://eventshop.ics.uci.edu:8004/userlog/', 'https://eventshop.ics.uci.edu:8004/wishlist/', 'https://eventshop.ics.uci.edu:8004/purchase/'] 

	# authentication ID and password
	auth = ('INDIA','SHINING')


	# user IDs that need to be profiled
	ids = ['56235e41-a73c-4479-9913-468709e0934a'] # incude more user IDs as ids = [ID1, ID2, ID3, ...]

	ans_record = [] # all user logs saved in ans_record

	for j in urls: # going through all endpoints in urls
		full_record = [] # contains record for the userlog, wishlist and purchase history individually for all users
		for i in ids: # fetching data for all users in ids
			req_url = j + i
			r = requests.get(req_url, auth=auth, verify=False) # get request for fetching the data
			record = json.loads(r.text) # loading the response into variable record
			full_record.extend(record) # adding all records for one user to full_record, which contains data for all users for a particular endpoint

		ans_record.append(full_record) # data for all users across the three endpoints

	json.dump(ans_record, open("logs.json", "w+"), indent = 4) # writing user logs to file logs.json

# uncomment the function call below to test the file
# get_new_log()