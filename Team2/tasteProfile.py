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

def categoriseTaste(flavor):
	newflavor = ast.literal_eval(flavor)
	userID = open("lastedit.txt", "r").read().strip()

	flavorProfile = json.load(open("flavorProfile.json"))

	if userID in flavorProfile:
		f = flavorProfile[userID]

		if len(f) == 10:
			f = f[:9]
			f.insert(0, newflavor)
			flavorProfile[userID] = f

		else:
			flavorProfile[userID].insert(0, newflavor)

	else:
		flavorProfile[userID] = []
		flavorProfile[userID].insert(0, newflavor)

	json.dump(flavorProfile, open("flavorProfile.json", "w+"), indent = 4)