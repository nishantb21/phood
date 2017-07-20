# Documentation - Team 2 : User Profiling


Programming language used : Python/Python3

Problem Statement : Given user logs, user has to be relavently scored for the dishes that were searched, purchased or added to the wishlist

##  Run through:

* Developed a knowledge base which contains ~1200 tags into which the dishes get tagged under. A hierarchy is maintained taking into consideration, the taxonomy of each item in the knowledge base, which will be used for scoring every tag, from the root, till the node in question, proportionately.
* Making use of an API (Spoonacular by Mashape) which tags the dishes in a very similar fashion to what our knowledge base contains. However, there are quite a few redundant tags returned by the API which are cleaned before getting added to the knowledge base and the hierarchy.

##  Flow:

* Dish which is taken as input is tagged appropriately from the knowledge base.
* If there are no matching tags (for the input) in the knowledge base, then the API is called.
* API call count is maintained since each API key is limited to 50 calls per day.
* The tags returned by the API are cleaned. These cleaned tags are then added to the knowledge base and hierarchy.
* Suppose the API does not return any tags for the queried dish, the dish is tagged with itself before it gets added to the knowledge base and to the hierarchy, as a top level tag.
* Once the dish is tagged, appropiate scoring is done based on where the tags lie in the hierarchy. Then user logs are queried for his old scores which are then updated with the new ones.
* There are differenent weights attached to the user logs based on whether he searched, purchased or added them to wishlist.
* The flavour profile of the user will also be modified in a similar fashion as that of user score, for every item queried by the user.

### Long term goal:
- Build a time-based decay function which decreases the user's scores over time, for a dish which is not being queried any more.
- Build a novelty function which keeps track of a dish which the user used to order a lot but has forgotten about it, currently.



## Program files:

- code.py - Main file which does the scoring and updates the user's score. Contains main()

- call_api.py - Program to call the Spoonacular API when the queried dish doesn't get matching tags from the knowledge base.

- cleaning.py - Program to clean the redundant / unwanted tags returned by the API. This program also adds the cleaned tags to the hierarchy and knowledge base.

- findleaves.py - This program locates the given tags for dish queried in the hierarchy and returns the number of leaves for that particular node. This is used for scoring the tags proportionately.

- GetLogs.py - Program to hit the eventshop endpoint for the given user ID and extract all his logs into a json file.

- write_files.py - Contains functions for writing content to dictionary, text file, pickle file, json file.

- tasteProfile.py - This program retrieves the flavour profile data from Team3 and is used for generating flavour profile for the user

## Database files:
- cuisine.pickle
- data1.pickle
- data2.pickle
- size.pickle
- vegnonveg.pickle
- cuisine_hierarchy.json
- h.json
- logs.json
- old_value.json
- sharedparents.json
- userscore.json

## Modules imported:
- json
- collections
- os
- re
- requests
- pickle
- copy
- logging
- sys
- matplotlib
