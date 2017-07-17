# Layer 2

### nearest_ingredient(*ingredient*)
 * Hashes ingredient, checks for exact match, **returns** match
 * If not, matches with closest ingredient, **returns** closest match
 * If not found, queries nutritionix, **returns** nutrition data
 * Else, can't be found, **returns** *None*

### profile(*dish_title*, *ingredient_list*)
 **NOT IN USE**

 * Given *dish_title* and *ingredient_list*, generates a taste profile, assigning scores for the 
 *sweet*, *salt*, and *fat* tastes
 * An initial *profile* for each dish is generated from layer 1
 * For each *ingredient* in *ingredient_list*, generates individual scores for *sweet*, *salt*, and *fat* and adds to the overall profile of the *dish*
 * **returns** a tuple containing *dish_title*, *ingredient_list* and *profile*
