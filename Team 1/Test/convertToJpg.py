import sys
import os
import imghdr
from PIL import Image

for item in os.listdir("."):
    if(imghdr.what(item)=="jpeg"):
        os.rename(item,item+".jpg")
    else:
        try:
            im=Image.open(item)
            im.convert('RGB').save(item + ".jpg","JPEG")
            im.close()
            os.remove(item)
        except Exception as e:
            print("Error:",e)