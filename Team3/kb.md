# kb.py - Knowledge Base Creation

## Rejector

### add(*self*, *words*):  
 *  Adds word to the reject list. All words are indexed by their first character.

### close(*self*)
 *  Closes rejects file

### process(*self*, *dirty_string*)  
 * Strips input of all undesirable parts, in the order listed :  
    * All unterminated braces
    * All punctuations
    * All extra spacing
 * Checks if input matches with any of the rejected words, and removes it from the list
 * **returns** cleaned string


## Acceptor

### close(*self*)
 *  Closes accepts file

### add(*self*, *word*):  
 *  Adds word to the accepts list. All words are indexed by their first character

### process(*self*, *dirty_string*)
 * Processes dirty string to get clean string via *Rejector.process()*
 * Splits string, checks if each word is exists in set of accepted words, else adds to reject list.
 * Adds string to acceptor list if number of parts matched vs total parts exceeds a certain *ACCEPT_THRESHOLD*

## Matcher

### close(*self*)
 *  Closes matches file

### add(*self*, *title*, *match*):  
 *  ?

### match(*self*,*match_query*)
 * ?


##


