# Layer 1

### get\_data\_from\_JSON(*food_item*)
**returns** nutritional information of *food_item* if corresponding JSON file exists.

### write\_data\_to\_JSON(*food_item, nutri\_info*)
Hashes *food_item*, creates JSON file populating it with its nutritional information (*nutri_info*)

### query\_JSON(*food_item*)
**returns** nutritional information of *food_item* if an exact match for JSON file is found 
Else, tries to find closest match and **returns** *nutri_info* after reading from JSON  
Else, **returns** *None*

### query\_nutritionix(*food_item*)
Since food item wasn't found in local storage, queries *food_item* to nutritionix and **returns** a result, and writes it to a file so it can be accessed 

### return_score(*food_item*)
**returns** nutritional information of queried *food_item* by:  

* Checking for JSON file (see: *query_JSON*)  
* Querying Nutritionix (see: *query_nutritionix*)
* **returns** None

##
