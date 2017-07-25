import argparse
import datak
import taster
import os
import json
import utilities

parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
parser.add_argument("-p", "--profile", help="profile the specified dish hashes", action='append')
arguments = parser.parse_args()

if arguments.profile:
	for dish in arguments.profile:
		datakresponse = datak.ingredient(dish)
		tastejson = taster.taste_dish(datakresponse.nutrition_data)
		print(tastejson)
		if not os.path.exists(os.path.join("tasted", utilities.hash(datakresponse.name))):
				with open(datakresponse.name, 'w') as outfile:
					json.dump(tastejson, outfile, indent='\t')
