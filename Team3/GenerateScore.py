# -*- coding: utf-8 -*- 
import glob
import csv
import json
import re
import jsbeautifier
import hashlib
import random
import sys
from ratip import ratio
from progress.bar import ShadyBar

args = sys.argv
x = glob.glob("ThaiCurry/WithIngsFixed/*.csv")
#print(x)
csvWrite = open("tasteScores.csv", 'a+',newline='')
writer = csv.writer(csvWrite,delimiter=',')
#writer.writerow(['foodName','hashName','sweetNutri','saltNutri','richnessNutri','sweetIngs','saltIngs','richnessIngs','Spicy','Sour','Bitter','Wasabi','Ingredients'])
nutrients_list = "Water;Energy;Energy;Protein;Total lipid (fat);Ash;Carbohydrate, by difference;Fiber, total dietary;Sugars, total;Sucrose;Glucose (dextrose);Fructose;Lactose;Maltose;Galactose;Starch;Calcium, Ca;Iron, Fe;Magnesium, Mg;Phosphorus, P;Potassium, K;Sodium, Na;Zinc, Zn;Copper, Cu;Manganese, Mn;Selenium, Se;Fluoride, F;Vitamin C, total ascorbic acid;Thiamin;Riboflavin;Niacin;Pantothenic acid;Vitamin B-6;Folate, total;Folic acid;Folate, food;Folate, DFE;Choline, total;Betaine;Vitamin B-12;Vitamin B-12, added;Vitamin A, RAE;Retinol;Carotene, beta;Carotene, alpha;Cryptoxanthin, beta;Vitamin A, IU (IU);Lycopene;Lutein + zeaxanthin;Vitamin E (alpha-tocopherol);Vitamin E, added;Tocopherol, beta;Tocopherol, gamma;Tocopherol, delta;Tocotrienol, alpha;Tocotrienol, beta;Tocotrienol, gamma;Tocotrienol, delta;Vitamin D (D2 + D3);Vitamin D2 (ergocalciferol);Vitamin D3 (cholecalciferol);Vitamin D (IU);Vitamin K (phylloquinone);Dihydrophylloquinone;Menaquinone-4;Fatty acids, total saturated;4:0;6:0;8:0;10:0;12:0;13:0;14:0;15:0;16:0;17:0;18:0;20:0;22:0;24:0;Fatty acids, total monounsaturated;14:1;15:1;16:1 undifferentiated;16:1 c;16:1 t;17:1;18:1 undifferentiated;18:1 c;18:1 t;18:1-11 t (18:1t n-7);20:1;22:1 undifferentiated;22:1 c;22:1 t;24:1 c;Fatty acids, total polyunsaturated;18:2 undifferentiated;18:2 n-6 c,c;18:2 CLAs;18:2 t,t;18:2 i;18:2 t not further defined;18:3 undifferentiated;18:3 n-3 c,c,c (ALA);18:3 n-6 c,c,c;18:3i;18:4;20:2 n-6 c,c;20:3 undifferentiated;20:3 n-3;20:3 n-6;20:4 undifferentiated;20:4 n-6;20:5 n-3 (EPA);21:5;22:4;22:5 n-3 (DPA);22:6 n-3 (DHA);Fatty acids, total trans;Fatty acids, total trans-monoenoic;Fatty acids, total trans-polyenoic;Cholesterol;Phytosterols;Stigmasterol;Campesterol;Beta-sitosterol;Tryptophan;Threonine;Isoleucine;Leucine;Lysine;Methionine;Cystine;Phenylalanine;Tyrosine;Valine;Arginine;Histidine;Alanine;Aspartic acid;Glutamic acid;Glycine;Proline;Serine;Hydroxyproline;Alcohol, ethyl;Caffeine;Theobromine"
nutrients_list = nutrients_list.split(';')
#widgets = ['Test: ', Percentage(), ' ', Bar(marker='0',left='[',right=']'),          ' ', ETA(), ' ', FileTransferSpeed()]
options = jsbeautifier.default_options()
options.brace_style = 'expand'

bar = ShadyBar(max=len(x))

class foodItem():
	name = ''
	ingredients = []
	ndbno = ''
	nutrients = dict()
	sweetScore = 0.0
	saltScore = 0.0
	fatScore = 0.0

	def __init__(self,filename):
		self.sweetScore = 0.0
		self.saltScore = 0.0
		self.fatScore = 0.0
		with open(filename,'r') as csvfile:
			self.name = csvfile.readlines()[2].strip()
		with open(filename,'r') as csvfile:
			reader = csv.reader(csvfile, delimiter = ",")
			for row in reader:
				if row:
					if row[0] in nutrients_list:
						#if re.findall('µg',row[1]):
							#row[1] = 'mug'
						self.nutrients[row[0]] = row[5]# + " " + row[1]
					if row[0] == "Ingredients":
						self.ingredients = next(reader)

	def getName(self):
		name_list = self.name.split('"')[1].split(',')
		self.ndbno = name_list[0].split(':')[1]
		name_list = name_list[1:]
		name = ''	
		for i in name_list:
			if "UPC:" in i:
				break
			name += i + ','
		#print(name[:-1].strip())
		return name[:-1].strip()

	def getIngredients(self):
		ingredients_list = re.split(r',\s*(?![^()]*\))',self.ingredients[0])
		#parenth_list = re.split(r'(,\s*(?![^()]*\))',self.ingredients[0])
		ingredients_list[-1] = ingredients_list[-1].split('Date')[0].strip()[:-1]
		ingredients_list = list(filter(None, ingredients_list))
		ingredients_list = [item.upper() for item in ingredients_list]
		return ingredients_list

	def getID(self):
		return self.ndbno

	def getNutrients(self):
		return self.nutrients

	#def getIngredientRatio(self):
	#	return ratio(len(self.getIngredients()))

	def updateSweetScore(self, value):
		self.sweetScore += value

	def updateSaltScore(self, value):
		self.saltScore += value

	def updateFatScore(self, value):
		self.fatScore += value

	def getSweetScore(self):
		#print(self.sweetScore)
		return self.sweetScore

	def getSaltScore(self):
		#print(self.saltScore)
		return self.saltScore

	def getFatScore(self):
		#print(self.fatScore)
		return self.fatScore


ings = set()

taste_q = ['richness','sweet','salt','umami']
taste_b = ['spicy','bitter','sour','wasabi']

print(len(ings))

def getTasteList(taste):
	with open('Boolean/'+taste) as tasteFile:
		return [i.strip() for i in tasteFile.readlines()]

spicyList = getTasteList('spicy')
sourList = getTasteList('sour')
bitterList = getTasteList('bitter')
wasabiList = getTasteList('wasabi')
umamiList = ['SODIUM GUANYLATE','SODIUM INOSINATE','INOSINATE','MONOSODIUM GLUTAMATE','GLUTAMATE','GUANYLATE','INOSINATE']
def getQuantIngList(taste):
	with open('Quantified/'+taste+'.json') as tasteFile:
		text = tasteFile.read()
		items = json.loads(text.encode('utf-8'))
		#print(items[0])
		return items

sweetDict = getQuantIngList('sweet')
saltDict = getQuantIngList('salty')
fatDict = getQuantIngList('fat')

umamiFoods = set()
def generateScore(dishCSV):
	food = foodItem(dishCSV)
	foodName = food.getName()
	foodIngredients = food.getIngredients()
	foodNutrients = food.getNutrients()
	#print(len(foodIngredients))
	foodIngredientRatio = ratio(len(foodIngredients))
	#print type(foodIngredientRatio[0])
	#print(foodIngredientRatio)
	hashName  = str(hashlib.md5(foodName.encode('utf-8')).hexdigest())
	#print(hashName)
	with open("saltScore.json",'a+') as saltScoreFile, open("sweetScore.json",'a+') as sweetScoreFile, open("richnessScore.json", 'a+') as richnessScoreFile:
		data = {}
		data['dish'] = foodName
		data['ingredients'] = foodIngredients
		data['sugar'] = foodNutrients['Sugars, total']
		#data['nutrients'] = foodNutrients
		#data['ndbno'] = food.getID() 
		data['taste'] = dict()
		data['taste']['sweetNutri'] = round(float(foodNutrients['Sugars, total'])/100,4)
		data['taste']['richnessNutri'] = round(float(foodNutrients['Total lipid (fat)'])/100,4)
		data['taste']['saltNutri'] = round(float(foodNutrients['Sodium, Na'])/39335,4)
		for taste in taste_b:
			data['taste'][taste] = False

		for item in range(0,len(foodIngredients)):
			for sweet in sweetDict.keys():
				if sweet in foodIngredients[item]:
				#	print(sweetDict[sweet], foodIngredientRatio[item], (sweetDict[sweet] * foodIngredientRatio[item])/100)
					food.updateSweetScore((sweetDict[sweet] * foodIngredientRatio[item])/100)
			'''
			for salt in saltDict.keys():
				if salt in foodIngredients[item]:
				#	print(saltDict[salt], foodIngredientRatio[item], (saltDict[salt] * foodIngredientRatio[item])/100)
					food.updateSaltScore((saltDict[salt] * foodIngredientRatio[item])/100)
			'''
			for fat in fatDict.keys():
				if fat in foodIngredients[item]:
				#	print(fatDict[fat], foodIngredientRatio[item], (fatDict[fat] * foodIngredientRatio[item])/100)
					food.updateFatScore((fatDict[fat] * foodIngredientRatio[item])/100)

			for umami in umamiList:
				if umami in foodIngredients[item]:
					umamiFoods.add(food)
			for spice in spicyList:
				if spice in foodIngredients[item] and (foodIngredientRatio[item] > 6.0):
					data['taste']['spicy'] = True
					break
			else:		
				for bitter in bitterList:
					if bitter in foodIngredients[item] and (foodIngredientRatio[item] > 15.0):
						data['taste']['bitter'] = True
						break
				else:
					for sour in sourList:
						if sour in foodIngredients[item] and (foodIngredientRatio[item] > 15.0):
							data['taste']['sour'] = True
							break

					else:
						for wasabi in wasabiList:
							if wasabi in foodIngredients[item]:
								data['taste']['wasabi'] = True
								break

		data['taste']['sweetIngs'] = food.getSweetScore()
		data['taste']['saltIngs'] = food.getSaltScore()/10
		data['taste']['richnessIngs'] = food.getFatScore()
		#foodFile.write(jsbeautifier.beautify(json.dumps(data),opts=options))
		#if args[1] == hashName:
		#	print(str(data))
		if data['taste']['sweetNutri'] > 0.0:
			sweetScoreFile.write('"' + foodName + '" : ' + str(data['taste']['sweetNutri']) + ',\n')
		if data['taste']['saltNutri'] > 0.0:
			saltScoreFile.write('"' + foodName + '" : ' + str(data['taste']['saltNutri'])+ ',\n')
		if data['taste']['richnessNutri'] > 0.0:
			richnessScoreFile.write('"' + foodName + '" : ' + str(data['taste']['richnessNutri'])+ ',\n')
		#writer.writerow([foodName,hashName,data['taste']['sweetNutri'],data['taste']['saltNutri'],data['taste']['richnessNutri'],data['taste']['sweetIngs'],data['taste']['saltIngs'],data['taste']['richnessIngs'],data['taste']['spicy'],data['taste']['sour'],data['taste']['bitter'],data['taste']['wasabi'],foodIngredients])
	#print str(foodIngredients) + " " + str(x.index(i)) + " " + i
	#for j in foodIngredients:
	#	ings.add(j.strip())

sample_list = [77563, 170551, 131548, 62692, 138628, 173067, 31312, 66662, 89753, 23072, 38337, 161273, 125932, 151670, 41466, 157282, 165724, 115704, 168456, 58095, 78144, 38334, 94519, 128805, 30442, 66307, 5404, 107299, 45499, 40677, 38570, 80963, 13469, 155346, 137058, 174804, 133245, 60427, 23942, 101461, 435, 49920, 73000, 123250, 86408, 6298, 64244, 158923, 67265, 99156, 143470, 14647, 38756, 74018, 101030, 80523, 165307, 126745, 111705, 171725, 107340, 28300, 141789, 72244, 38627, 63051, 83394, 84141, 21886, 28843, 158605, 92700, 162025, 96810, 133301, 94680, 93948, 168823, 49627, 114206, 79631, 139151, 9936, 110060, 128395, 10767, 144125, 154075, 87485, 6179, 155168, 115309, 144830, 62044, 58716, 66137, 150702, 128371, 133324, 135629, 107026, 150438, 54845, 173681, 174902, 36072, 136182, 110292, 119542, 7164, 61453, 146004, 10214, 117618, 38691, 107154, 98750, 63217, 157199, 40987, 5091, 61972, 173678, 33857, 149959, 130626, 65585, 55704, 143736, 17172, 51373, 76003, 75934, 164467, 123787, 149019, 21535, 69123, 112252, 161112, 153777, 26062, 87587, 58838, 97945, 8200, 98028, 109520, 170098, 8908, 62337, 144768, 72007, 51698, 147069, 34444, 171681, 52098, 7944, 127458, 54996, 80245, 107687, 124933, 170052, 120048, 93618, 172528, 104443, 133147, 108374, 93316, 84453, 14091, 125419, 57311, 23541, 20152, 78633, 45921, 32512, 142641, 67214, 114615, 143647, 147039, 88019, 55182, 18369, 132952, 15868, 145087, 38918, 19553, 150783, 125061, 76680, 156135, 144201, 138461, 46763, 125063, 167777, 52875, 88174, 151002, 105491, 61070, 69251, 87631, 133821, 173152, 121791, 39510, 139540, 21718, 140583, 128852, 127944, 53710, 144021, 92359, 62661, 122412, 43879, 152393, 109474, 39331, 105805, 111830, 129741, 17863, 170452, 157193, 128860, 41852, 16029, 106398, 93068, 44282, 156537, 111100, 31173, 33493, 85443, 67486, 46693, 85841, 90009, 20103, 139355, 43832, 110173, 151680, 36241, 146366, 161856, 148191, 153675, 52675, 6609, 76595, 82715, 81579, 12700, 108679, 30626, 33836, 120378, 119877, 146194, 26223, 152994, 6961, 14259, 70934, 97075, 80164, 71236, 152749, 64369, 36572, 116558, 59759, 44945, 16368, 93715, 29470, 85527, 169754, 144516, 66331, 130949, 169334, 24144, 86738, 79176, 113888, 79422, 111590, 150498, 124833, 77929, 128758, 37850, 74051, 22153, 6030, 139084, 150165, 25078, 169400, 153060, 8614, 127841, 78534, 171410, 31884, 111254, 98155, 44089, 110077, 85264, 168660, 7751, 61839, 60239, 55140, 144902, 93837, 107148, 126380, 173032, 165483, 4573, 100157, 98237, 91288, 33406, 56124, 87602, 132134, 113689, 48999, 9350, 15591, 151231, 39631, 74227, 120468, 18463, 21341, 57397, 71530, 137332, 119348, 99743, 116045, 63820, 166327, 53126, 12303, 41748, 121828, 77961, 85362, 60513, 167788, 162336, 89647, 20403, 164037, 157594, 150401, 25317, 150417, 166578, 20838, 23663, 117120, 82249, 135394, 131109, 28465, 15689, 130724, 81227, 76947, 173805, 61459, 6119, 142501, 101435, 39098, 60193, 55151, 155435, 123050, 93388, 160253, 120086, 152149, 108054, 136694, 31062, 165342, 29465, 159995, 44428, 89580, 32615, 47414, 1126, 172687, 72181, 154357, 89279, 103744, 111414, 152242, 60430, 78174, 68401, 48011, 165671, 72967, 102592, 60943, 162043, 9307, 138670, 28545, 5741, 96103, 68629, 117354, 89814, 82510, 43192, 37663, 125489, 50086, 41803, 151268, 76297, 145926, 76778, 78935, 93363, 65074, 174864, 129824, 159147, 117368, 134930, 135673, 93628, 7626, 95107, 148255, 66362, 152926, 11378, 152999, 105081, 129843, 52208, 8446, 55893, 28787, 114753, 48644, 18287, 79126, 17067, 58667, 93406, 54048, 159259, 131102, 130238, 21856, 103082, 47137, 142558, 73746, 87313, 34274, 71445, 53918, 84583, 131040, 47716, 133149, 76310, 169930, 166848, 98650, 31003, 171463, 132755, 160719, 98704, 137691, 95584, 101221, 34557, 174844, 47849, 146193, 149587, 173951, 56114, 44401, 140108, 79717, 117165, 118652, 112690, 3022, 23131, 153430, 105554, 103577, 97549, 140078, 78957, 115562, 147192, 119400, 47883, 84175, 93294, 132233, 16427, 48214, 33011, 65736, 145673, 106785, 118380, 157211, 51873, 73494, 102056, 18166, 30462, 77835, 73031, 16224, 93964, 82372, 166737, 150382, 167494, 108322, 93210, 139435, 27723, 96760, 8501, 121721, 33893, 171332, 132844, 170416, 53746, 33282, 30416, 10353, 173017, 1283, 68072, 9564, 99278, 21197, 146368, 48749, 11730, 8385, 6389, 165083, 32964, 38137, 134621, 41753, 30040, 47167, 126641, 88688, 162480, 127510, 30284, 155562, 168003, 77715, 58399, 11665, 70514, 117866, 97462, 6937, 67631, 67811, 15293, 39373, 3875, 67480, 163286, 139358, 152193, 71784, 85267, 165028, 146805, 19301, 55612, 5820, 35418, 149398, 24079, 134784, 165991, 20027, 43116, 150201, 134237, 9153, 3059, 93255, 84637, 39104, 16825, 5431, 61951, 30177, 161217, 39450, 117145, 88133, 31129, 9698, 69599, 120793, 137091, 31754, 37747, 26621, 60642, 104544, 142973, 171168, 163388, 122045, 163058, 266, 126379, 159233, 19767, 131592, 54893, 1735, 97710, 168716, 63115, 34562, 131464, 158349, 148188, 53310, 101830, 72622, 16119, 72629, 40599, 85993, 92117, 154207, 141803, 54052, 50662, 5041, 6973, 148439, 166746, 166102, 128436, 55317, 133662, 141434, 111163, 161030, 51020, 98633, 100227, 81767, 93269, 58146, 82434, 170850, 54108, 71594, 35506, 13409, 78034, 98182, 128115, 172272, 101499, 9526, 169447, 125575, 10814, 25947, 48981, 174255, 92661, 25007, 164861, 127562, 117359, 31931, 137685, 56452, 15861, 146177, 27121, 155253, 142707, 114459, 15337, 151455, 119645, 85789, 68303, 164297, 61105, 35502, 36830, 159202, 51287, 128011, 129336, 110913, 97204, 85896, 102138, 89978, 63515, 32923, 118608, 83609, 111112, 14595, 97334, 133085, 42608, 83415, 87277, 54262, 170120, 81391, 140371, 61656, 134833, 16556, 101541, 162186, 142617, 47379, 40204, 35910, 43120, 138300, 47323, 161046, 171057, 146625, 6192, 156301, 37041, 50680, 68005, 160758, 133997, 79437, 30851, 9516, 42485, 130898, 101058, 83682, 51610, 42425, 144075, 161650, 72326, 169515, 86006, 138190, 134343, 38915, 143253, 116239, 82736, 44005, 166933, 153357, 10023, 15687, 113922, 165800, 80625, 101036, 10587, 159559, 60947, 167463, 67782, 145364, 36782, 7754, 32850, 107845, 83834, 152685, 151585, 86996, 163120, 91526, 114314, 13744, 19216, 22677, 7237, 146077, 106898, 160180, 118813, 157210, 142570, 141523, 75360, 148230, 53347, 65780, 45279, 95908, 150663, 84848, 129313, 93666, 71072, 150533, 12751, 147207, 16160, 78501, 50985, 106556, 8210, 53421, 60922, 133023, 9647, 45962, 141285, 49775, 109230, 117698, 134797, 19876, 45884, 83244, 69255, 115910, 158938, 24279, 26780, 57243, 113863, 12717, 97283, 114228, 148263, 64063, 77743, 114118, 50369, 48245, 83147, 57935, 163483, 26180, 162343, 151869, 56500, 169585, 52870, 23006, 68081, 25631, 121205, 87170, 122855, 22490, 93514, 9635, 137845, 63081, 14489, 46636, 42100, 163884, 60557, 61901, 121530, 51784, 5999, 141191, 51247, 83232, 144071, 142495, 147066, 116453, 29689, 134240, 84288, 45192, 159128, 1274, 147401, 19978, 61718, 20945, 62516, 90303, 58606, 75151, 12943, 82308, 142096, 138235, 15429, 100772, 12389, 30091, 35249, 45500, 3379, 11780, 33862, 84743, 146733, 130113, 141705, 40970, 46071, 6802, 148593, 134270, 142847, 108461, 6350, 80212, 4250, 53242, 93276, 154610, 130205, 2925, 117931, 14653, 67809, 30752, 153130, 174423, 91733, 29838, 4557, 54645, 104663, 29489, 85526, 55346, 75730, 124125, 125280, 28321, 61569, 164559, 160205, 160010, 116902, 162216, 21175, 117814, 149117, 127320, 137146, 154363, 161262, 128631, 161382, 7171, 98250, 781, 145457, 128291, 20810, 77234, 93665, 30434, 115741, 54797, 62059, 131158, 161993, 83273, 75578, 122684, 152000, 90354, 8066, 156501, 53372, 5168, 134285, 156104, 107810, 33982, 27583, 56720, 173831, 173003, 5453, 112747, 65936, 71902, 95732, 159511, 35769, 47386, 173483, 161761, 60441, 120577, 114495, 99973, 126580, 78855, 128591, 29184, 151311, 126694, 164022, 90131, 89492, 59979, 110839, 112684, 147776, 123672, 3853, 109220, 94032, 77085, 84346, 101916, 23547, 48642, 35008, 45791, 61144, 35441, 28055, 14463, 150987, 117792, 101544, 37361, 76482, 31564, 170091, 66495, 155349, 113778, 32080, 158606, 6220, 156473, 116141, 60394, 88847, 36574, 19738, 144794, 154327, 129773, 143871, 171396, 173749, 42387, 66235, 113899, 132277, 115436, 20644, 168422, 53517, 155033, 125448, 115754, 139670, 157364, 20855, 167818, 163667, 73591, 96301, 103950, 36629, 157346, 156701, 46637, 135140, 18140, 170929, 24099, 41622, 57579, 92403, 80579, 78033, 129650, 19461, 49382, 46565, 7791, 153939, 145207, 63609, 77304, 18271, 39962, 155053, 96007, 43166, 50759, 19494, 54857, 16893, 110208, 130019, 159574, 139660, 68500, 62351, 9985, 144314, 101914, 147885, 41562, 119057, 91034, 83008, 76073, 3837, 154382, 75414, 37491, 142231, 33628, 140126, 13876, 43530, 22335, 160538, 5643, 128452, 145746, 2350, 28342, 82595, 138120, 66522, 161559, 120096, 132811, 31378, 41568, 78000, 74007, 49108, 131770, 62034, 128111, 32681, 39864, 47699, 115919, 91613, 28538, 92716, 151029, 48448, 168906, 47429, 60522, 13056, 59845, 118753, 47731, 160683, 59377, 77576, 102445, 173343, 148154, 144602, 79185, 158286, 169690, 173185, 34233, 160318, 29897, 118044, 7572, 91158, 106177, 171362, 73751, 17352, 62136, 82175, 129291, 154149, 131186, 153202, 114003, 88522, 139092, 134853, 7334, 11374, 51190, 62339, 137772, 115115, 2682, 71089, 128680, 139667, 131953, 39580, 63209, 134420, 151529, 114988, 992, 120376, 86269, 69564, 82575, 159055, 37622, 21875, 29350, 138161, 118193, 30561, 54753, 3582, 102073, 997, 91578, 40342, 30874, 76623, 113537, 114138, 74340, 151948, 12527, 75575, 17963, 512, 74058, 21170, 99124, 154753, 126091, 56156, 101952, 37366, 144898, 85996, 50218, 53292, 12292, 41547, 115772, 2285, 103288, 164977, 93067, 63904, 29830, 175052, 66146, 69333, 18025, 165343, 45489, 10549, 111806, 115519, 135295, 7717, 138792, 96295, 123641, 148738, 118347, 63981, 135458, 112207, 115262, 106137, 102577, 127609, 13299, 164075, 149363, 112220, 104585, 139132, 43428, 88410, 126798, 107871, 106776, 29901, 43689, 151380, 107337, 80544, 90076, 59363, 10788, 15931, 138189, 113399, 24546, 120324, 168014, 37207, 43944, 85741, 141632, 99656, 123235, 15800, 56913, 147756, 78796, 136983, 150686, 159093, 77525, 46621, 62078, 161022, 114472, 48444, 36965, 136703, 144734, 155190, 96819, 40638, 124268, 18790, 83173, 58379, 166664, 56998, 35523, 9070, 107941, 140575, 70517, 30199, 122693, 97515, 60900, 2341, 106462, 140416, 79799, 60693, 37614, 144448, 110741, 1541, 94347, 150688, 9849, 33697, 149549, 13814, 46654, 72972, 164081, 36851, 56819, 126669, 165903, 45811, 143885, 74942, 8104, 150125, 59655, 171376, 87691, 99997, 25125, 78839, 79586, 36188, 96332, 81514, 35551, 160174, 15363, 86018, 120357, 143925, 122455, 29432, 49983, 43011, 154993, 123608, 88667, 94346, 161651, 7430, 18749, 27944, 46432, 22462, 122912, 64066, 5040, 5556, 48562, 149157, 21168, 1879, 43885, 128271, 104735, 171987, 170257, 115689, 84268, 74407, 45687, 83495, 48198, 80881, 162411, 48777, 35057, 108356, 10662, 84112, 105649, 2640, 41623, 169047, 169388, 35309, 134694, 105123, 155915, 102877, 114925, 3504, 56765, 80322, 145592, 20478, 85053, 57653, 122308, 109494, 67846, 138888, 282, 77350, 150500, 74268, 43213, 85957, 147978, 77020, 53645, 138302, 82162, 10798, 113124, 44770, 142948, 173684, 15424, 70174, 30644, 3934, 49375, 158100, 36299, 139399, 39801, 100170, 97073, 47473, 27436, 160028, 60462, 153571, 152921, 137697, 69162, 79705, 53704, 148970, 113529, 88745, 143967, 136180, 165038, 30988, 24806, 70739, 35545, 113457, 44450, 92195, 109408, 110035, 153263, 51425, 159738, 64686, 8581, 122934, 55105, 18987, 124877, 120234, 100392, 86788, 132611, 129083, 73843, 103127, 140259, 116624, 79645, 95794, 52934, 120551, 81879, 30599, 38596, 149849, 162358, 83163, 44798, 68565, 153732, 102420, 123130, 36829, 85346, 128652, 142524, 61373, 47207, 82533, 77199, 98096, 143015, 134832, 151272, 79682, 50443, 3560, 160521, 146479, 75251, 56207, 144003, 22510, 38501, 123016, 130530, 102484, 30926, 160742, 5159, 131239, 157206, 54377, 40210, 124845, 93048, 15493, 110803, 11181, 116889, 72906, 27918, 38048, 22762, 76675, 127986, 77931, 115673, 43040, 155285, 21855, 66133, 126701, 174076, 84024, 92613, 61680, 61168, 147625, 30036, 138780, 153823, 55121, 109613, 81950, 161235, 10274, 91245, 110815, 98238, 107775, 50108, 157291, 142467, 51794, 99794, 159997, 130967, 35336, 7187, 88153, 9791, 23372, 132049, 73781, 16049, 73401, 100623, 174601, 4769, 159650, 91255, 150403, 67148, 49524, 94614, 3044, 134580, 60458, 77605, 142779, 86285, 107232, 150062, 158116, 144905, 48582, 143115, 111657, 104377, 14672, 121895, 31974, 96472, 148010, 107602, 143415, 645, 144987, 31419, 170554, 120766, 137862, 113773, 143022, 56543, 145044, 30121, 139535, 119512, 122763, 52540, 155718, 24264, 156598, 128445, 87003, 122256, 170789, 78294, 150607, 32609, 292, 114379, 99281, 127245, 152142, 32585, 25179, 144923, 126231, 58115, 122129, 21259, 62071, 64011, 139167, 70844, 88896, 140689, 65286, 45118, 79478, 119194]
print(len(sample_list))
for i in sample_list	:
	try:
		generateScore(x[i])
		bar.next()
	except UnicodeDecodeError:
		print()

bar.finish()
print("List Done")

'''
bar = Bar('Processing',max=len(ings))
with open("Ingredients.txt",'w+') as ingFile:
	for i in ings:
		ingFile.write(i+'\n')	
		bar.next()
bar.finish()
'''
with open("umamiFoods.csv",'a+',newline='') as umamiFile:
	writer = csv.writer(umamiFile,delimiter=',')
	for i in umamiFoods:
		writer.writerow([i.getName(),i.getIngredients()])