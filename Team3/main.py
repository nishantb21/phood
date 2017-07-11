#wrapper for L2
import argparse
import layer2
import glob
import json

parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
parser.add_argument("--build-kb", help="Specify the kb component to build", choices=['kb.acceptor', 'kb.rejector', 'kb.matcher'], action='append')
parser.add_argument("--rebuild-kb", help="Specify the kb component to rebuild", choices=['kb.acceptor', 'kb.rejector', 'kb.matcher'], action='append')
parser.add_argument("-p","--profile", help="profile the specified number of dish hashes", action='append')
parser.add_argument("--profile-all", help="profile all dishes in specified folder")
arguments = parser.parse_args()
print("Profiling {} dishes".format(arguments.profile_all))
print("Knowledge base actions\nBuild: {}\tRebuild: {}".format(arguments.build_kb, arguments.rebuild_kb))


if arguments.profile_all:
	for dish in glob.iglob(arguments.profile_all + '*.json'):
		print(dish)
		with open(dish) as dish_file:
			dish_json = json.load(dish_file)
			layer2.profile(dish_json["dish"], dish_json["ingredients"])
elif arguments.profile:
	for dish in arguments.profile:
		with open(dish) as dish_file:
			dish_json = json.load(dish_file)
			layer2.profile(dish_json["dish"], dish_json["ingredients"])