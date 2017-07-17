import argparse
import layer1
import layer2
import glob
import json
import kb
from math import pi
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(prog="Fabric - Taste Profiler")
parser.add_argument("--build-kb", help="Specify the kb component to build")
parser.add_argument("-p","--profile", help="profile the specified dish hashes", action='append')
parser.add_argument("--profile-all", help="profile all dishes in specified folder")
arguments = parser.parse_args()

dish_pair = ('', [], None)
dish_name = str()
dish_json_l1 = dict()

if arguments.build_kb:
	for file in glob.iglob(arguments.build_kb + "/*.json"):
		jsonfile = dict()
		with open(file) as rfobj:
			file_json = json.load(rfobj)
		print('\r', file, end='\r')
		layer2.profile(file_json['name'], file_json['ingredients'])

if arguments.profile:
	for dish in arguments.profile:
		dish_json_l1 = layer1.return_score(dish.upper())
		
		if dish_json_l1 is not None:
			print(dish_json_l1)
			dish_pair = layer2.profile(dish, dish_json_l1['ingredients'])
			#print(dish_pair)			

layer1.end()
layer2.kb.end()
# Set data
print(dish_json_l1)
cat = ['Sweetness', 'Saltiness', 'Richness']
values = [dish_json_l1['sweet']*100, dish_json_l1['salt']*100, dish_json_l1['fat']*100]
if dish_pair is not None:
	values = [dish_pair[2]['sweet_score']*100, dish_pair[2]['salt_score']*100, dish_pair[2]['rich_score']*100]
print(values)

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
plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"])


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

plt.title(dish_name)
# Show polar plot
plt.show()
