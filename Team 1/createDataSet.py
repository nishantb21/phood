from googleapiclient.discovery import build
import json
import requests
import jsbeautifier
import pprint
import os
import urllib
import sys

'''
API KEYS NEEDED
'''


my_api_key = ""
my_cse_id = ""

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

def getImages(menu,restaurantName,tot_number,start_count):
	print("Restaurant Name:" + restaurantName)
	json_data = json.load(menu)
	dish_number = 0
	print("Starting from dish number:" + str(start_count))
	for j in json_data:
		try:
			if dish_number >= start_count:
				ctr = 0
				dishName = restaurantName + " " + j['dishName']
				print(str(dish_number)+"/"+str(tot_number))
				results = google_search(dishName, my_api_key, my_cse_id, num=10)
				os.mkdir(dishName)
				os.chdir(dishName)
				for i in results:
					try:
						url = i['link']
						urllib.urlretrieve(url,str(ctr))
					except:
						pass
					finally:
						ctr += 1	
				os.chdir("..")
			dish_number += 1
		except:
			print("Error occurred at dish number:" + str(dish_number))
			print("Dish name is:" + dishName)
			break
	return dish_number

menus = os.listdir("./Menus/temp/")
save_file = open("save_state.csv","r")
state = save_file.readline().split(",")
restaurant_number = int(state[0])
start_count = int(state[1])

for i in range(len(menus)):
	if (i >= restaurant_number):
		with open("./Menus/temp/"+menus[i],'r') as menu:
			filename = "../Menus/temp/"+menus[i]
			restaurantName = menus[i].split(".")[0].replace("_"," ")

			# First create a directory for that restaurant if it doesn't exist already
			if not(os.path.isdir(restaurantName)):
				os.mkdir(restaurantName)

			# Change directory to that restaurant
			os.chdir(restaurantName)
			tot_number = get_number_of_dishes(filename)
			state_number = getImages(menu,restaurantName,tot_number,start_count)

			# Change the directory back to the parent directory before doing anything else
			os.chdir("..")

			# If the returned dish number is not the same as the total number of dishes then something went wrong
			if (state_number != tot_number):

				# Save the iteration number(or restaurant number) and the dish number in that restaurant
				restaurant_number = i
				save = open("save_state.csv","w")
				save.write(str(i)+","+str(state_number))

				# Change this to a raise exception instead of a break
				break

			else:
				start_count = -1