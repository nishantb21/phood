# Utilities

### modmatch(*query\_string, match\_string, threshold*)
Compares the *query_string* with the *match_string* by checking how similar they are.  
**returns** a tuple containing the *match_string* and the score of how similar the strings are if the score is greater than the *threshold*,  
**returns** *None* otherwise

### modmatchi(*query\_string, iterable, threshold*)
Compares the *query_string* with each element in the *iterable* and **returns** best possible match

### modmatchir(*query\_string, nriterable, threshold*)
A variant of the **_modmatchi_** function, **returns** the index of the best match within the iterable.

### parameterize(*qstring*):
Replaces the spaces in query string with '+' and **returns**

### hash(*input_title*)
Cleans the string, encodes into UTF-8 and **returns** an MD5 hash of the string

### package(*input_file*)
Reads through an *input_file* and generates a 1-depth trie tree file.
Sorts every string in the file based on the first
character.

### standardize(*input_file*)
For every food item queried, a file is generated
This file is read and the scores are standardized, so that each dish's nutritional information corresponds to a 100g serving, and later outputted to another file

### ratio(*i_no = 1*):
Not in use.
Based on number of ingredients (*i_no*) in a particular dish, a percentage list is generated.
For an n-ingredient dish, a fraction of the *i*th dish is added to the first ingredient, and a percentage list is generated
**returns** percentage list

##


