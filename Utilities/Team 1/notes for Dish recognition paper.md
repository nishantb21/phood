#ABSTRACT
* Simplify the classification problem by leveragin geolocation and external info about the restaurants
* Two approaches to this
  * geolocalized voting
  * combinations of bundled classifiers

##INTRODUCTION
###The Problem
Food classes are highly deformable, some food can have multiple appearances due to different cooking styles and seasonings.
###The solution
Use geotagged images and limit the candidate classes on to those few candidats based on geolocation (**Shortlist approach**). Exploit the information about the geographic location of the photo and about the dishes in the menu of the restaurants near that location, including user contributed images of those dishes.
###1st approach (Shortlist)
1. Use a global classifier to train over all the dish classes.
2. During test, geolocalize the problem by finding the restaurants within the geographic neighborhood of the test image and selecting only the dishes in their menus as potential classes for the test image.
3. There are _limitations_ in this. There is mismatch between the test settings(query-dependent) and the training settings. Models learned for the whole database are used over a query-dependent subset of classes.

###2nd approach
1. Introduction of geolocalized models and the related geolocalized training and model combination.
2. Complexity reduces when using geolocalized models. Testing and training data then become similar to those found for a particular image.

##DISCRIMINATIVE CLASSIFICATION IN GEOLOCALIZED SETTINGS
1. We are asssuming the user and hence the photo is located inside a restaurant.
2. We try to guess the dish rather than the food to emphasize the relation with the menu of the restaurant.
###Problems to expect
* Combined number of classes can be very very large.
* There can be visual variability for the same dish OR accidental similarity between non-related dishes
* These problems become significant in larger datasets with more restaurants.
