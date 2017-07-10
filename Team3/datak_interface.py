'''
datak interface. Use as follows:
python datak_interface.py <files, space-seperated>
'''
import datak
import sys
from multiprocessing import Pool

def routine(file_list):
	with Pool(len(file_list)) as process_pool:
		process_pool.map(datak.leech, file_list)

if __name__ == '__main__':
	routine(sys.argv[1:])