import cv2
import difflib
from pathlib import Path

#see https://wiki.programstore.ru/python-sravnenie-kartinok/

#Calc hash
def CalcImageHash(FileName, x_size = 16, y_size = 16):
    image = cv2.imread(FileName) #Read image
    resized = cv2.resize(image, (x_size,y_size), interpolation = cv2.INTER_AREA) #Resize
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #Convert to grayscale
    avg = gray_image.mean() #mean value of pixel
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Thresold
    
    #hash calc
    _hash=""
    for x in range(x_size):
        for y in range(y_size):
            val=threshold_image[x,y]
            if val == 255:
                _hash=_hash+"1"
            else:
                _hash=_hash+"0"
            
    return _hash, avg
 
def CompareHash(hash1, hash2):
    l=len(hash1)
    i=0
    count=0
    while i<l:
        if hash1[i]!=hash2[i]:
            count=count+1
        i=i+1
    return count

last_hash = None
files = list()
for name in Path('dbg_files').glob('*.JP*'):
    hash_tmp, light_tmp = CalcImageHash(str(name), 32, 32)
    if light_tmp > 35:
        if last_hash == None or CompareHash(last_hash, hash_tmp) > 150:
            last_hash = hash_tmp
            files.append(str(name.stem))

print(files)

print('Ok')
