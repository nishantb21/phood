import os
from os import listdir
from os.path import isfile, join
count = 0
mypath = "/home/kushal/UCI/phood/Team 1/Menus/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
for files in onlyfiles:
    f = mypath + files
    statinfo = os.stat(f)
    if statinfo.st_size <= 2:
        count = count + 1
print(count)
