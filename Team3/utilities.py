#utility
import hashlib
import sys
import json
import nltk

def parameterize(qstring):
		return qstring.strip('\n').replace(' ', '+')
		
def modmatchi(query_string, iterable, threshold):
	best_match = (None, None, -1)
	for word in iterable:
		result = modmatch(query_string, word, threshold)
		best_match = result if (result) and (result[2] > best_match[2]) else best_match
	return best_match

def modmatch(query_string, match_string, threshold):
	ps = nltk.PorterStemmer()
	match_string_split = [ps.stem(word) for word in match_string.strip().upper().replace(',',' ').split(' ')]
	query_string_split = [ps.stem(word) for word in query_string.strip().upper().replace(',',' ').split(' ')]
	match_string_split = list(filter(lambda x: x,match_string_split))
	query_string_split = list(filter(lambda x: x,query_string_split))
	matched = [word for word in query_string_split if word in match_string_split]
	if len(matched) > 0 or (' ' not in match_string and query_string.upper().strip().replace(',',' ') in match_string.upper().strip().replace(',',' ')):
		if len(matched) / len(query_string_split) >= threshold:
			return (match_string, query_string, round(len(matched) / len(query_string_split), 2))
	return None
'''
def modmatchlist(match_string, query_string, threshold):
	ps = nltk.PorterStemmer()
	match_string_split = [ps.stem(word) for word in match_string.strip().upper().replace(',',' ').split(' ')]
	query_string_split = [ps.stem(word) for word in query_string.strip().upper().replace(',',' ').split(' ')]
	if '&' in match_string_split:
		amp_index = match_string_split.index('&')
		str_after_amp = match_string_split[amp_index+1]
		str_before_amp = match_string_split[amp_index-1]
		match_string_split = match_string_split[:amp_index-1]
		match_string_split.append(str_before_amp+' & '+str_after_amp)
	if '&' in query_string_split:
		amp_index = query_string_split.index('&')
		str_after_amp = query_string_split[amp_index+1]
		str_before_amp = query_string_split[amp_index-1]
		query_string_split = query_string_split[:amp_index-1]
		query_string_split.append(str_before_amp+' & '+ str_after_amp)
		match_string_split = list(filter(lambda x: x,match_string_split))
		query_string_split = list(filter(lambda x: x,query_string_split))
		matched = [word for word in query_string_split if word in match_string_split]
		if len(matched) > 0 or (' ' not in match_string and query_string.upper().strip().replace(',',' ') in match_string.upper().strip().replace(',',' ')):
			if len(matched) / len(query_string_split) >= threshold:
				return matched
	return None

'''

def hash(input_title):
	return hashlib.md5(input_title.strip().upper().encode('utf-8')).hexdigest()

def package(input_file):
	contents = dict()
	with open(input_file) as ifile:
		for line in ifile:
			if not contents.__contains__(line[0]):
				contents[line[0]] = set()
			contents[line[0]].add(line.strip('\n'))
			
	for key in contents.keys():
		contents[key] = list(contents[key])
	with open(input_file.split('.')[0] + '.json', 'w') as writer:
		json.dump(contents, writer, indent='\t')

if __name__ == '__main__':
	package(sys.argv[1])