import cv2
import numpy as np


image = cv2.imread('G:\\My Drive\\School\\Spring 2023\\CMP4992 - Capstone\\Project\\Map Images\\asd-2.png')


buildingpos = []
print('------WTF!!!-------') #nazar printi

counter = 0

for j in range(0, image.shape[1]):
    for i in range (0,image.shape[0]):
        if not np.array_equal(image[i,j], [255,255,255]): 
            buildingpos.append((i,j))



for za in range (len(buildingpos)-1):
    counter += 1
    if (abs(buildingpos[za+1][0]-buildingpos[za][0]) > 1): 
        break

print(counter)


buildingstartpos = []
buildingstartpos.append(buildingpos[0])
for la in range (0, len(buildingpos)-1, counter-1):
    if (abs(buildingpos[la+1][1]-buildingpos[la][1]) > 1):
        buildingstartpos.append(buildingpos[la])
        print(buildingpos[la])


# for x in buildingpos:
#     print(x)

# # nazar printi
# print (image[0,0])
# print (image[19,19])
