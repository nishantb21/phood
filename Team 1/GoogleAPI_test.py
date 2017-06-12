from googleapiclient.discovery import build
import json
import pprint
import urllib
import os

my_api_key = "AIzaSyA7c4b13kDVqcGhKiAozS9-YdHV1btGsm4"
my_cse_id = "004130078630997984643:onnmdc_aavw"
ctr = 0
_ctr = 0
restauranName = "jamba juice"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def get_number_of_dishes(filename):
    dish_ctr = 0
    fl = open(filename)
    json_data = json.load(fl)
    for i in json_data:
        dish_ctr += 1
    return dish_ctr

json_file = open('jamba_juice.json')
json_data = json.load(json_file)
pp = pprint.PrettyPrinter(depth=6)
os.chdir('jamba juice')
for j in json_data:
    if not(_ctr < 197):
        #print("Dish Number: " + str(_ctr) +)
        ctr = 0
        dishName = restauranName + j['dishName']
        print("Dish Name: " + dishName)
        results = google_search(dishName, my_api_key, my_cse_id, num=10)
        os.makedirs(dishName)
        os.chdir(dishName)
        for i in results:
            try:
                url = i['link']
                components = url.split('/');
                extension = components[len(components)-1].split('.')[1];
                urllib.urlretrieve(url,str(ctr))
                ctr += 1
            except:
                pass
        os.chdir('..')

    _ctr += 1
'''
'''
ctr = 0;
json_file = open('mcDonalds.json')
json_data = json.load(json_file)
pp = pprint.PrettyPrinter(depth=6)
for j in json_data:
    ctr += 1

print("Total number of dishes:" + str(ctr))
