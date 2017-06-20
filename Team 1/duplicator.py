import os
from shutil import copyfile
rootdir = './chick fil a'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        src = os.path.join(subdir,file)
        for i in range(10):
            dst = src + "_" + str(i) + ".jpg"
            #copy the file with different name
            copyfile(src, dst)
