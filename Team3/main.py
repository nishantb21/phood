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
#print("Profiling {} dishes".format(arguments.profile_all or arguments.profile))
#print("Knowledge base actions\nBuild: {}\tRebuild: {}".format(arguments.build_kb, arguments.rebuild_kb))

dish_pair = ('', [], None)
dish_name = str()
'''
if arguments.profile_all:
#		print("\r", dish, end='..')
		
		
		with open(dish) as dish_file:
			dish_json = json.load(dish_file)
		dish_name = dish_json['dish']
		dish_json_l1 = layer1.return_score(dish_json['dish'])
		
		if dish_json_l1 is not None:
			dish_pair = layer2.profile(dish_json["dish"], dish_json_l1["ings"], dish_json_l1)
		
			#print("done.      ", end='\r')
		#dish_pair = layer2.profile(dish_json["dish"], dish_json["ingredients"])
			if dish_pair is not None:
				#print("\n\n", dish_pair[0], dish_pair[1], sep='')
'''
#elif arguments.profile:
if arguments.profile:
	for dish in arguments.profile:
		#print("\r", dish, end='..')
		
		'''
		with open(dish) as dish_file:
			dish_json = json.load(utilities.hash(dish_file))
		dish_name = dish_json['dish']
		'''
		dish_json_l1 = layer1.return_score(dish)
		dish_name = dish_json_l1[dish_json_l1["name"]]
		if dish_json_l1 is not None:
			#print(dish_json_l1)
			dish_pair = layer2.profile(dish, dish_json_l1[dish_json_l1["name"]]["ings"], dish_json_l1)
		
		#	print("done.      ", end='\r')
		#dish_pair = layer2.profile(dish_json["dish"], dish_json["ingredients"])
			if dish_pair is not None:
		#		print("\n\n", dish_pair[0], dish_pair[1], sep='')
				pass

layer2.kb.end()

#Call team3 as a subprocess
# os.chdir("/home/dev/Demo/phood/Team2")
'''
if dish_pair is not None:
	#subprocess.run(["python3", "code.py", dish_pair[0], ",".join(dish_pair[1])])
	print(dish_pair[0])
	print(",".join(dish_pair[1]))
else:
	#subprocess.run(["python3", "code.py", dish_name])
'''
print(dish_name)