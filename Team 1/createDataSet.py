from googleapiclient.discovery import build
import json
import requests
import jsbeautifier
import pprint
import os

my_api_key = "AIzaSyA7c4b13kDVqcGhKiAozS9-YdHV1btGsm4"
my_cse_id = "004130078630997984643:onnmdc_aavw"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType='image', **kwargs).execute()
    return res['items']

def get_number_of_dishes(filename):
    dish_ctr = 0
    fl = open(filename)
    json_data = json.load(fl)
    for i in json_data:
        dish_ctr += 1
    return dish_ctr

def getImages(menu,restaurantName):
	print("Restaurant Name:" + restaurantName)
	json_data = json.load(menu)
	ctr = 0
	for j in json_data:
		dishName = j['dishName']
		print(dishName)
		results = google_search(dishName, my_api_key, my_cse_id, num=10)
        #os.mkdir(dishName)
        #os.chdir(dishName)
        for i in results:
            print("Inside results")
            try:
                url = i['link']
                components = url.split('/');
                extension = components[len(components)-1].split('.')[1];
                urllib.urlretrieve(url,str(ctr))
                ctr += 1
            except:
                pass
            finally:
                pass
        break
	return ctr

os.chdir("./Menus/Has Menus")
menus = os.listdir(".")
for i in range(len(menus)):
    with open(menus[i],'r') as menu:
		restaurantName = menus[i].split(".")[0].replace("_"," ")

		# First create a directory for that restaurant
		print(get_number_of_dishes(menus[i]))
		print(getImages(menu,restaurantName))
		break
		# Then read the file as JSON data
