import json
import requests
import jsbeautifier
import pprint

req_url = 'http://eventshop.ics.uci.edu:8004/search/restaurant/location?lat=33.645864&lon=-117.842787&rad=2'
auth = ('INDIA','SHINING')
options = jsbeautifier.default_options()
options.brace_style = 'expand'

def getRestaurantIDs(req_url):
	restID_list = []
	r = requests.get(req_url, auth=auth)
	record = json.loads(r.text)
	for i in record:
		restID_list.append((i['restaurantName'],i['restaurantId']))
		#print(i,'\n')	
	#print i['restaurantId']
	return restID_list

restID_list = getRestaurantIDs(req_url)
test_list = [('something','cf40c45d-0160-410a-892a-cbc78011de8a')]

def getMenus(restID_list):
	for i in restID_list:
		menu_url = 'http://eventshop.ics.uci.edu:8004/restaurant/'+ i[1] +'/menu'
		r = requests.get(menu_url,auth=auth)
		with open('Menus/'+ i[0].encode('utf8') +'.json','w') as outfile:
			outfile.write(jsbeautifier.beautify(r.text,opts=options))
		print(i[0].encode('utf8'))
getMenus(restID_list)