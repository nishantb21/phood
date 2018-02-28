import sys
from pymongo import MongoClient
import csv
import os
import json
my_path = os.path.abspath(os.path.dirname(__file__))


'''
To run:
python3 mediator.py rating userID selectedDish
'''
def getDocumentDetails(predictedDish):
    c = MongoClient()
    db = c.INDIANFOOD101
    collection = db.itemDetails2
    document = collection.find_one({'dish_name':predictedDish})
    del document['_id']
    with open(os.path.join(my_path,'input_file.json'),'w') as outfile:
        json.dump(document, outfile)
    dishID = document['dish_id']
    return dishID
def appendToReviewFile(dishID,userID,rating,path):
    fields = [str(dishID),str(userID),str(rating)]
    with open(path,'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fields)
def main():
    rating = eval(sys.argv[1])
    userID = eval(sys.argv[2])
    predictedDish = sys.argv[3]
    path = os.path.join(my_path,'Team 2/review.csv')
    dishID = getDocumentDetails(predictedDish)
    appendToReviewFile(dishID,userID,rating,path)
if __name__ == '__main__':
    main()
    print("Created input Path");
    sys.stdout.flush()
