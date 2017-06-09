import json
import requests
import jsbeautifier
import pprint

# To suppress Insecure warnings - to be dealt with later
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

req_url = 'https://eventshop.ics.uci.edu:8004/search/restaurant/location?lat=33.645864&lon=-117.842787&rad=2'
auth = ('INDIA','SHINING')
options = jsbeautifier.default_options()
options.brace_style = 'expand'

def getRestaurantIDs(req_url):
	restID_list = []
	# Just a hack to get past the verification
	r = requests.get(req_url, auth=auth,verify=False)
	record = json.loads(r.text)
	for i in record:
		restID_list.append((i['restaurantName'],i['restaurantId']))
	return restID_list

restID_list = getRestaurantIDs(req_url)

def getMenus(restID_list):
	without_menus = 0
	for i in restID_list:
		menu_url = 'https://eventshop.ics.uci.edu:8004/restaurant/'+ i[1] +'/menu'
		# Just a hack to get past verification
		r = requests.get(menu_url,auth=auth,verify=False)
		if (r.text == "[]"):
			without_menus += 1
		else:
			print(i[0] + ',' + i[1])
			with open('Menus/'+ i[0].encode('utf8') +'.json','w') as outfile:
				outfile.write(jsbeautifier.beautify(r.text,opts=options))
	return without_menus

getMenus(restID_list)
