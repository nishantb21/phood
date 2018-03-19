'''
User Profiler
'''

import random
import json
import taster
import copy
from dish import Dish
import sys


class Profile:
  def __init__(self, dishlistfile='tasteinp.json', history=20):
    self.flavourlist = ["salt", "sweet", "rich"]
    self.segpercs = [0.5, 0.3, 0.2]
    self.history = history
    self.items = list()

    with open(dishlistfile) as ifile:
      for item in json.load(ifile):
        self.items.append(Dish(item))
    # Uncomment for testing
    # self.historydata = random.sample(self.items, k=history)
    self.historydata = copy.deepcopy(self.items)
    self.init_profile(self.historydata)

  def init_profile(self, history):
    self.taste = dict()
    for flavour in self.flavourlist:
      self.taste[flavour] = 0.0

    # for dish in history:
      # tastedict = taster.taste(dish.data)
    for tastedict in history:
      for flavour in self.flavourlist:
        self.taste[flavour] += tastedict[flavour]

    for flavour in self.flavourlist:
      self.taste[flavour] /= len(history)

    # sys.stdout.write("Before adjustment: ")
    # sys.stdout.write(str(self.taste))
    delta = self.get_delta()
    # sys.stdout.write("\ndelta: ")
    # sys.stdout.write(str(delta))
    for flavour in self.flavourlist:
      self.taste[flavour] += delta[flavour]

    # sys.stdout.write("\nAfter adjustment: ")
    # sys.stdout.write(str(self.taste))

    ceiling = max(self.taste.values())
    if ceiling > 10:
      for key in self.taste:
        self.taste[key] = self.taste[key] * 10 / ceiling

  def dish_titles(self):
    return [food["dish_name"] for food in self.historydata]

  def __str__(self):
    for key in self.taste:
      self.taste[key] = round(self.taste[key], 2)
    return json.dumps(self.taste, sort_keys=True)

  def get_delta(self):
    segoneindex = int(0.35 * self.history)
    seg_1 = self.historydata[0:segoneindex]
    seg_2 = self.historydata[segoneindex:segoneindex * 2]
    seg_3 = self.historydata[len(seg_1) + len(seg_2):]
    delta = dict(zip(self.flavourlist, [0] * len(self.flavourlist)))
    mappings = zip([seg_1, seg_2, seg_3], self.segpercs)
    for mapping in mappings:
      for dish in mapping[0]:
        for flavour in self.flavourlist:
          if dish.overall_rating < 3:
            delta[flavour] -= (mapping[1] *
                               dish.flavours[flavour]) / 8.6

          else:
            delta[flavour] += (mapping[1] *
                               dish.flavours[flavour]) / 8.6

    for key in delta.keys():
      delta[key] = round(delta[key], 2)
    return delta


def read_from_csv(inputfile="review.csv", headers=True):
  datalist = list()
  with open(inputfile) as ifile:
    if headers:
      next(ifile)
    for line in ifile:
      line = line.strip("\n").strip().split(",")
      datalist.append(
          {
              "dishid": int(line[0]),
              "userid": int(line[1]),
              "rating": int(line[2])
          }
      )
  with open("reviews.json", "w") as outfile:
    json.dump(datalist, outfile, indent='  ')
    return datalist


if __name__ == "__main__":
  print(Profile())
