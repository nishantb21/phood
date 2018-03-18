'''
User Profiler
'''

import random
import json
import taster
import copy
from dish import Dish


class Profile:
  def __init__(self, dishlistfile='testinp.json', history=20):
    self.flavourlist = ["salt", "sweet", "rich"]
    self.segpercs = [0.5, 0.3, 0.2]
    self.history = history
    self.items = list()

    with open(dishlistfile) as ifile:
      for item in json.load(ifile):
        self.items.append(Dish(item))

    self.historydata = random.sample(self.items, k=history)
    hist = copy.deepcopy(self.historydata)
    self.init_profile(hist)

  def init_profile(self, history):
    self.taste = dict()
    for flavour in self.flavourlist:
      self.taste[flavour] = 0.0

    for dish in history:
      tastedict = taster.taste(dish.data)
      # print(tastedict)
      for flavour in self.flavourlist:
        self.taste[flavour] += tastedict[flavour]

    for flavour in self.flavourlist:
      self.taste[flavour] /= len(history)

    print("Before adjustment: ", self.taste)
    delta = self.get_delta()
    print("delta: ", delta)
    for flavour in self.flavourlist:
      self.taste[flavour] += delta[flavour]

    print("After adjustment: ", self.taste)

  def dish_titles(self):
    return [food["dish_name"] for food in self.historydata]

  def __str__(self):
    return str(
        list(zip(self.dish_titles(),
                 [taster.taste(food) for food in self.historydata])))

  def get_delta(self):
    segoneindex = 0.35 * self.history
    seg_1 = self.historydata[0:segoneindex]
    seg_2 = self.historydata[segoneindex:segoneindex * 2]
    seg_3 = self.historydata[len(seg_1) + len(seg_2):]
    delta = dict(zip(self.flavourlist, [0] * len(self.flavourlist)))
    mappings = zip([seg_1, seg_2, seg_3], self.segpercs)
    for mapping in mappings:
      for dish in mapping[0]:
        if dish.rating < 3:
          delta[dish.most_significant_flavour] -= mapping[1] * \
              dish.flavours[dish.most_significant_flavour]

        else:
          delta[dish.most_significant_flavour] += mapping[1] * \
              dish.flavours[dish.most_significant_flavour]

    return delta

  def split(self):
    self.split = {
        "positives": list(),
        "negatives": list()
    }
    self.positivepercent = 0
    self.negativepercent = 0
    weight_per_dish = round(100 / self.history, 2)
    for dish in self.historydata:
      if dish.rating < 3:
        self.split["positives"].append(dish)
        self.negativepercent += weight_per_dish
      else:
        self.split["negatives"].append(dish)
        self.positivepercent += weight_per_dish

  def map_dishid(self, dishid):
    return self.items[dishid - 1]


def read_from_csv(inputfile="review.csv", headers=True):
  datalist = dict()
  with open(inputfile) as ifile:
    if headers:
      next(ifile)
    for line in ifile:
      line = line.strip("\n").strip().split(",")
      try:
        datalist[int(line[1])].append(
            {
                "dishid": int(line[0]),
                "rating": int(line[2])
            }
        )
      except KeyError:
        datalist[int(line[1])] = [{
            "dishid": int(line[0]),
            "rating": int(line[2])
        }]
  with open("reviews.json", "w") as outfile:
    json.dump(datalist, outfile, indent='  ')
    return datalist


if __name__ == "__main__":
  print(Profile())
