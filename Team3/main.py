import argparse
import datak
import taster
import json

parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
parser.add_argument("-p", "--profile", help="profile the specified dish", action='append')
arguments = parser.parse_args()

if arguments.profile:
	for dish in arguments.profile:
		datakresponse = datak.ingredient(dish)
		tastejson = taster.taste_dish(dish, datakresponse.nutrition_data)
		print(json.dumps(tastejson, sort_keys=True))
