

import pytesseract
from PIL import Image
import urllib.request
import io
from skimage import io
import cv2
import sys
import imutils
from skimage.filters import threshold_local
import base64



def loadImage(URL):
  image=io.imread(URL)
  #io.imshow(io.imread(URL))
  return image





#W=800

#resize_proc = imutils.resize(image,width=W)
#resize_orig = imutils.resize(image,width=W)



def cleanImage(image,stage=0):
    V = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    kernel= cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    # applying topHat/blackHat operations
    topHat = cv2.morphologyEx(V,cv2.MORPH_TOPHAT,kernel)         # light area with dark background
    blackHat = cv2.morphologyEx(V,cv2.MORPH_BLACKHAT,kernel)      # dark area with light background
    # add and subtract between morphological operations
    add = cv2.add(V,topHat)
    subtract = cv2.subtract(add,blackHat)

    if (stage ==1):
        return subtract
    T = threshold_local(subtract,29,offset=35,method="gaussian",mode="mirror")

    thresh=(subtract > T).astype("uint8")*255

    if (stage==2):
        return thresh
    # invert image
    thresh = cv2.bitwise_not(thresh)
    return thresh











def getAppendedString(l, start):
  s = ""
  for i in range(start, len(l)):
    s+=(l[i] +  ('' if i == len(l)-1 else " "))
  return s

def getDLInfo(data):
  info = {}
  for line in data.split("\n"):
    if line not in ['', '  ', ' ', '    ', '   ']:
      l = line.split(" ")
      if len(l) >= 2 and l[0] in ['1.', '1', '1,','i.']:
        info['lastName'] = getAppendedString(l, 1)
      if len(l) >= 2 and l[0] in ['2.', '2', '2,','_2']:
        info['firstName'] = getAppendedString(l, 1)
      if len(l) >= 2 and l[0] in ['3.', '3', '3,','39']:
        info['dob'] = l[1]
      if len(l) >= 2 and l[0] in ['5.', '5', '5,','e =i','_','eH']:
        info['dlNo'] = getAppendedString(l, 1)
  return info




def getUrl(URL):
    image = loadImage (URL)
    thresh = cleanImage (image, stage=1)

    img_rgb1 = cv2.cvtColor (thresh, cv2.COLOR_BGR2RGB)
    data1 = pytesseract.image_to_string (img_rgb1)

    img_rgb = cv2.cvtColor (loadImage (URL), cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_string (img_rgb)

    return getDLInfo (data1)


URL="https://authenticdriverslicense.com/wp-content/uploads/2020/02/5.png"

getUrl(URL)