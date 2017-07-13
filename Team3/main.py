#wrapper for L2
import argparse
import layer1
import layer2
import glob
import json
import kb
import subprocess

parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
parser.add_argument("--build-kb", help="Specify the kb component to build", choices=['kb.acceptor', 'kb.rejector', 'kb.matcher'], action='append')
parser.add_argument("--rebuild-kb", help="Specify the kb component to rebuild", choices=['kb.acceptor', 'kb.rejector', 'kb.matcher'], action='append')
parser.add_argument("-p","--profile", help="profile the specified number of dish hashes", action='append')
parser.add_argument("--profile-all", help="profile all dishes in specified folder")
arguments = parser.parse_args()
print("Profiling {} dishes".format(arguments.profile_all or arguments.profile))
print("Knowledge base actions\nBuild: {}\tRebuild: {}".format(arguments.build_kb, arguments.rebuild_kb))

dish_pair = ('', [], None)
if arguments.profile_all:
	for dish in glob.iglob(arguments.profile_all + '*.json'):
		print("\r", dish, end='..')
		with open(dish) as dish_file:
			dish_json = json.load(dish_file)
		dish_pair = layer2.profile(dish_json["dish"], dish_json["ingredients"])
		print("done.      ", end='\r')
	#print("\n\n", dish_pair[0], dish_pair[1], sep='')

elif arguments.profile:
	for dish in arguments.profile:
		print("\r", dish, end='..    .')
		dish_json = layer1.return_score(dish)

		#with open(dish) as dish_file:
		#	dish_json = json.load(dish_file)
		dish_pair = layer2.profile(dish, dish_json["ings"], dish_json)
		print("done.      ", end='\r')
		#print("\n\n", dish_pair[0], dish_pair[1], sep='')


#Call team3 as a subprocess
subprocess.run(["python", "ratip.py", dish_pair[0], ",".join(dish_pair[1]) if dish_pair[1] != [] else ''])
layer2.kb.end()