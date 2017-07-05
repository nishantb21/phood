'''
datak interface. Use as follows:
python datak_interface.py <files, space-seperated>
'''
import datak
import sys
from multiprocessing import Pool

print(__doc__)

with Pool(len(sys.argv[1:])) as process_pool:
	process_pool.map(datak.leech, sys.argv[1:])