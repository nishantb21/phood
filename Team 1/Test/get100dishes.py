from googleapiclient.discovery import build
import json
import pprint
import urllib
import os
import sys

my_api_key = "AIzaSyCpI8nDmM3-3jRegNuxX0Q_U7zus9zmRDU"
my_cse_id = "017061563640751549217:b1vjokvjd8k"

def google_search(search_term, num, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, imgType="photo", searchType='image', start=num, **kwargs).execute()
    return res["items"]

def get_number_of_dishes(filename):
    dish_ctr = 0
    fl = open(filename)
    json_data = json.load(fl)
    for i in json_data:
        dish_ctr += 1
    return dish_ctr

def get_the_json_data(restaurantName,filename):
    terms = []
    fl = open(filename)
    json_data = json.load(fl)
    for i in json_data:
        terms.append(restaurantName + " " + i['dishName'])
    return terms

search_terms = get_the_json_data("burger king","burger king.json")

for term in search_terms:
    print("Dish Name is: " + str(term))
    if not(os.path.isdir(term)):
        os.mkdir(term)
    os.chdir(term)
    try:
        for i in range(10):
            ctr = i * 10 + 1
            print("Getting images from " + str(i*10+1) + " to" + str((i+1)*10))
            results = google_search(term,i*10+1,my_api_key,my_cse_id)
            for j in results:
                try:
                    url = j['link']
                    urllib.urlretrieve(url,str(ctr))
                except Exception as e:
                    print("Error in URL retrieval:", e)
                finally:
                    ctr += 1

    except Exception as e:
        print("Error: ", e)
        print("Iteration number: " + str(i))
        print("Dish Name: " + term)
    
    finally:
        os.chdir("..")
