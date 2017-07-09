import taster
import sys
import glob
import os

def routine(file_list):
	for folder in file_list:
		for file in glob.iglob(folder + '/*_std', recursive=True):
			if not os.path.isdir(file):		
				taster.taste(file)
		print('\nDone with folder {0}'.format(folder))

if __name__ == '__main__':
	routine(sys.argv[1:])