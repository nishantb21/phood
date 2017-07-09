#utility
import hashlib
import sys
import json

def parameterize(qstring):
		return qstring.strip('\n').replace(' ', '+')
		
def modmatchi(query_string, iterable, threshold):
	best_match = (None, -1)
	for word in iterable:
		result = modmatch(query_string, word, threshold)
		best_match = result if result[1] > best_match[1] else best_match
	return best_match

def modmatch(query_string, match_string, threshold):
	match_string_split = match_string.strip().upper().split(' ')
	query_string_split = query_string.strip().upper().split(' ')
	matched = [word for word in query_string_split if word in match_string_split]
	if len(matched) > 0 or (' ' not in match_string and query_string.upper().strip() in match_string.upper().strip()):
		if len(matched) / len(query_string_split) >= threshold:
			return (query_string, round(len(matched) / len(query_string_splitlen(matched) / len(query_string_split, 2))))
	return None

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