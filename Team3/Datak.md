# Datak

### ingredient(*query*)
Queries Nutritionix, by checking for best match amongst results provided by search predictor, and returns an object of type *NutritionixResponse* on a successful query

### leech(*for_file*,*folder*)
*for_file* is a file that contains a list of dishes, which are queried via **ingredient(*query*)** , and writes the nutritional information to a file


## NutritionixResponse:
* **name**  
Name of the item queried  
* **item_id**  
Nutritionix's internal id used to tag items
* **item_type**  
?
* **nutrition_data**  
Contains the nutritional information of the item queried





