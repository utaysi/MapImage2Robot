import cv2
import numpy as np


image = cv2.imread('G:\\My Drive\\School\\Spring 2023\\CMP4992 - Capstone\\Project\\Map Images\\asd6.png')


buildingpos = []
print('------WTF!!!-------') #nazar printi

buildingLen = 0

for j in range(0, image.shape[1]):
    for i in range (0,image.shape[0]):
        if not np.array_equal(image[j,i], [255,255,255]): 
            buildingpos.append((i,j))



for za in range (len(buildingpos)-1):
    buildingLen += 1
    if (abs(buildingpos[za+1][0]-buildingpos[za][0]) > 1): 
        break

print(buildingLen)

#Finding building start positions
buildingstartpos = []
buildingstartpos.append(buildingpos[0])

prevBuilding = buildingpos[buildingLen]
firstRun = True
for la in range (buildingLen, len(buildingpos)-1, buildingLen):
    if (abs(buildingpos[la][1]-buildingpos[la-1][1]) == 0):
        if (firstRun):
            if(buildingpos[la][1]-buildingpos[0][1] != 1):
                buildingstartpos.append(buildingpos[la])
                print(buildingpos[la])
                prevBuilding = buildingpos[la]
                firstRun = False
            else:
                buildingstartpos.append(buildingpos[la-buildingLen])
                print(buildingpos[la-buildingLen])
                prevBuilding = buildingpos[la]
                firstRun = False
        elif(prevBuilding[0]-buildingpos[la][0] !=  0 and prevBuilding[1]-buildingpos[la][1] != -1):
            if(buildingpos[la][1]-buildingpos[0][1] != 1):
                buildingstartpos.append(buildingpos[la])
                print(buildingpos[la])
                prevBuilding = buildingpos[la]
            else:
                buildingstartpos.append(buildingpos[la-buildingLen])
                print(buildingpos[la-buildingLen])
                prevBuilding = buildingpos[la]


#print(image[2,8])


# for x in buildingpos:
#     print(x)

# # nazar printi
# print (image[0,0])
# print (image[19,19])
