import json
import collections
import os
import re
import requests
import pickle
import copy
import logging
import sys

def makeDataToPlot():
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
	ans = json.dumps(ans)
	print(ans)