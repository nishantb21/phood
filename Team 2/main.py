import argparse

import matF
import factMachines

ap = argparse.ArgumentParser()
ap.add_argument("--matF", action='store_true')
ap.add_argument("--factM", action = 'store_true')
ap.add_argument("--retrain", action='store_true')
ap.add_argument("--predict")
argvalues = ap.parse_args()

if argvalues.matF:
	if argvalues.retrain:
		if argvalues.predict:
			matF.start(retrain = True, predict_on = int(argvalues.predict))
		else:
			matF.start(retrain  = True)

	else:
		if argvalues.predict:
			matF.start(retrain = False, predict_on = int(argvalues.predict))
		else:
			matF.start(retrain = False)

elif argvalues.factM:
	factMachines.start(predict_on = int(argvalues.predict))