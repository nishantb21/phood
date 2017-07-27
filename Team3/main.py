import argparse
import datak
import taster
import json
import utilities
import os
import sys

parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
parser.add_argument("-p", "--profile", help="profile the specified dish", action='append')
arguments = parser.parse_args()

if arguments.profile:
	for dish in arguments.profile:
		nutrition = dict()
		# Call stop word scrubber here
		# add_sides(subtitle_list, main_title, save_to_file=True/False)
		if os.path.exists(utilities.hash(dish) + ".json"):
			with open(utilities.hash(dish) + ".json") as ifile:
				nutrition = json.load(ifile)
		else:
			nutrition = datak.ingredient(dish)
			if not nutrition["item_data"].lower() == dish.lower():
				print(nutrition["item_name"], file=sys.stderr)
			nutrition = nutrition.nutrition_data
		tastejson = taster.taste_dish(dish, nutrition)
		print(json.dumps(tastejson, sort_keys=True))
