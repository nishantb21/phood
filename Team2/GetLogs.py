import json
import requests
import os
import re

# to suppress insecure warnings - to be dealt with later
def get_new_log():
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

	urls = ['https://eventshop.ics.uci.edu:8004/userlog/', 'https://eventshop.ics.uci.edu:8004/wishlist/', 'https://eventshop.ics.uci.edu:8004/purchase/']
	auth = ('INDIA','SHINING')

	ids = ['56235e41-a73c-4479-9913-468709e0934a']
	# ids = ['cd21f093-b703-4ed4-aac5-845244b3ec27']

	ans_record = []

	for j in urls:
		full_record = []
		for i in ids:
			req_url = j + i
			r = requests.get(req_url, auth=auth,verify=False)
			record = json.loads(r.text)
			full_record.extend(record)

		ans_record.append(full_record)

	json.dump(ans_record, open("logs.json", "w+"), indent = 4)

# get_new_log()