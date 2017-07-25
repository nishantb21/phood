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

# Input for this function is the flavour profile passed from Team3 and it is converted into a dictionary. Then, the flavour profile of the user whose ID is present in a file which maintains User ID of the latest edit is accessed and his flavour profile is updated. This is then dumped into a json file
def categoriseTaste(flavor):
	newflavor = ast.literal_eval(flavor)
	userID = open("lastedit.txt", "r").read().strip()

	flavorProfile = json.load(open("flavorProfile.json"))

	if userID in flavorProfile:
		f = flavorProfile[userID]

		if len(f) == 20:
			f = f[:19]
			f.insert(0, newflavor)
			flavorProfile[userID] = f

		else:
			flavorProfile[userID].insert(0, newflavor)

	else:
		flavorProfile[userID] = []
		flavorProfile[userID].insert(0, newflavor)

	json.dump(flavorProfile, open("flavorProfile.json", "w+"), indent = 4)