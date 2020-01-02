import numpy as np
import cv2
from PIL import Image

cv2.destroyAllWindows() #Program will shut down if not shut down by q exit

cap = cv2.VideoCapture(0) #Sets what device to use for pictures

#while(True):
cv2.waitKey(50)
ret, frame = cap.read()
cv2.imshow('frame1', frame)

cv2.imwrite('frame1.jpg', frame)
#print('frame: ',frame)
im = Image.open('frame1.jpg')

print(im.format, im.size, im.mode)

pixel_array = [[0 for x in range(im.size[1])] for y in range(im.size[0])] #Long 1D array string?

#print(pixel_array)

for x in range(im.size[0]): #Assigns picture pixels to an array
    for y in range(im.size[1]):
         coordinate = (x-1, y-1)
         pixel_array[x][y] = im.getpixel(coordinate)


img = Image.new('RGB', im.size, color='red')
#gen_img = img.load()

gen_img = [0 for x in range(im.size[0]*im.size[1])]
#print(len(gen_img))
#each i increment is 480, and each j is 640. so 640 is the multiple, while 480 is added
for i in range(im.size[0]):    # for every col
    for j in range(im.size[1]):    # For every row
        #print("i: ",i,", j: ",j)
        gen_img[((i*480)+j)] = pixel_array[i][j]

#print(len(gen_img))
img.putdata(gen_img)
img.save('generated.jpg')

#img = Image.fromarray(pixel_array, 'RGB')
#img.save('generated.jpg')
#img =

#print(img[5,5])
#print(pixel_array[5][5])
#img[5,5] = pixel_array[5][5]

#for x in range(im.size[0]):
#    for y in range(im.size[1]):
#         img[x,y] = pixel_array[x][y]

#for x in range(im.size[0]): #displays pixels in a map format
#    print(pixel_array[x][:])

while(True): #Adds a stop so the program doesn't immediately close everything
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()