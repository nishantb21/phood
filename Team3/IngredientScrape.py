import requests
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup
number = str(58513)
numList = ['144321','105925',number]
def getNutritionData(number):
	nutritionData = dict()
	url = urlopen('https://ndb.nal.usda.gov/ndb/foods/show/'+number)
	page = BeautifulSoup(url,'html.parser')
	name = page.find('div',{"id":'view-name','style':"width:auto"})
	dishName = ''
	nameList = name.text.split('\n')[4].split(',')[1:]
	for i in nameList:
		if "UPC:" in i:
				break
		dishName += i + ','
	nutritionData['dishName'] = dishName[:-1].strip()
	td_list = page.findAll('td')
	for td in td_list:
		if "Sodium, Na" in td.text:
			#print "Na: " + td.findNext('td').findNext('td').findNext('td').text
			nutritionData['Sodium, Na'] = td.findNext('td').findNext('td').findNext('td').text

		if "Total lipid (fat)" in td.text:
			#print "Fat:" + td.findNext('td').findNext('td').findNext('td').text
			nutritionData['Total lipid (fat)'] = td.findNext('td').findNext('td').findNext('td').text

		if "Sugars, total" in td.text:
			#print "Sugar:" + td.findNext('td').findNext('td').findNext('td').text
			nutritionData['Sugars, total'] = td.findNext('td').findNext('td').findNext('td').text
	return nutritionData

for i in numList:
	print(getNutritionData(i))