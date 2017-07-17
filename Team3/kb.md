# kb.py - Knowledge Base Creation

##

# Rejector

##  kb.Rejector.add(*self*, *words*):  
 *  Adds word to the reject list. All words are indexed by their first character.

#### parameters:
- *words* - A list of words to be added to the reject list

#### returns: 
- *None*


## kb.Rejector.close(*self*)
 *  Closes rejects file

#### parameters:
- *None*

#### returns: 
- *None*


## kb.Rejector.process(*self*, *dirty_string*)  
 * Strips input of all undesirable parts, in the order listed :  
    * All unterminated braces
    * All punctuations
    * All extra spacing
 * Checks if input matches with any of the rejected words, and removes it from the list
 * **returns** cleaned string

#### parameters:
- *dirty_string* - String to be processed

#### returns: 
- Cleaned *string*

##

# Acceptor

## kb.Acceptor.close(*self*)
 *  Closes accepts file

#### parameters:
- *None*

#### returns: 
- *None*

## kb.Acceptor.add(*self*, *word*):  
 *  Adds word to the accepts list. All words are indexed by their first character

#### parameters:
- *word* - Word to be added to the accept list
#### returns: 
- *None*

## kb.Acceptor.process(*self*, *dirty_string*)
 * Processes dirty string to get clean string via *Rejector.process()*
 * Splits string, checks if each word is exists in set of accepted words, else adds to reject list.
 * Adds string to acceptor list if number of parts matched vs total parts exceeds a certain *ACCEPT_THRESHOLD*

#### parameters:
- *dirty_string* - String to be processed

#### returns: 
- *None*

##

# Matcher

## kb.Matcher.close(*self*)
 *  Closes matches file

#### parameters:
- *None*

#### returns: 
- *None*

## kb.Matcher.add(*self*, *title*, *match*):  
 *  ?

### parameters:
- *title* - dish title
- *match* - String to be matched with

#### returns: 
- *None*


## kb.Matcher.match(*self*,*match_query*)
 * ?

#### parameters:
- *match_query* - String for which a match is to be found

#### returns:
- *key* on match success
- *None* on match failure



##


