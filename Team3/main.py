#wrapper for L2
import argparse
import layer1
import layer2
import glob
import json
import kb
import subprocess
from math import pi
import matplotlib.pyplot as plt

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
print(dish_name)
# Set data
cat = ['Sweetness', 'Saltiness', 'Richness']
values = [dish_name['sweet']*100, dish_name['salt']*100, dish_name['fat']*100]

N = len(cat)

x_as = [n / float(N) * 2 * pi for n in range(N)]

# Because our chart will be circular we need to append a copy of the first 
# value of each list at the end of each list with data
values += values[:1]
x_as += x_as[:1]


# Set color of axes
plt.rc('axes', linewidth=0.5, edgecolor="#888888")


# Create polar plot
ax = plt.subplot(111, polar=True)


# Set clockwise rotation. That is:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)


# Set position of y-labels
ax.set_rlabel_position(0)


# Set color and linestyle of grid
ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
ax.yaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)


# Set number of radial axes and remove labels
plt.xticks(x_as[:-1], [])

# Set yticks
plt.yticks([20, 40, 60, 80, 100], ["20", "40" "60", "80", "100"])


# Plot data
ax.plot(x_as, values, linewidth=0, linestyle='solid', zorder=3)

# Fill area
ax.fill(x_as, values, 'b', alpha=0.3)


# Set axes limits
plt.ylim(0, 100)


# Draw ytick labels to make sure they fit properly
for i in range(N):
    angle_rad = i / float(N) * 2 * pi

    if angle_rad == 0:
        ha, distance_ax = "center", 10
    elif 0 < angle_rad < pi:
        ha, distance_ax = "left", 1
    elif angle_rad == pi:
        ha, distance_ax = "center", 1
    else:
        ha, distance_ax = "right", 1

    ax.text(angle_rad, 100 + distance_ax, cat[i], size=10, horizontalalignment=ha, verticalalignment="center")


# Show polar plot
plt.show()