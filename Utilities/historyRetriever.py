import os
import csv
import sys
import time
from pymongo import MongoClient
def main(u):
    time.sleep(0.2)
    c = MongoClient()
    db = c.INDIANFOOD101
    collection = db.itemDetails2
    history = dict()
    my_path = my_path = os.path.abspath(os.path.dirname(__file__))
    userID = int(u)
    reviewList = list(csv.reader(open(os.path.join(my_path,'Team 2/review.csv'))))
    for i in reviewList[-(len(reviewList)-1):]:
        if int(i[1]) == userID:
            document = collection.find_one({'dish_id':int(i[0])})
            history[document['dish_name']] = int(i[2])
    print(history)
if __name__ == "__main__":
    main(sys.argv[1])
sys.stdout.flush()
