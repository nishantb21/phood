'''
I/P format:
{
	"dish": "dish_name",
	"ingredients": [],
	"nutrients": {},
	"ndbno": 1234
}
'''

import hashlib
import os

taste_q = ['richness', 'sweet', 'salt', 'umami'] #Quantified
taste_b =	['spicy', 'bitter', 'sour','wasabi']   #Boolean


class Ingredient:
	def __init__(self, name, taste = None, weight = 0.0):
		self.name = name
		if taste is None:
			with open(os.path.join("Ingredients", str(hashlib.md5(self.name.upper()).hexdigest()) + ".json")) as ingfile:
				self.taste = json.loads(ingfile.read().splitlines())
				for nutrient,value in self.taste.items():
					self.taste[nutrient] = float(re.findall('\d+\.\d+', value)[0])
		else:
			self.taste = taste

		if weight !=  0.0:
			self.weight = weight

	def __getitem__(self, key):
		return self.taste[key]

class Dish:
	def __init__(self, dish = "salted butter", ingredients = list(), nutrients = dict()):
		with open(os.path.join("Food", str(hashlib.md5(self.dish.upper()).hexdigest()) + ".json")) as dishfile:
			self.jdish = json.loads(dishfile.read().splitlines())
			self.dish = self.jdish['dish']
			self.ingredients = self.jdish['ingredients']
			self.nutrients = self.jdish['nutrients']
			self.ndbno = self.jdish['ndbno']

		if isinstance(ingredients[0], Ingredient):
			self.ingredients = ingredients
		elif isinstance(ingredients[0], str):
			self.ingredients = list()
			for ingredient in ingredients:
				self.ingredients.append(Ingredient(ingredient))

		self.nutrients = nutrients
		self.taste = dict()

	def get_ingredients(self):
		return self.ingredients

	def get_nutrients(self):
		return self.nutrients

	def taste_score(self):
		'''Return taste score'''
		for ingredient in self.ingredients:
			for taste in taste_b:
				self.taste[taste] = ingredient[taste] * ingredient['weight']
			for taste in taste_q:
				self.taste[taste] += ingredient[taste] * ingredient['weight']
		return self.taste

	def __str__(self):
		return str(self.dish) + " : " + str(self.taste_score())

	def get_taste_weight(self):
		