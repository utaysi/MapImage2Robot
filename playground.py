# Importing Image from PIL package
from PIL import Image
from PIL import ImageFilter

# creating a image object
im = Image.open(r"G:\My Drive\School\Spring 2023\CMP4992 - Capstone\Project\Map Images\map.jpg")
im2 = Image.open(r"G:\My Drive\School\Spring 2023\CMP4992 - Capstone\Project\Map Images\map2.jpg")





counter = 0
buildingpos = 0


# for j in range (0,im.size[1]):
#     for i in range (0,im.size[0]):
#         if(im.getpixel((i,j)) == (0,0,0) ):
#             print(i,j)
#             j+=100
#             counter+= 1
            
#             #if(buildingpos == 0 | buildingpos <)
#             buildingpos = (i,j)
# print('Counter: ' + str(counter))


print('------WTF!!!-------')
im3 = Image.open(r"G:\My Drive\School\Spring 2023\CMP4992 - Capstone\Project\Map Images\asd.jpg")
for j in range(0, im3.size[1]):
    for i in range (0,im3.size[0]):
        if(im3.getpixel((i,j)) != (255,255,255) ):
            print((i,j))







# counter2 = 0
# for j in range (0,im2.size[1]):
#     for i in range (0,im2.size[0]):
#         if(im2.getpixel((i,j)) != (255,255,255) ):
#             i+=100
#             counter2+= 1
# print('Counter: ' + str(counter2))
