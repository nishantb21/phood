# Indian food recommendation

## Python Scripts to be run in this order
1. `python3 ../Team 1/oneShotLearning/Keras2-Oneshot/predictor.py /path/to/uploaded/image`
    This returns the predictions made on the image in a JSON format
2. `python3 ../Utilities/Team 2/mediator.py predictions(raw string) rating userID`
3. `python3 ../Team 2/Collaborative Filtering/matF.py --predict userID`
4. `python3 ../Team 3/taster.py --file input_file.json`
    The `input_file.json` is created automatically by `mediator.py`
