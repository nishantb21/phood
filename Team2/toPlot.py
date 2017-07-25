# Refer readme.md for brief information about each file.
# Refer files.md for detailed information about each file and functions used in each file.

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

# This program is gives the data for plotting graphs which visualises user's old data and the updated data.
# Retrieves the User ID from a file which maintains the ID of the latest edit. Uses this ID to get that user's old data and new data which is appended in the form an ordered dictionary.

def makeDataToPlot(flavor):
	userID = open("lastedit.txt", "r").read().strip()
	newdata = json.load(open("userscore.json"))
	olddata = json.load(open("oldscore.json"))

	for i in newdata:
		if i not in olddata:
			olddata[i] = {}
		
		if userID not in olddata[i]:
				olddata[i][userID] = {}
		
		for k in newdata[i][userID]:	
			if k not in olddata[i][userID]:
				olddata[i][userID][k] = 0

	ans = []

	for i in sorted(newdata):
		half_ans = []
		for k in sorted(newdata[i][userID]):
			half_ans.append((k, newdata[i][userID][k]))
		key = i + "new"
		ans.append((key, collections.OrderedDict(half_ans)))


	for i in sorted(olddata):
		half_ans = []
		for k in sorted(olddata[i][userID]):
			half_ans.append((k, olddata[i][userID][k]))

		key = i + "old"
		ans.append((key, collections.OrderedDict(half_ans)))

	ans = collections.OrderedDict(ans)

	if flavor:
		flavorProfile = json.load(open("flavorProfile.json"))
		if userID in flavorProfile:
			f = flavorProfile[userID]
			answer = f[0]
			for i in f[1:]:
				for j in i:
					answer[j] += i[j]

			for i in answer:
				answer[i] = round(answer[i] / len(f), 3)

			if 'spice' in answer:
				if answer['spice'] > 0.5:
					answer['spice'] = 1

				else:
					anser['spice'] = 0
			ans["flavor"] = answer
			
	ans = json.dumps(ans)
	return ans